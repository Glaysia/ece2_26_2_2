"""Verify the integration manual's counter edit and exact-byte restoration."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def main():
    env=os.environ.copy()
    if Path('C:/msys64/mingw64/bin/iverilog.exe').exists():
        env['PATH']='C:/msys64/mingw64/bin'+os.pathsep+env.get('PATH','')
    reports=[]
    for edition in ['vivado_2026_1','opensource_cli']:
        source=LAB/edition/'09_integrated'
        baseline=json.loads((source/'evidence/standalone-simulation.json').read_text(encoding='utf-8'))
        assert all(hashlib.sha256((source/name).read_bytes()).hexdigest()==digest for name,digest in baseline['input_sha256'].items())
        record={'path':source.relative_to(LAB).as_posix(),'baseline_log':baseline['simulation_log'],
                'edit':'counter4.v: increment 1 -> 2; leave TB expectations unchanged','runs':[]}
        with tempfile.TemporaryDirectory(prefix='lab2-integrated-edit-') as temporary:
            project=Path(temporary)/'project'
            shutil.copytree(source,project,ignore=shutil.ignore_patterns('build','.git','vivado'))
            rtl=project/'src/counter4.v'; original=rtl.read_bytes()
            assert original.count(b"value + 4'd1")==1
            for stage in ['changed','restored']:
                rtl.write_bytes(original.replace(b"value + 4'd1",b"value + 4'd2") if stage=='changed' else original)
                result=subprocess.run([sys.executable,'-X','utf8','tools/lab1.py','simulate'],cwd=project,env=env,
                                      capture_output=True,text=True,encoding='utf-8',timeout=45)
                state=json.loads((project/'build/sim/result.json').read_text(encoding='utf-8'))
                log=(project/'build/sim'/state['run']/'simulation.log').read_text(encoding='utf-8')
                if stage=='changed':
                    assert result.returncode!=0 and 'LAB2_INTEGRATED_FAIL counter increments once' in log
                    assert not (project/'build/sim/wave.vcd').exists()
                else:
                    assert result.returncode==0 and 'LAB2_INTEGRATED_PASS modes=8 checks=2848' in log
                    assert rtl.read_bytes()==original
                record['runs'].append({'stage':stage,'exit_code':result.returncode,'simulation_log':log,
                                       'rtl_sha256':hashlib.sha256(rtl.read_bytes()).hexdigest()})
                print(edition,stage,'expected outcome',flush=True)
        reports.append(record)
    (LAB/'docs/integrated-modification-validation.json').write_text(json.dumps({'status':'PASS','projects':reports},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
