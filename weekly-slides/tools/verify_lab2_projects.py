"""Fresh-directory simulations of all 18 independent LAB2 example projects."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    env=os.environ.copy()
    if Path('C:/msys64/mingw64/bin/iverilog.exe').exists():
        env['PATH']='C:/msys64/mingw64/bin'+os.pathsep+env.get('PATH','')
    projects=json.loads((LAB/'projects.json').read_text(encoding='utf-8'))
    assert len(projects)==18 and len({p['path'] for p in projects})==18
    reports=[]
    for entry in projects:
        source=LAB/entry['path']
        workspace=json.loads((source/'LAB1.code-workspace').read_text(encoding='utf-8'))
        assert len(workspace['folders'])==1 and workspace['folders'][0]['path']=='.'
        assert set(workspace['extensions']['recommendations'])=={
            'hudson-river-trading.vscode-slang','lramseyer.vaporview','tomoki1207.pdf'}
        assert len(workspace['tasks']['tasks'])==3
        with tempfile.TemporaryDirectory(prefix='lab2-independent-') as temporary:
            project=Path(temporary)/source.name
            shutil.copytree(source,project,ignore=shutil.ignore_patterns('build','.git','vivado'))
            config=json.loads((project/'simulation.json').read_text(encoding='utf-8'))
            for path in config['sources']+[config['testbench']]:
                assert (project/path).resolve().is_relative_to(project.resolve())
            result=subprocess.run([sys.executable,'-X','utf8','tools/lab1.py','simulate'],cwd=project,env=env,
                                  capture_output=True,text=True,encoding='utf-8',timeout=45)
            state=json.loads((project/'build/sim/result.json').read_text(encoding='utf-8'))
            run=project/'build/sim'/state['run']
            log=(run/'simulation.log').read_text(encoding='utf-8')
            assert result.returncode==0 and re.search(r'LAB2_(?:INTEGRATED_)?PASS\b',log),(entry['path'],result.stdout,result.stderr)
            assert not (run/'compile.log').read_text(encoding='utf-8')
            report={'path':entry['path'],'status':'PASS','execution':'fresh temporary directory; standalone CLI simulation',
                    'simulation_log':log,'input_sha256':state['inputs_sha256'],
                    'workspace_sha256':digest(project/'LAB1.code-workspace'),'constraints_sha256':digest(project/entry['constraints'])}
            if not (source/'.git').exists():
                (source/'evidence/standalone-simulation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            reports.append(report)
            print(entry['path'],'PASS',flush=True)
    (LAB/'docs/18-project-simulation-validation.json').write_text(json.dumps({'status':'PASS','projects':reports},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
