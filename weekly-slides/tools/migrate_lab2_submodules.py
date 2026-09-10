"""Replace prepared example folders with published submodules, retaining local backups."""
from pathlib import Path
import json
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def run(args,cwd=ROOT):
    return subprocess.run(args,cwd=cwd,check=True,capture_output=True,text=True,encoding='utf-8',errors='replace').stdout.strip()

def main():
    publications=json.loads((LAB/'docs/example-repositories.json').read_text(encoding='utf-8'))
    assert len(publications)==18 and all(p['status']=='PUBLISHED' for p in publications)
    backups=(ROOT/'tmp'/('lab2-before-submodules-'+str(time.time_ns()))).resolve()
    backups.mkdir(parents=True)
    results=[]
    for record in publications:
        source=(LAB/record['project']).resolve()
        backup=(backups/record['project']).resolve()
        # Validate both absolute paths before any recursive directory move.
        assert source.is_relative_to(LAB.resolve()) and source!=LAB.resolve()
        assert backup.is_relative_to(backups) and backup!=backups
        relative=source.relative_to(ROOT).as_posix()
        if (source/'.git').exists():
            assert run(['git','remote','get-url','origin'],source)==record['repository']
            assert run(['git','rev-parse','HEAD'],source)==record['commit']
        else:
            assert source.is_dir()
            backup.parent.mkdir(parents=True,exist_ok=True)
            # Only remove the old files from the parent index; preserve every local byte.
            run(['git','rm','-r','--cached','--ignore-unmatch','--',relative])
            shutil.move(str(source),str(backup))
            name='lab2-'+record['project'].replace('/','-').replace('_','-')
            run(['git','submodule','add','--name',name,'--',record['repository'],relative])
            run(['git','checkout','--detach',record['commit']],source)
            run(['git','add','--',relative])
        assert run(['git','rev-parse','HEAD'],source)==record['commit']
        assert not run(['git','status','--porcelain'],source)
        results.append({'path':relative,'commit':record['commit'],'backup':backup.relative_to(ROOT).as_posix(),
                        'status':'SUBMODULE'})
        (LAB/'docs/submodule-migration.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(relative,'SUBMODULE',flush=True)

if __name__=='__main__': main()
