"""Crop observed VS Code screenshots and describe their teaching use.

Only crops original screen pixels. No source text is rendered into these images.
Run before lab1_series.py when the locally retained PNG captures are available.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'example/fpga_projects_hdl/LAB1'
ASSETS = ROOT / 'weekly-slides/weekly-slides/LAB1_FPGA_0914/assets/lab1-circuits'
PANELS = []

def add(source, capture, suffix, lines, box, title, *notes):
    PANELS.append(dict(source='common/'+source, capture=capture+'.png',
                       image=Path(source).stem+'-'+suffix+'.png', lines=lines,
                       crop_box=box, title=title, notes=list(notes)))

for module, end, right in [('mux_4x1',4,850),('demux_1x8',4,870),
                           ('encoder8x3',10,960),('decoder3x8',3,725),
                           ('seg_decoder',12,960)]:
    add('rtl/'+module+'.v',module+'-rtl-full','rtl-crop',[1,end],
        [65,89,right,114+24*(end-1)],'RTL 구조를 설명한다')

TB_NOTES = {
 'tb_logic_gate': 'a·b의 00, 01, 10, 11을 순서대로 넣고 AND·OR·XOR 세 출력을 묶어 비교한다.',
 'tb_full_adder': 'a·b·cin의 8개 조합을 만든다. 정수 덧셈으로 기대값을 구하고 carry와 sum을 함께 비교한다.',
 'tb_adder_4bit': 'n/16은 a, n%16은 b다. 16×16개 조합의 합을 5비트 기대값에 담아 carry까지 검사한다.',
 'tb_sub_4bit': '상위 비트에는 a<b인 경우의 borrow를 넣고, 하위 4비트에는 차의 하위 4비트를 넣는다. a=b도 포함한다.',
 'tb_compare_4': 'a>b, a=b, a<b일 때 기대값을 각각 100, 010, 001로 만든다. 256개 조합을 검사한다.',
 'tb_mux_4x1': '입력 i의 16개 값과 선택선 s의 4개 값을 조합한다. s=0이 i[3]을 고르는 순서에 주의한다.',
 'tb_demux_1x8': '입력 i가 0이면 모든 출력은 0이다. i가 1이면 선택선에 따라 10000000을 오른쪽으로 이동한다.',
 'tb_encoder8x3': '8개 one-hot 입력뿐 아니라 256개 입력을 모두 넣는다. 1이 없거나 여러 개인 입력의 기대값은 000이다.',
 'tb_decoder3x8': 'abc를 000부터 111까지 바꾼다. 1을 입력값만큼 왼쪽으로 옮겨 기대 출력의 위치를 정한다.',
}
for name, note in TB_NOTES.items():
    split,end=(13,23) if name=='tb_encoder8x3' else (12,22)
    # First panel ends immediately before the output comparison; second keeps
    # the complete failure message and watchdog visible.
    add('tb/'+name+'.sv',name+'-full','input',[1,split],
        [65,89,1040 if name=='tb_full_adder' else 850,114+24*(split-1)],
        'TB · 입력과 기대값',note,'DUT는 검사할 회로다. dumpfile·dumpvars는 파형 파일에 신호를 남긴다.')
    add('tb/'+name+'.sv',name+'-full','check',[split+1,end],
        [65,90+24*split,1040,114+24*(end-1)],
        'TB · 비교와 종료',
        '!==는 X·Z를 포함한 불일치도 잡는다. 다르면 $fatal로 중단하고 어떤 입력에서 틀렸는지 출력한다.',
        'checked가 전체 검사 수와 같은지 확인한 뒤 PASS와 $finish. watchdog은 종료되지 않는 테스트를 실패시킨다.')

add('tb/tb_seg_decoder.sv','tb_seg_decoder-top','setup',[1,7],[65,89,1070,258],
    'TB · 7세그먼트 검사 준비','입력은 4비트, 출력은 8비트다. digits 배열에 0–F의 기대 점등 패턴을 저장한다.')
for suffix, first,last in [('digits0',8,15),('digits8',16,23)]:
    add('tb/tb_seg_decoder.sv','tb_seg_decoder-top',suffix,[first,last],
        [65,90+24*(first-1),390,114+24*(last-1)],
        'TB · 기대 점등 패턴 '+('0–7' if first==8 else '8–F'),
        '배열 값은 a–dp 순서의 8비트 패턴이다. 1은 점등, 마지막 dp 비트는 0이다.',
        '예를 들어 0은 FC=11111100, 8은 FE=11111110이다. 점등할 선분과 직접 대조한다.')
add('tb/tb_seg_decoder.sv','tb_seg_decoder-bottom','compare',[24,31],[65,287,1050,479],
    'TB · 16개 패턴 비교','0부터 F까지 입력하고 10ns 뒤 기대 배열 값과 출력을 비교한다. 불일치 시 입력과 두 값을 출력한다.')
add('tb/tb_seg_decoder.sv','tb_seg_decoder-bottom','finish',[32,37],[65,479,735,624],
    'TB · 완료 판정','16개를 모두 검사한 경우에만 PASS를 출력한다. 정상 종료는 160ns이고 watchdog은 100,000ns다.')

# Each integrated image is split at a meaningful source boundary.
add('rtl/lab1_integrated.v','lab1_integrated-rtl-top','mode',[1,11],[65,89,975,354],
    '통합 RTL · 모드 번호','기본값은 디바운스 20클록·LCD 대기 50클록이다. 입력 클록은 보드의 1kHz다.',
    'reset은 mode=0, 버튼 펄스는 다음 모드로 이동한다. 내부 번호 0–9는 LCD의 01–10에 대응한다.')
add('rtl/lab1_integrated.v','lab1_integrated-rtl-top','circuits-a',[12,18],[65,354,825,522],
    '통합 RTL · 논리·가산 연결','공유 RTL의 논리 게이트·전가산기·4비트 가산기를 인스턴스화한다. DIP 입력에서 필요한 비트를 연결한다.')
add('rtl/lab1_integrated.v','lab1_integrated-rtl-top','circuits-b',[19,25],[65,522,825,691],
    '통합 RTL · 나머지 회로 연결','감산·비교·MUX·DEMUX·인코더·디코더·7세그먼트도 같은 입력 스위치를 사용한다.',
    '모든 회로는 함께 동작하며, 다음 코드에서 현재 모드의 출력을 선택한다.')
add('rtl/lab1_integrated.v','lab1_integrated-rtl-bottom','outputs-a',[26,34],[65,167,740,383],
    '통합 RTL · 출력 선택 01–05','7세그먼트는 mode=9에서만 켠다. LED 기본값을 0으로 두고 모드별 결과를 지정한다.',
    '비트 묶음의 왼쪽이 led[7]이며 보드 LED1에 연결된다. 남는 비트는 0으로 채운다.')
add('rtl/lab1_integrated.v','lab1_integrated-rtl-bottom','outputs-b',[35,44],[65,383,955,624],
    '통합 RTL · 출력 선택 06–10','MUX부터 7세그먼트까지 출력 선택을 마친다. LCD에는 같은 mode를 전달해 회로 이름을 표시한다.')
add('rtl/button_onepulse.v','button_onepulse-rtl-full','sync',[1,9],[65,89,770,306],
    '버튼 RTL · 두 단계 동기화','외부 버튼을 sync1, sync2 두 플립플롭을 거쳐 받는다. ASYNC_REG 속성으로 동기화 레지스터임을 표시한다.')
add('rtl/button_onepulse.v','button_onepulse-rtl-full','debounce',[10,20],[65,306,770,571],
    '버튼 RTL · 한 번만 전환','입력이 accepted와 다르게 20클록 유지되면 새 상태를 받아들인다. 그 전에는 연속 안정 시간을 센다.',
    'pulse의 기본값은 0이고 누름을 받아들일 때만 1이다. 뗄 때는 상태만 바뀌어 모드를 넘기지 않는다.')
LCD = [
 ('ports','top',1,11,[65,89,960,354],'LCD RTL · 포트와 상태','phase는 한 바이트의 전송 단계, index는 화면 내 위치다. shown_mode는 현재 화면의 모드다.'),
 ('names','top',12,21,[65,354,925,594],'LCD RTL · 회로명 선택','shown_mode에 따라 16문자 회로명을 고른다. 남는 자리는 공백으로 채운다.'),
 ('reset','top',22,26,[65,594,960,714],'LCD RTL · 리셋과 전원 대기','리셋 때 모든 상태와 출력 신호를 초기화한다. 1kHz에서 POWER_WAIT=50은 50ms 대기다.'),
 ('init','middle',27,34,[65,203,830,395],'LCD RTL · 초기 명령','38을 세 번 보낸 뒤 0C, 06으로 초기화한다. 첫 줄 주소 80을 보낼 때 mode를 shown_mode에 저장한다.'),
 ('heading','middle',35,42,[65,395,960,587],'LCD RTL · MODE 01–10','문자 MODE와 두 자리 번호를 보낸다. 내부 mode=9만 10으로 표시하고, 그다음 C0으로 둘째 줄을 선택한다.'),
 ('characters','middle',43,49,[65,587,900,756],'LCD RTL · 이름의 한 글자','index=23–38에서 128비트 이름을 8비트씩 꺼낸다. 나머지 첫 줄 위치는 공백으로 채운다.'),
 ('enable','bottom',50,60,[65,359,960,624],'LCD RTL · E 펄스와 반복','phase 1에서 E를 올리고 phase 2에서 내린다. 1kHz이므로 E high는 1ms다.',),
]
for suffix,cap,first,last,box,title,note in LCD:
    add('rtl/lcd_modes.v','lcd_modes-rtl-'+cap,suffix,[first,last],box,title,note,
        '첫 초기 명령 뒤에는 추가 대기한다. 한 화면이 끝나면 index=5로 돌아가 모드를 새로 저장한다.' if suffix=='enable' else '한 화면을 전송하는 동안 shown_mode를 유지하여 두 줄의 모드가 섞이지 않게 한다.')

ITB = [
 ('setup','top',1,13,[65,89,870,402],'통합 TB · 검사 환경','10ns 클록과 짧은 디바운스·전원 대기로 기능 검사를 빠르게 한다. 실제 합성의 1kHz 설정과 구분한다.'),
 ('tasks','top',14,22,[65,402,950,618],'통합 TB · 반복 동작','cycles는 클록 하강까지 기다리고 assert_mode는 모드 번호를 검사한다. press_once는 눌렀다 떼는 한 번의 동작이다.'),
 ('lcd-command','lcd',23,32,[65,93,1165,357],'통합 TB · LCD 명령 검사','실제 출력 lcd_e의 하강에서 lcd_rw와 초기 명령을 검사한다. 주소 80·C0을 만나면 해당 줄 조립을 시작한다.'),
 ('lcd-frame','lcd',33,41,[65,357,820,574],'통합 TB · 완성된 화면','주소에 따라 받은 문자를 16문자 버퍼에 넣는다. 둘째 줄 마지막 문자까지 받은 순간 완성된 두 줄을 보관한다.'),
 ('reset-bounce','vectors',42,52,[65,117,1165,381],'통합 TB · 리셋과 바운스','기대 LCD 명령·숫자 패턴을 준비한다. 1클록 누름과 2클록 뗌을 반복해도 mode=0인지 확인한다.'),
 ('expect-a','vectors',53,60,[65,381,840,573],'통합 TB · 모드별 입력','10개 모드 각각에서 DIP 256개를 모두 넣는다. 출력의 비트 배치까지 포함하여 별도 기대값을 계산한다.'),
 ('expect-b','vectors',61,68,[65,573,880,765],'통합 TB · 경계와 선택 순서','감산 borrow, 비교 결과, 선택선 순서, 인코더의 비정상 입력까지 기대값에 반영한다.'),
 ('compare','text',69,79,[65,213,1035,478],'통합 TB · 출력과 모드 번호','LED·7세그먼트를 매 입력마다 비교한다. 화면 갱신을 기다린 뒤 LCD 첫 줄의 MODE 번호와 초기화 횟수를 검사한다.'),
 ('name','text',80,87,[65,478,1120,670],'통합 TB · 회로명 대조','두 번째 줄은 16문자 전체를 해당 모드의 기대 회로명과 비교한다. 번호만 맞고 이름이 틀린 오류도 잡는다.'),
 ('finish','bottom',88,99,[65,335,1120,624],'통합 TB · 길게 누름·순환·복귀','80클록 동안 눌러도 한 번만 넘어가는지, 10→01 순환과 재리셋 후 LCD 복구를 검사한다.'),
]
for suffix,cap,first,last,box,title,note in ITB:
    add('tb/tb_lab1_integrated.sv','tb_lab1_integrated-'+cap,suffix,[first,last],box,title,note,
        '2,560개 출력과 10개 이상 화면을 확인한 뒤 PASS를 출력한다. 외부 보드의 실제 동작은 별도 실험이다.' if suffix=='finish' else '실험 전 레포트에는 이 코드의 역할과 자신의 실행 로그·파형을 함께 설명한다.')

def main():
    from PIL import Image
    records=json.loads((ASSETS/'provenance.json').read_text(encoding='utf-8'))
    records=[r for r in records if 'image' not in r]
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    for panel in PANELS:
        original=ASSETS/panel['capture']; output=ASSETS/panel['image']; source=LAB/panel['source']
        with Image.open(original) as screen:
            assert screen.size==(1202,801),(original,screen.size)
            screen.crop(panel['crop_box']).save(output)
        records.append({**panel,'capture_date':'2026-09-10','method':'Actual VS Code window via computer-use; crop only',
                        'full_capture_sha256':digest(original),'crop_sha256':digest(output),'source_sha256':digest(source)})
    for source in {p['source'] for p in PANELS}:
        line_count=len((LAB/source).read_text(encoding='utf-8').splitlines())
        covered=[n for p in PANELS if p['source']==source for n in range(p['lines'][0],p['lines'][1]+1)]
        assert sorted(covered)==list(range(1,line_count+1)),(source,'Missing or repeated source line')
    (ASSETS/'provenance.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(PANELS)} actual code panels prepared')

if __name__=='__main__':main()
