"""Shift-register teaching pages backed by actual editor captures.

Vivado GUI captures include XSim, pins, synthesis, implementation and bitstream.
"""
import json
from PIL import Image
from lab2_series import LAB, BASE, Deck, setup, code, gui, paras, steps, table


def make(p):
    project = LAB / p['path']
    config = json.loads((project / 'simulation.json').read_text('utf-8'))
    d = Deck(p['id'])

    def shot(title, name, caption, box=None, common=False):
        folder = 'divider-0913' if common else 'shift-0913'
        trim = ''
        if box:
            x1, y1, x2, y2 = box
            with Image.open(BASE / 'assets' / folder / (name+'.png')) as im:
                width, height = im.size
            assert 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height
            trim = ',trim='+' '.join(f'{v*.75:g}bp' for v in [x1,height-y2,width-x2,y1])+',clip'
        d.frame(title, r'\includegraphics[width=\textwidth,height=4.8cm,keepaspectratio'+trim+r']{assets/'+folder+'/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

    def workspace(title, name, caption, box=None):
        shot(title, name, caption+' 화면은 v2.0.0 빈 템플릿의 공통 예시다. v2.0.1에서도 여는 방법은 같고 .slang 설정이 추가되어 있다.', box, True)

    d.frame('LAB 2 · 시프트 레지스터', paras('작성일 2026. 09. 13. · 이해리', '빈 템플릿 → 직접 작성 → Icarus 시뮬레이션 → Vivado 구현'))
    d.frame('목차', r'\navlink{setup}{프로젝트 시작}\par\vspace{0.3cm}\navlink{code}{RTL·TB·XDC 작성}\par\vspace{0.3cm}\navlink{simulation}{VS Code 실행과 파형}\par\vspace{0.3cm}\navlink{reports}{실험 전 레포트}\par\vspace{0.3cm}\navlink{implementation}{Vivado 구현}\par\vspace{0.3cm}\navlink{after-report}{실험 후 레포트}', 'lab2-contents')
    setup(d, p, project, config, workspace_shot=workspace)
    d.frame('한 비트씩 받아 네 비트를 기억한다', paras('value[3:0]은 네 비트를 저장한다. enable=1인 clk 상승 에지마다 serial_in을 value[3]에 넣는다.', '이전 value[3], value[2], value[1]은 각각 value[2], value[1], value[0]으로 이동한다. 이전 value[0]은 버린다.', 'rst=1이면 0으로 초기화한다. rst=0, enable=0이면 입력이 변해도 저장값을 유지한다.'), 'code')
    d.frame('다음 상태를 먼저 계산', table(['rst','enable','다음 value[3:0]'], [('1','무관','0000'),('0','0','이전 value 유지'),('0','1','{serial_in, 이전 value[3:1]}')])+paras('예: value=0100, serial_in=1이면 다음 value=1010이다. 시프트 방향을 화면의 좌우가 아닌 비트 번호로 설명한다.'))
    d.frame('중괄호와 nonblocking 대입', paras('{serial_in, value[3:1]}은 1비트와 3비트를 이어 붙인 4비트다. 덧셈이나 네 번의 순차 실행이 아니다.', 'value <= ...의 오른쪽은 상승 에지 직전 저장값에서 계산한다. 네 비트는 같은 에지의 nonblocking 갱신으로 바뀐다.', '한 에지에 입력 비트가 모든 단계를 통과하지 않는다. 네 번 enable이 걸려야 입력 이력이 네 단계에 채워진다.'))
    for name in config['sources']:
        code(d, project, name)
    d.frame('버튼 한 번이 한 단계가 되도록', paras('input_frontend는 비동기 입력을 주 클록에 동기화하고 버튼이 20회 연속 안정된 뒤 한 클록의 press를 만든다.', '1 kHz 주 클록에서 20샘플은 20 ms다. 버튼을 누르고 놓는 한 동작이 enable 한 번이 된다.', 'ASYNC_REG는 동기화 레지스터를 도구에 알리는 속성이다. 버튼 디바운스는 별도의 안정 시간 검사 로직이 수행한다.'))
    d.frame('보드 연결과 스위치 순서', table(['항목','역할'], [('B6 / clk','1 kHz 주 클록'),('K4 / rst','네 비트 초기화'),('N8 / button','한 단계 시프트'),('DIP SW1 / sw[7]','serial_in'),('LED[3:0]','value[3:0]'),('LED[7:4]','항상 0000')])+paras('DIP SW1–SW8은 sw[7]–sw[0] 순서다. SW1을 정한 뒤 입력이 안정되면 N8을 누르고 놓는다.'))
    d.frame('테스트벤치의 여덟 검사', table(['검사 시각','동작','value (16진수)'], [('6 ns','reset','0'),('16 ns','1 입력','8'),('26 ns','0 입력','4'),('36 ns','enable=0, 입력은 1','4 유지'),('46 ns','enable=1, 1 입력','A'),('56 ns','0 입력','5'),('96 ns','0을 네 번 더 입력','0'),('106 ns','rst=1, 입력은 1','0')]))
    d.frame('클록 에지와 검사 시각', paras('TB는 always #5로 10 ns 주기의 클록을 만든다. 실제 보드의 1 kHz와 달라도 코어의 에지별 동작을 빠르게 검사할 수 있다.', 'step은 @(posedge clk) 뒤 #1을 기다린다. 5 ns 에지에서 초기화하고 6 ns에 갱신된 값을 비교한다.', '값이 맞지 않으면 LAB2_FAIL과 $fatal로 중단한다. 여덟 검사를 모두 통과해야 LAB2_PASS를 출력한다.'))
    code(d, project, config['testbench'])
    d.frame('XDC 전체를 직접 작성', paras('constraints/lab2_shift_register.xdc를 만들고 다음 세 화면을 모두 입력한다.', 'PACKAGE_PIN의 포트 이름·비트 번호를 lab2_shift_register.v와 대조한다. B6의 주기는 1,000,000 ns다.', 'Icarus 코어 TB는 XDC를 사용하지 않는다. PASS만으로 실제 핀 연결이나 버튼 동작이 검증되지는 않는다.'))
    code(d, project, p['constraints'])
    d.frame('VS Code에서 실행', steps('File → Save All로 모든 파일을 저장한다.', 'Terminal → Run Task... → 01 Check tools.', '같은 메뉴에서 02 Simulate. Ctrl+Shift+B도 기본 시뮬레이션 작업을 실행한다.', '오류가 있으면 첫 파일·행 번호부터 확인한다. 마지막 줄만 보고 이전 PASS를 재사용하지 않는다.'), 'simulation')
    shot('작업 메뉴의 세 번호', '11-task-list', '공통 작업 메뉴: 01 도구 확인 → 02 시뮬레이션 → 03 파형 열기 순서다.', (638,8,1240,256), True)
    shot('시프트 레지스터 검사 통과', '06-vscode-pass', 'LAB2_PASS shift_register4 checks=8과 106000 ps(106 ns) 종료를 확인한다.', (353,600,1438,866))
    shot('VaporView 활성화', '07-enable-vaporview', 'Extensions → @installed vaporview. 꺼져 있다면 Enable 옆 화살표 → Enable (Workspace)를 선택한다.', (353,60,1370,410))
    shot('VCD를 파형 편집기로 열기', '08-open-wave', 'build/sim/wave.vcd를 연다. 텍스트로 보이면 오른쪽 위 편집기 선택 메뉴에서 VaporView를 선택한다.', (1120,60,1442,205))
    shot('다섯 신호 추가', '09-netlist', 'Netlist View에서 tb_shift_register4를 펼친다. clk·rst·enable·serial_in·value를 차례로 더블클릭한다.', (45,35,352,320))
    shot('0–106 ns 전체 파형', '10-wave-ns', 'Zoom Fit으로 전체 구간을 맞추고 Time Units → ns. 신호 이름이 잘리면 이름 열 경계를 오른쪽으로 넓힌다.', (353,84,1438,310))
    d.frame('파형 읽기: 입력과 유지', paras('15 ns 에지에서 입력 1이 bit 3에 들어가 value=8이 된다. 25 ns 에지에는 입력 0과 이전 100의 연결로 value=4다.', '35 ns에는 serial_in=1이어도 enable=0이므로 value=4를 유지한다. 이 구간으로 enable의 역할을 확인한다.', '45 ns에는 enable=1이므로 {1,010}=1010, 즉 A가 된다. 55 ns에는 {0,101}=0101, 즉 5가 된다.'))
    d.frame('파형 읽기: 비우기와 초기화', paras('65, 75, 85, 95 ns 에지에 0을 넣으면 5 → 2 → 1 → 0 → 0 순서다. TB는 네 에지를 모두 지난 96 ns에 마지막 0을 검사한다.', '105 ns에는 serial_in과 enable이 모두 1이지만 rst가 우선하여 value=0이다. 비교는 106 ns에 끝난다.', '처음 0–5 ns의 X는 아직 리셋 상승 에지를 거치지 않은 reg의 미정 상태다. 첫 리셋 에지 이후까지 X가 남으면 원인을 찾아야 한다.'))
    d.frame('수정 실험: 시프트 방향 뒤집기', steps('정상 로그와 wave.vcd를 보관한다.', 'shift_register4.v의 {serial_in,value[3:1]}을 {value[2:0],serial_in}으로 바꾼다. TB 기대값은 유지한다.', '저장 → 02 Simulate. 16 ns의 input enters MSB 검사가 실패하는지 확인한다.', '첫 입력 1에서 기대값 1000과 변경된 회로의 0001을 비교한다.', 'RTL을 원복·저장·재실행하고 checks=8, 106 ns 종료를 확인한다.'))
    d.frame('실험 전 레포트', steps('enable·rst별 다음 상태 표와 8 → 4 → A → 5 계산을 작성한다.', '직접 입력한 RTL·TB·simulation.json·XDC의 역할을 설명한다.', '정상·변경·원복의 로그, 검사 시각, 기대값·실제값을 비교한다.', 'VS Code 전체 파형과 enable 유지·리셋 우선 구간을 넣어 해석한다.', '보드의 SW1·N8·K4 조작과 예상 LED를 정리한 뒤 Vivado를 시작한다.'), 'reports')
    from lab2_shift_gui import shift_gui
    shift_gui(d, shot)
    d.frame('장치에 기록', steps('보드 전원·JTAG·주 클록 1 kHz를 확인한다.', 'Open Hardware Manager → Open Target → Auto Connect.', '장치 우클릭 → Program Device → 방금 생성한 lab2_shift_register.bit → Program.', 'K4로 초기화한다. SW1을 먼저 정하고 N8을 누르고 놓는다.'))
    d.frame('보드에서 입력 이력 확인', table(['조작','LED[7:0] (16진수)'], [('K4 초기화','00'),('SW1=1, N8 한 번','08'),('SW1=0, N8 한 번','04'),('SW1=1, N8 한 번','0A'),('SW1=0, N8 한 번','05'),('SW1=0, N8 네 번','02 → 01 → 00 → 00')])+paras('N8을 누르지 않고 SW1만 바꾸면 LED 값은 유지되어야 한다. 이 단계는 학생이 실제 장비에서 확인한다.'))
    d.frame('실험 후 레포트', steps('같은 TB의 XSim PASS·106 ns 종료·파형을 Icarus와 비교한다.', '부품·핀·클록·합성·구현·bit 파일과 타이밍·경고를 기록한다.', '실제 Program Device 화면과 보드 전체·LED 사진을 넣는다.', 'SW1 입력과 N8 조작으로 비트가 이동하고 K4로 초기화되는 영상을 촬영한다.', '소스·전후 레포트·사진·영상 링크를 GitHub README에서 연결한다.'), 'after-report')
    return d
