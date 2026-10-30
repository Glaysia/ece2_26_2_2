#!/usr/bin/env python3
"""Prepare the exact LAB1 S75 database on Linux/macOS without Vivado.

The fabric correction is pinned to openXC7/prjxray-db PR 15. The adjacent
CSV was measured from xc7s75fgga484-1, not copied from another package.
See evidence/openxc7/database-provenance.json for its provenance.
"""
import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

COMMIT = 'a3cc0736a90c697b7d4c40319f847a5b6988df62'
PART = 'xc7s75fgga484-1'
PINS_SHA = '34f526ca240f522b9b971e470dd72f5884f7e311e18bc460a6f49431bf80675e'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.home()/'fpga-cli/lab1-s75')
    parser.add_argument('--tools', type=Path, default=Path.home()/'.apio/packages/openxc7')
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    tools = args.tools.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    pins = Path(__file__).with_name(PART+'-package-pins.csv')
    if digest(pins) != PINS_SHA:
        raise ValueError('Unexpected package pin CSV hash')
    db = root/'prjxray-db'
    def run(argv, log=None):
        print(' '.join(map(str, argv)), flush=True)
        if log:
            with (root/log).open('w') as stream:
                subprocess.run(list(map(str, argv)), check=True, stdout=stream, stderr=subprocess.STDOUT)
        else:
            subprocess.run(list(map(str, argv)), check=True)
    if not db.exists():
        run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
             'https://github.com/openXC7/prjxray-db.git', db])
        run(['git', '-C', db, 'fetch', '--depth', '1', 'origin', COMMIT])
        run(['git', '-C', db, 'checkout', '--detach', COMMIT])
        run(['git', '-C', db, 'sparse-checkout', 'set', 'spartan7'])
    actual = subprocess.check_output(['git', '-C', str(db), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != COMMIT:
        raise ValueError('Existing database has a different revision; use a new --root')
    family = db/'spartan7'
    grid = json.loads((family/'xc7s100/tilegrid.json').read_text())
    rows = list(csv.DictReader(pins.read_text().splitlines()))
    if len(rows) != 338 or len({r['pin'] for r in rows}) != 338:
        raise ValueError('Incomplete or duplicate package pins')
    for row in rows:
        if row['site'] not in grid[row['tile']]['sites']:
            raise ValueError('Pin site absent from fabric: '+row['pin'])
    by_pin = {r['pin']: r for r in rows}
    assert by_pin['B6']['site'] == 'IOB_X1Y174'
    assert by_pin['K4']['site'] == 'IOB_X1Y129'
    (family/PART/'package_pins.csv').write_bytes(pins.read_bytes())
    # This exporter predates devices.yaml support. Apply that exact upstream
    # S75 -> S100 fabric mapping while retaining the S75 part and package.
    alias = family/'xc7s75'
    if not alias.exists():
        alias.symlink_to('xc7s100', target_is_directory=True)
    if alias.resolve() != (family/'xc7s100').resolve():
        raise ValueError('Unexpected S75 fabric directory')
    bba = root/(PART+'.bba')
    chipdb = root/(PART+'.bin')
    run(['python3', tools/'share/nextpnr/python/bbaexport.py', '--xray', family,
         '--device', PART, '--bba', bba], 'export.log')
    run([tools/'bin/bbasm', '--l', bba, chipdb], 'bbasm.log')
    record = {'part': PART, 'database_commit': COMMIT, 'package_pins': 338,
              'package_pins_sha256': digest(pins), 'chipdb_sha256': digest(chipdb),
              'tilegrid_sha256': digest(family/'xc7s100/tilegrid.json'),
              'part_yaml_sha256': digest(family/PART/'part.yaml'),
              'exporter_sha256': digest(tools/'share/nextpnr/python/bbaexport.py'),
              'db_root': str(family), 'chipdb': str(chipdb)}
    (root/'prepared.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
