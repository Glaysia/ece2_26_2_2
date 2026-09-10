"""Run each standalone lesson and a targeted student edit in an isolated copy."""
from pathlib import Path
from datetime import datetime, timezone
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
EDITS={
    'counter4': ('value + 4\'d1', 'value + 4\'d2', '증가량을 1에서 2로 바꾸기'),
    'clock_divider': ('DIVISOR/2 - 1', 'DIVISOR/2', '출력의 첫 전이를 한 클록 늦추기'),
    'register_pair': ('value <= stored;', 'value <= data_in;', '이전 저장값 대신 현재 입력 전달하기'),
    'shift_register4': ('{serial_in, value[3:1]}', '{value[2:0], serial_in}', '시프트 방향 반대로 바꾸기'),
    'piso4': ('assign serial_out = value[3];', 'assign serial_out = value[0];', 'MSB 대신 LSB 출력하기'),
    'moore_cycle': ("2'b01: value <= 2'b10;", "2'b01: value <= 2'b00;", 'S1 다음 상태를 S0로 바꾸기'),
    'mealy_toggle': ("(state ? 2'b01 : 2'b10)", "(state ? 2'b10 : 2'b01)", '두 상태의 입력 1 출력을 서로 바꾸기'),
    'segment_scan8': ("blank ? 8'h00 : (8'h01 << index)", "8'h01 << index", '자리 전환 blanking 제거하기'),
}

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    env=os.environ.copy()
    if Path('C:/msys64/mingw64/bin/iverilog.exe').exists():
        env['PATH']='C:/msys64/mingw64/bin'+os.pathsep+env.get('PATH','')
    manifest=json.loads((LAB/'circuits.json').read_text(encoding='utf-8'))
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'execution':'CLI, no GUI actions',
            'scope':'8 functional cores; no board wrapper, XDC, Vivado or hardware validation',
            'iverilog':subprocess.run(['iverilog','-V'],env=env,capture_output=True,text=True).stdout.splitlines()[0],
            'projects':[]}
    with tempfile.TemporaryDirectory(prefix='lab2-core-check-') as temporary:
        for entry in manifest:
            source=LAB/entry['path']
            project=Path(temporary)/source.name
            shutil.copytree(source,project,ignore=shutil.ignore_patterns('build','.git'))
            top=entry['top']
            rtl=project/'src'/f'{top}.v'
            original=rtl.read_bytes()
            before,after,instruction=EDITS[top]
            content=original.decode('utf-8')
            assert content.count(before)==1, (top,before)
            record={'path':entry['path'],'top':top,'edit':instruction,
                    'inputs_sha256':{p.relative_to(source).as_posix():digest(p) for p in source.rglob('*')
                                     if p.is_file() and 'build' not in p.relative_to(source).parts},'runs':[]}
            for stage in ['baseline','changed','restored']:
                rtl.write_bytes(content.replace(before,after).encode('utf-8') if stage=='changed' else original)
                result=subprocess.run([sys.executable,'-X','utf8','tools/lab1.py','simulate'],
                                      cwd=project,env=env,capture_output=True,text=True,encoding='utf-8',timeout=45)
                runner=json.loads((project/'build/sim/result.json').read_text(encoding='utf-8'))
                runfolder=project/'build/sim'/runner['run']
                log=(runfolder/'simulation.log').read_text(encoding='utf-8')
                compile_log=(runfolder/'compile.log').read_text(encoding='utf-8')
                wave_text=(runfolder/'wave.vcd').read_text(encoding='utf-8')
                stable_wave=re.sub(r'\$date\b.*?\$end', '', wave_text, flags=re.S)
                if stage=='changed':
                    assert result.returncode!=0 and 'LAB2_FAIL' in log and 'LAB2_PASS' not in log, (top,stage,log)
                    assert not (project/'build/sim/wave.vcd').exists(), 'failed run published stale waveform'
                else:
                    assert result.returncode==0 and re.search(rf'LAB2_PASS {top} checks=\d+',log), (top,stage,result.stdout,result.stderr)
                    assert runner['status']=='SIMULATED'
                record['runs'].append({'stage':stage,'exit_code':result.returncode,
                                       'log':log,'compile_log':compile_log,
                                       'rtl_sha256':digest(rtl),'wave_sha256':runner.get('wave_sha256')})
                record['runs'][-1]['wave_without_date_sha256']=hashlib.sha256(stable_wave.encode('utf-8')).hexdigest()
                print(top,stage,result.returncode,flush=True)
            assert rtl.read_bytes()==original
            assert record['runs'][0]['wave_without_date_sha256']==record['runs'][2]['wave_without_date_sha256'], 'restored trace differs'
            report['projects'].append(record)
    report['result']='PASS: 8 baseline + 8 changed failures + 8 restored'
    out=LAB/'docs/core-simulation-validation.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(report['result'])

if __name__=='__main__': main()
