"""Publish validated instructor examples; the single-project student template is untouched."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def run(args,cwd,check=True):
    return subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',check=check)

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--publish',action='store_true')
    parser.add_argument('--prepared',type=Path)
    args=parser.parse_args()
    prepared=args.prepared.resolve() if args.prepared else ROOT/'tmp'/('lab2-publish-'+str(time.time_ns()))
    prepared.mkdir(parents=True,exist_ok=True)
    records=[]
    for entry in json.loads((LAB/'projects.json').read_text(encoding='utf-8')):
        assert re.fullmatch(r'[a-z0-9_]+',entry['id'])
        source=(LAB/entry['path']).resolve(); assert source.is_relative_to(LAB.resolve())
        proof=json.loads((source/'evidence/standalone-simulation.json').read_text(encoding='utf-8'))
        assert proof['status']=='PASS'
        for name,expected in proof['input_sha256'].items(): assert digest(source/name)==expected,(entry['id'],name)
        assert digest(source/entry['constraints'])==proof['constraints_sha256']
        assert digest(source/'LAB1.code-workspace')==proof['workspace_sha256']
        target=prepared/entry['id']
        if not target.exists():
            shutil.copytree(source,target,ignore=shutil.ignore_patterns('build','vivado','.git'))
            run(['git','init','-b','main'],target)
        else:
            raise RuntimeError('Prepared project already exists; inspect before reusing: '+str(target))
        slug=entry['id'].replace('vivado_2026_1','vivado').replace('opensource_cli','cli').replace('_','-')
        repository='Glaysia/fpga-lab2-example-'+slug
        url='https://github.com/'+repository+'.git'
        run(['git','add','.'],target)
        run(['git','commit','-m','Add independently simulated LAB2 instructor example'],target)
        record={'project':entry['path'],'repository':url,'prepared':target.relative_to(ROOT).as_posix(),
                'commit':run(['git','rev-parse','HEAD'],target).stdout.strip(),'status':'PREPARED'}
        if args.publish:
            existing=run(['gh','repo','view',repository,'--json','nameWithOwner'],target,check=False)
            if existing.returncode==0:
                assert json.loads(existing.stdout)['nameWithOwner'].lower()==repository.lower()
                run(['git','remote','add','origin',url],target)
            else:
                if 'Could not resolve to a Repository' not in existing.stderr and 'Not Found' not in existing.stderr:
                    raise RuntimeError(existing.stderr)
                run(['gh','repo','create',repository,'--public','--source',str(target),'--remote','origin',
                     '--description','LAB2 instructor example; students author RTL from the single fpga-lab-template v2.0.0'],target)
            run(['git','push','-u','origin','main'],target)
            remote=run(['git','ls-remote','origin','refs/heads/main'],target).stdout.split()[0]
            assert remote==record['commit']
            record['status']='PUBLISHED'
        records.append(record)
        (prepared/'publication-results.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if args.publish:
            (LAB/'docs/example-repositories.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(repository,record['status'],flush=True)

if __name__=='__main__': main()
