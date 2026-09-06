"""Check snapshot provenance and record hashes for the report evidence."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
source = root.parent / 'src'
for n in range(16, 22):
    for path in (root / 'simulation' / f'exp{n}').iterdir():
        if path.suffix not in ('.v', '.sv'):
            continue
        expected = (source / path.name).read_text(encoding='utf-8-sig')
        if path.name == 'top_main.v':
            expected = expected.replace('    parameter integer EXPERIMENT = 16,',
                                        f'    parameter integer EXPERIMENT = {n},', 1)
        assert path.read_text(encoding='utf-8-sig').rstrip() == expected.rstrip(), path
files = sorted(p for p in (root / 'simulation').glob('exp*/*')
               if p.is_file() and p.suffix in ('.v', '.sv', '.vcd', '.txt'))
out = {
    'source_base_commit': '944f2436e3bd9663a32b4295a8d292b62b327936',
    'snapshot_change': 'Only active EXPERIMENT value changed per execution; line endings, BOM and trailing blank lines may differ.',
    'sha256': {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
}
(root / 'simulation' / 'manifest.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
print(f'All six source snapshots match src, with only the experiment selector changed. Hashed {len(files)} files.')
