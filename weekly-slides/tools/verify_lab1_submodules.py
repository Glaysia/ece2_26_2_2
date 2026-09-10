"""Verify pinned remote examples, checkout bytes and simulation in fresh clones."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB1'


def command(args,cwd):
    return subprocess.check_output(args,cwd=cwd,text=True,encoding='utf-8',errors='replace').strip()


def main():
    entries=json.loads((LAB/'docs/example-repositories.json').read_text())
    out=ROOT/'tmp/submodule-checkout-v2'
    out.mkdir(exist_ok=True)
    results=[]
    for e in entries:
        target=out/e['project'].replace('/','-')
        if target.exists():
            raise FileExistsError(f'Use a fresh checkout directory: {target}')
        command(['git','clone','--quiet',e['repository'],str(target)],ROOT)
        assert command(['git','rev-parse','HEAD'],target)==e['commit']
        assert len(list(target.glob('*.code-workspace')))==1
        cfg=json.loads((target/'simulation.json').read_text())
        for name in cfg['sources']+[cfg['testbench']]:
            assert (target/name).resolve().is_relative_to(target.resolve())
        provenance=json.loads((target/'evidence/source-provenance.json').read_text())
        for name,record in provenance['files'].items():
            assert hashlib.sha256((target/name).read_bytes()).hexdigest()==record['sha256'],name
        backup=ROOT/'tmp/pre-submodule-v2'/e['project']/'original'
        original_count=0
        if backup.exists():
            for original in backup.rglob('*'):
                if original.is_file():
                    assert original.read_bytes()==(target/'original'/original.relative_to(backup)).read_bytes()
                    original_count+=1
        log=command([sys.executable,'-X','utf8','tools/lab1.py','simulate'],target)
        assert 'LAB1_PASS ' in log
        assert not command(['git','status','--porcelain'],target)
        results.append({'project':e['project'],'commit':e['commit'],
                        'status':'PASS','original_files_equal':original_count,
                        'simulation':json.loads((target/'build/sim/result.json').read_text()),
                        'log':log})
        (LAB/'docs/submodule-validation.json').write_text(json.dumps({'results':results},indent=2)+'\n')
        print(e['project'],'fresh remote clone PASS',flush=True)
    assert len(results)==22


if __name__=='__main__':
    main()
