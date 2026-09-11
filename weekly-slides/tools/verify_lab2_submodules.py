"""Verify all published gitlinks and execute their actual fresh checkout directories."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def git(args,cwd):
    return subprocess.run(['git',*args],cwd=cwd,check=True,capture_output=True,text=True,encoding='utf-8').stdout.strip()

def main():
    env=os.environ.copy()
    if Path('C:/msys64/mingw64/bin/iverilog.exe').exists():
        env['PATH']='C:/msys64/mingw64/bin'+os.pathsep+env.get('PATH','')
    published=json.loads((LAB/'docs/example-repositories.json').read_text(encoding='utf-8'))
    assert len(published)==18
    reports=[]
    for entry in published:
        project=LAB/entry['project']; assert (project/'.git').is_file()
        assert git(['rev-parse','HEAD'],project)==entry['commit']
        assert git(['remote','get-url','origin'],project)==entry['repository']
        assert not git(['status','--porcelain'],project)
        index=git(['ls-files','--stage','--',project.relative_to(ROOT).as_posix()],ROOT).split()
        assert index[0]=='160000' and index[1]==entry['commit']
        proof=json.loads((project/'evidence/standalone-simulation.json').read_text(encoding='utf-8'))
        for name,digest in proof['input_sha256'].items():
            assert hashlib.sha256((project/name).read_bytes()).hexdigest()==digest,(entry['project'],name)
        config=json.loads((project/'simulation.json').read_text(encoding='utf-8'))
        for name in config['sources']+[config['testbench']]:
            assert (project/name).resolve().is_relative_to(project.resolve())
        result=subprocess.run([sys.executable,'-X','utf8','tools/lab1.py','simulate'],cwd=project,env=env,
                              capture_output=True,text=True,encoding='utf-8',timeout=45)
        state=json.loads((project/'build/sim/result.json').read_text(encoding='utf-8'))
        log=(project/'build/sim'/state['run']/'simulation.log').read_text(encoding='utf-8')
        marker=re.search(r'LAB2_(?:INTEGRATED_)?PASS[^\r\n]*',log)
        assert result.returncode==0 and marker,(entry['project'],result.stdout,result.stderr)
        assert not git(['status','--porcelain'],project)
        reports.append({'path':entry['project'],'commit':entry['commit'],'repository':entry['repository'],
                        'status':'PASS','marker':marker[0],'inputs_sha256':state['inputs_sha256'],'simulation_log':log})
        print(entry['project'],marker[0],flush=True)
    (LAB/'docs/fresh-submodule-validation.json').write_text(json.dumps({'status':'PASS',
        'execution':'Actual freshly cloned submodule directories; pinned commit, source bytes, direct simulation and clean Git status',
        'projects':reports},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
