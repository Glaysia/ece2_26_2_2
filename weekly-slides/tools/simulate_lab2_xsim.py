"""Run the student's same nine modern testbenches in Vivado XSim without GUI."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'
BIN=Path('C:/AMDDesignTools/2026.1/Vivado/bin')

def main():
    records=[]
    for configfile in sorted((LAB/'vivado_2026_1').glob('*/simulation.json')):
        project=configfile.parent; config=json.loads(configfile.read_text(encoding='utf-8'))
        files=[project/name for name in config['sources']+[config['testbench']]]
        hashes={p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        run=ROOT/'tmp/lab2-xsim'/(project.name+'-'+str(time.time_ns())); run.mkdir(parents=True)
        commands=[['xvlog.bat','--sv',*map(str,files)],
                  ['xelab.bat',config['simulation_top'],'-s','lab2_snapshot'],
                  ['xsim.bat','lab2_snapshot','-runall','-log','simulation.log']]
        results=[]
        for command in commands:
            with (run/(Path(command[0]).stem+'-console.log')).open('w',encoding='utf-8') as log:
                result=subprocess.run([str(BIN/command[0]),*command[1:]],cwd=run,stdout=log,stderr=subprocess.STDOUT,timeout=180)
            results.append(result.returncode)
            if result.returncode: raise RuntimeError(f'{project.name}: {command[0]} failed in {run}')
        log=(run/'simulation.log').read_text(encoding='utf-8',errors='replace')
        marker=re.search(r'LAB2_(?:INTEGRATED_)?PASS[^\r\n]*',log)
        assert marker,(project.name,log)
        assert all(hashlib.sha256((project/name).read_bytes()).hexdigest()==value for name,value in hashes.items())
        record={'path':project.relative_to(LAB).as_posix(),'tool':'Vivado 2026.1 XSim','execution':'batch, no GUI',
                'status':'PASS','marker':marker[0],'commands_exit_code':results,'inputs_sha256':hashes,
                'run_directory':run.relative_to(ROOT).as_posix()}
        evidence=project/'evidence/xsim-batch'; evidence.mkdir(exist_ok=True)
        (evidence/'simulation.log').write_bytes((run/'simulation.log').read_bytes())
        (evidence/'validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        records.append(record)
        (LAB/'docs/xsim-batch-validation.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(project.name,marker[0],flush=True)

if __name__=='__main__': main()
