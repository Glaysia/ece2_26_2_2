"""Concrete student edits, tested against the unchanged self-check benches."""
from pathlib import Path
import hashlib, json, shutil, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'example/fpga_projects_hdl/LAB1'
# Full replacement expressions are verification data. Student slides describe
# the edit in words, retaining the course's screenshot-only HDL presentation.
EXERCISES = {
 'logic_gate': ('logic_gate.v', 'a ^ b', 'a | b', 'z의 XOR 연산자를 OR로 바꾼다.', 'a=b=1이면 z의 정상값은 0, 변경 후 값은 1이다.'),
 'full_adder': ('full_adder.v', 'carry_ab | carry_cin', 'carry_ab & carry_cin', 'cout의 OR 연산자를 AND로 바꾼다.', 'a=0, b=1, cin=1에서 정상 carry는 1이다. 변경 후 carry는 0이다.'),
 'adder_4bit': ('adder_4bit.v', "{1'b0,a} + {1'b0,b}", "{1'b0,a} - {1'b0,b}", '덧셈 연산자를 뺄셈으로 바꾼다.', 'a=0, b=1의 정상 결과는 carry=0, sum=1이다. 변경 후 carry=1, sum=15다.'),
 'sub_4bit': ('sub_4bit.v', 'a < b', 'a <= b', 'borrow 비교에 등호를 추가한다.', 'a=b=0이면 정상 borrow는 0이다. 변경 후에는 1이 된다.'),
 'compare_4': ('compare_4.v', 'a == b', 'a != b', '출력 가운데의 같음 비교를 다름 비교로 바꾼다.', 'a=b=0에서 정상 출력은 010이다. 변경 후에는 000이 된다.'),
 'mux_4x1': ('mux_4x1.v', 'i[3-s]', 'i[s]', '출력에 연결할 입력의 인덱스를 3-s에서 s로 바꾼다.', 'i=0001, s=00에서 정상 z=0이다. 변경 후에는 z=1이다.'),
 'demux_1x8': ('demux_1x8.v', '>> s', '<< s', '오른쪽 시프트를 왼쪽 시프트로 바꾼다.', 'i=1, s=1에서 정상 출력은 01000000이다. 변경 후에는 00000000이다.'),
 'encoder8x3': ('encoder8x3.v', "8'h01: a=7", "8'h01: a=6", '입력 00000001에 대응하는 출력 상수를 7에서 6으로 바꾼다.', '이 입력의 정상 출력은 111이다. 변경 후에는 110이다.'),
 'decoder3x8': ('decoder3x8.v', '<< {a,b,c}', '>> {a,b,c}', '왼쪽 시프트를 오른쪽 시프트로 바꾼다.', 'abc=001에서 정상 출력은 00000010이다. 변경 후에는 00000000이다.'),
 'seg_decoder': ('seg_decoder.v', "0:seg_data=8'hfc", "0:seg_data=8'h60", '숫자 0의 패턴을 1의 패턴으로 바꾼다.', 'bcd=0의 정상 출력은 FC다. 변경 후에는 60이다.'),
 'lab1_integrated': ('lab1_integrated.v', '(mode==9)?0:mode+1', '(mode==8)?0:mode+1', '버튼 처리의 모드 순환 비교값을 9에서 8로 바꾼다.', '내부 mode는 0부터 센다. 화면 MODE 09 다음에 MODE 10 대신 MODE 01로 돌아가면 실패다.'),
}

def main():
 projects=json.loads((LAB/'projects.json').read_text(encoding='utf-8'))
 records=[]
 for project in projects:
  if project['edition']!='vivado_2026_1': continue
  source=LAB/project['path']; config=json.loads((source/'simulation.json').read_text())
  filename,before,after,edit,expected=EXERCISES[project['top']]
  with tempfile.TemporaryDirectory(prefix='lab1-edit-') as tmp:
   tmp=Path(tmp)
   for rel in config['sources']+[config['testbench']]:
    target=tmp/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/rel,target)
   target=tmp/'src'/filename;original=target.read_bytes();text=original.decode()
   assert text.count(before)==1,(project['path'],before)
   runs=[]
   for phase in ['baseline','modified','restored']:
    target.write_bytes(text.replace(before,after).encode() if phase=='modified' else original)
    compile_result=subprocess.run(['C:/msys64/mingw64/bin/iverilog.exe','-g2012','-s',config['simulation_top'],'-o','simulation.vvp',*config['sources'],config['testbench']],cwd=tmp,capture_output=True,text=True,timeout=60)
    assert compile_result.returncode==0,compile_result.stderr
    run=subprocess.run(['C:/msys64/mingw64/bin/vvp.exe','simulation.vvp'],cwd=tmp,capture_output=True,text=True,timeout=60)
    assert (run.returncode!=0 and ('FAIL' in run.stdout or 'FATAL:' in run.stdout)) if phase=='modified' else (run.returncode==0 and 'LAB1_PASS' in run.stdout),(project['path'],phase,run.stdout)
    runs.append(dict(phase=phase,exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr,rtl_sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
   assert target.read_bytes()==original
   records.append(dict(project=project['path'],top=project['top'],file='src/'+filename,edit=edit,expected=expected,inputs_sha256={rel:hashlib.sha256((source/rel).read_bytes()).hexdigest() for rel in config['sources']+[config['testbench'],'simulation.json']},runs=runs))
   print(project['top']+': baseline PASS, change detected, restored PASS',flush=True)
 modern=LAB/'vivado_2026_1/11_integrated';cli=LAB/'opensource_cli/integrated'
 config=json.loads((modern/'simulation.json').read_text())
 assert all((modern/rel).read_bytes()==(cli/rel).read_bytes() for rel in config['sources']+[config['testbench']])
 out=LAB/'docs/student-modification-validation.json'
 out.write_text(json.dumps({'status':'PASS','projects':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()

