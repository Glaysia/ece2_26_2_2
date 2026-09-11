"""Publish already validated standalone instructor examples, never the template."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'example/fpga_projects_hdl/LAB1'


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True,
                          encoding='utf-8', errors='replace').stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('prepared', type=Path)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    prepared = args.prepared.resolve()
    projects = json.loads((LAB / 'projects.json').read_text(encoding='utf-8'))
    manifest = []
    for p in projects:
        target = prepared / p['id']
        provenance = json.loads((target / 'evidence/source-provenance.json').read_text(encoding='utf-8'))
        simulation = json.loads((target / 'evidence/standalone-simulation.json').read_text(encoding='utf-8'))
        assert simulation['status'] == 'SIMULATED'
        for name, record in provenance['files'].items():
            assert hashlib.sha256((target / name).read_bytes()).hexdigest() == record['sha256']
        assert len(list(target.glob('*.code-workspace'))) == 1
        attributes = target / '.gitattributes'
        preservation = '\n# Preserve instructor source and legacy archive bytes across platforms.\nsrc/** -text\nsim/** -text\nconstraints/** -text\noriginal/** -text\n'
        if 'original/** -text' not in attributes.read_text(encoding='utf-8'):
            with attributes.open('a', encoding='utf-8') as stream:
                stream.write(preservation)
        original = LAB / p['path'] / 'original'
        if original.is_dir():
            shutil.copytree(original, target / 'original', dirs_exist_ok=True)
        # Historical GUI/build evidence remains explicitly separate from the new run.
        old_evidence = LAB / p['path'] / 'evidence'
        if old_evidence.is_dir():
            shutil.copytree(old_evidence, target / 'evidence/historical-course', dirs_exist_ok=True)
        (target / 'evidence/README.md').write_text(
            '# 검증 근거\n\n'
            '`standalone-simulation.*`는 이 독립 예시를 Windows Icarus로 실행한 결과다. '
            '`source-provenance.json`은 원본 코드 경로와 해시다.\n\n'
            '`historical-course/`는 이전 강의 프로젝트에서 얻은 GUI·구현·DB 조사 기록이다. '
            '이 독립 clone에서 Vivado 또는 CLI bit를 다시 실행한 증거로 해석하지 않는다. '
            '기록 속 과거 경로·커밋은 당시 실행 환경을 나타낸다.\n', encoding='utf-8')
        name='fpga-lab-example-'+p['id'].replace('_','-')
        url='https://github.com/Glaysia/'+name+'.git'
        entry={'project':p['path'],'repository':url,'template_commit':provenance['template_commit']}
        if args.publish:
            run(['git','add','.'],target)
            if run(['git','diff','--cached','--name-only'],target):
                run(['git','commit','-m','Add independently simulated LAB1 instructor example'],target)
            remotes=run(['git','remote'],target).splitlines()
            if 'origin' not in remotes:
                run(['gh','repo','create','Glaysia/'+name,'--public','--source',str(target),
                     '--remote','origin','--description','LAB1 instructor example; students start from fpga-lab-template'],target)
            assert run(['git','remote','get-url','origin'],target).removesuffix('.git') == url.removesuffix('.git')
            run(['git','push','-u','origin','main'],target)
            entry['commit']=run(['git','rev-parse','HEAD'],target)
            assert run(['git','ls-remote','origin','refs/heads/main'],target).split()[0] == entry['commit']
            entry['status']='PUBLISHED'
        else:
            entry['status']='PREPARED'
        manifest.append(entry)
        (prepared/'publication-results.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        print(name,entry['status'],flush=True)
    assert len(manifest)==22


if __name__=='__main__':
    main()
