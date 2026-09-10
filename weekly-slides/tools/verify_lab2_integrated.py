"""Execute both independent integration projects, including their LCD bus."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def main():
    env=os.environ.copy()
    if Path('C:/msys64/mingw64/bin/iverilog.exe').exists():
        env['PATH']='C:/msys64/mingw64/bin'+os.pathsep+env.get('PATH','')
    reports=[]
    for edition in ['vivado_2026_1','opensource_cli']:
        project=LAB/edition/'09_integrated'
        shutil.copyfile(LAB/'common/tb_lab2_integrated.sv',project/'sim/tb_lab2_integrated.sv')
        result=subprocess.run([sys.executable,'-X','utf8','tools/lab1.py','simulate'],cwd=project,env=env,
                              capture_output=True,text=True,encoding='utf-8',timeout=45)
        state=json.loads((project/'build/sim/result.json').read_text(encoding='utf-8'))
        run=project/'build/sim'/state['run']
        compile_log=(run/'compile.log').read_text(encoding='utf-8')
        log=(run/'simulation.log').read_text(encoding='utf-8')
        assert result.returncode==0 and 'LAB2_INTEGRATED_PASS modes=8' in log,(edition,result.stdout,result.stderr)
        assert not compile_log, compile_log
        wave=(run/'wave.vcd').read_text(encoding='utf-8')
        stable=re.sub(r'\$date\b.*?\$end','',wave,flags=re.S)
        reports.append({'path':project.relative_to(LAB).as_posix(),'simulation_log':log,'inputs_sha256':state['inputs_sha256'],
                        'compile_log':compile_log,'wave_without_date_sha256':hashlib.sha256(stable.encode('utf-8')).hexdigest()})
        print(log,flush=True)
    assert reports[0]['inputs_sha256']==reports[1]['inputs_sha256']
    assert reports[0]['wave_without_date_sha256']==reports[1]['wave_without_date_sha256']
    (LAB/'docs/integrated-simulation-validation.json').write_text(json.dumps({
        'result':'PASS','scope':'two matching standalone projects; all eight modes, debounced buttons, LCD bus, reset, scan; no physical hardware execution',
        'projects':reports},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
