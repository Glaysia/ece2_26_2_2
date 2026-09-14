"""Divider-specific teaching pages backed by the September 13 GUI captures."""
import json
from PIL import Image
from lab2_series import LAB, BASE, Deck, setup, code, paras, steps, table


def make(p):
    project = LAB / p['path']
    config = json.loads((project / 'simulation.json').read_text('utf-8'))
    d = Deck(p['id'])

    def shot(title, name, caption, box=None):
        trim = ''
        if box:
            x1, y1, x2, y2 = box
            with Image.open(BASE / 'assets/divider-0913' / (name+'.png')) as im:
                width, height = im.size
            trim = ',trim=' + ' '.join(f'{v*.75:g}bp' for v in [x1, height-y2, width-x2, y1]) + ',clip'
        d.frame(title, r'\includegraphics[width=\textwidth,height=4.8cm,keepaspectratio'+trim+r']{assets/divider-0913/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

    d.frame('LAB 2 · 클록 분주', paras('작성일 2026. 09. 13. · 이해리', '빈 템플릿 → 소스 작성 → Icarus 시뮬레이션 → Vivado 구현'))
    d.frame('목차', r'\navlink{setup}{프로젝트 시작}\par\vspace{0.35cm}\navlink{code}{RTL·TB·XDC 작성}\par\vspace{0.35cm}\navlink{simulation}{VS Code 실행과 파형}\par\vspace{0.35cm}\navlink{reports}{실험 전 레포트}\par\vspace{0.35cm}\navlink{implementation}{Vivado 구현}\par\vspace{0.35cm}\navlink{after-report}{실험 후 레포트}', 'lab2-contents')
    setup(d, p, project, config, workspace_shot=shot)
    d.frame('두 출력을 구분한다', paras('divided: 입력 주파수를 DIVISOR로 나눈 사각파. 짝수 DIVISOR에서 High와 Low 시간이 같다.', 'tick: count가 DIVISOR−1일 때만 1인 한 클록 폭의 신호. 다른 순차회로의 enable로 사용할 수 있다.', '이 예제는 divided를 다른 always 블록의 클록으로 사용하지 않는다. 모든 상태는 주 클록의 상승 에지에서 바뀐다.'), 'code')
    d.frame('10분주를 손으로 계산', table(['에지 뒤 count', 'divided', 'tick'], [('0–4','0','0'),('5–8','1','0'),('9','1','1'),('다음 에지: 0','0','0')])+paras('오른쪽 항은 에지 직전 count를 읽는다. count==4인 에지에서 divided가 1, count==9인 에지에서 0이 된다.'))
    d.frame('보드와 테스트벤치의 시간', table(['항목','테스트벤치','실제 보드'], [('입력 주기','10 ns','1 ms'),('10분주 주기','100 ns','10 ms'),('1000분주 주기','이 TB에서는 사용 안 함','1 s')])+paras('TB의 100 MHz는 빠른 기능 검사 조건이다. XDC와 보드의 주 클록은 1 kHz다.'))
    for name in config['sources']:
        code(d, project, name)
    d.frame('보드에서 관찰할 출력', table(['출력','주파수 / 폭','관찰 방법'], [('LED[0]','500 Hz','파형·측정 장비'),('LED[1]','100 Hz','파형·측정 장비'),('LED[2]','20 Hz','주기 비교'),('LED[3]','1 Hz','0.5초 켜짐/0.5초 꺼짐'),('LED[4]','1 ms tick','파형·측정 장비')])+paras('K4는 초기화 입력이다. 이 회로에서 N8 버튼과 DIP 스위치는 분주비를 바꾸지 않는다. LED[7:5]는 0이다.'))
    d.frame('테스트벤치가 검사하는 것', steps('DIVISOR=10과 최소값 2를 동시에 검사한다.', '30개 클록에서 듀티·위상·tick을 매번 비교한다.', '10분주 tick을 소비한 에지가 3번인지 확인한다.', '동작 중 리셋을 넣고 초기화와 재시작을 검사한다.', '불일치는 LAB2_FAIL과 $fatal로 즉시 중단한다.'))
    code(d, project, config['testbench'])
    d.frame('XDC도 직접 입력', paras('constraints/lab2_clock_divider.xdc에 다음 화면 전체를 작성한다.', 'get_ports 이름을 lab2_clock_divider.v의 포트와 대조한다.', 'Icarus는 XDC를 사용하지 않는다. PASS는 분주 코어의 기능 검사 결과다. 핀·보드 입출력·타이밍은 Vivado와 장치에서 별도로 확인한다.'))
    code(d, project, p['constraints'])
    d.frame('VS Code에서 실행', steps('File → Save All로 모든 파일을 저장한다.', 'Terminal → Run Task... 또는 Ctrl+Shift+P → Tasks: Run Task.', '01 Check tools로 설치 확인 후 02 Simulate를 선택한다.', 'Ctrl+Shift+B도 이 템플릿의 기본 작업인 02 Simulate를 실행한다.'), 'simulation')
    shot('작업 선택', '11-task-list', '번호 01은 도구 확인, 02는 컴파일·테스트벤치 실행, 03은 파형 파일 열기다.', (638, 8, 1240, 256))
    d.frame('Python 실행 경로 오류', paras('WindowsApps·9009 오류가 나오면 실행 별칭이 실제 Python을 가리키는지 확인한다.', 'LAB1.code-workspace를 열고 세 작업의 windows → command에 자신의 python.exe 경로를 지정한다. JSON 경로에는 /를 쓰면 편리하다.', '다른 사람의 사용자 이름·설치 경로를 그대로 복사하지 않는다. 수정한 항목을 실험 전 레포트에 적는다.'))
    shot('129개 검사 통과', '13-divider-pass', 'LAB2_PASS clock_divider checks=129. 바로 다음 $finish 줄의 436000 ps는 436 ns다. 같은 폴더에서 실행한 최신 로그인지 확인한다.', (366, 790, 755, 822))
    d.frame('편집기 경고와 실행 결과', paras('편집기의 정적 분석과 Icarus 실행은 서로 다른 검사다. 캡처에는 사용하지 않는 입출력 등에 대한 경고가 남아 있다.', 'unknown module 오류는 파일명·module 이름·저장 여부를 먼저 확인한다. 여러 파일의 모듈 탐색이 필요하면 slang의 소스 검색 경로를 지정하고 언어 서버를 재시작한다.', 'PASS는 모든 가능한 입력을 증명한 결과가 아니다. 이번 TB의 129개 비교와 종료 시각을 확인한 결과다.'))
    shot('여러 RTL 파일의 편집기 설정', '19-slang-config', 'v2.0.1에는 .slang/server.json이 포함되어 있다. 이 화면은 이전 템플릿에서 설정을 추가한 예다. 현재 파일에서 src 탐색 설정을 확인한다. src를 모듈 검색 경로로 지정한다. 저장 후 명령 팔레트의 Developer: Reload Window로 다시 연다.', (351,38,804,507))
    shot('VaporView가 꺼져 있다면', '14-enable-vaporview', 'Extensions → @installed vaporview → Enable 옆 화살표 → Enable (Workspace).', (390, 76, 1070, 286))
    shot('텍스트 VCD를 파형으로 전환', '15-reopen-vaporview', 'build/sim/wave.vcd를 연다. 텍스트라면 탭 우클릭 → Reopen Editor With... → VaporView.', (638, 8, 1239, 161))
    shot('관찰할 신호 추가', '16-netlist', 'Netlist View → tb_clock_divider를 펼친다. clk·rst·divided·tick·div2·tick2를 차례로 더블클릭한다.', (49, 36, 347, 406))
    shot('전체 파형과 시간축', '17-wave-ns', '왼쪽 위 Zoom Fit으로 전체 구간을 맞춘다. 이름 열 경계를 넓히고, 하단 Time Units → ns를 선택한다.', (355, 88, 1870, 334))
    d.frame('10분주 파형 해설', paras('rst가 해제된 뒤 divided는 55 ns에서 처음 1이 된다. 이후 105 ns에서 0, 155 ns에서 다시 1이다.', 'High 50 ns와 Low 50 ns를 합친 주기 100 ns는 입력 주기 10 ns의 10배다.', 'tick은 95–105 ns, 195–205 ns, 295–305 ns에 1이다. 다음 상승 에지에서 enable로 소비되므로 30클록 동안 3회가 된다.'))
    d.frame('리셋 파형 해설', paras('376 ns에 rst=1. tick은 리셋 조건에 의해 즉시 0으로 마스킹된다.', '385 ns 상승 에지에서 count와 divided가 초기화된다. rst=0으로 돌아온 후 새 주기를 센다.', '435 ns에서 divided가 다시 1이 되고, TB는 436 ns에 마지막 검사 후 종료한다. 처음 0–5 ns의 X는 첫 동기 리셋 에지 전의 미정 상태다.'))
    d.frame('수정 실험: 한 클록의 차이', steps('정상 로그와 wave.vcd를 별도 보관한다.', 'clock_divider.v에서 상승 조건 DIVISOR/2 - 1을 DIVISOR/2로 바꾼다.', 'TB는 그대로 두고 저장 → 02 Simulate.', 'minimum divisor duty 검사가 16 ns에 실패하는 이유를 계산한다.', '조건을 원복하고 다시 실행해 129개 검사 통과를 확인한다.'))
    d.frame('실험 전 레포트', steps('count·divided·tick의 예상 상태와 분주 주기를 계산한다.', 'RTL·TB·simulation.json·XDC의 역할을 설명한다.', '자신의 정상/변경/원복 로그를 표로 비교한다.', '전체 파형과 듀티·tick·리셋 확대 화면을 넣고 해석한다.', '1 kHz 보드 설정, 각 LED 예상 동작과 측정 방법을 정리한다.'), 'reports')
    divider_gui(d, shot)
    d.frame('장치에 기록', steps('보드 전원·JTAG 연결·주 클록 1 kHz를 확인한다.', 'Open Hardware Manager → Open Target → Auto Connect.', '장치 우클릭 → Program Device → 방금 만든 lab2_clock_divider.bit → Program.', 'K4 초기화 후 LED[3]의 1초 주기와 다른 출력의 분주비를 확인한다.', '빠른 신호는 눈으로 주파수를 단정하지 말고 측정 장비나 파형으로 비교한다.'))
    d.frame('실험 후 레포트', steps('Vivado의 동일 TB PASS·파형을 VS Code 결과와 비교한다.', '부품·핀·클록 제약·합성·구현·bit 파일과 남은 경고를 기록한다.', '실제 장치 기록 화면, 보드 전체와 LED 사진을 넣는다.', '초기화와 1 Hz 출력 변화를 함께 보여 주는 영상을 촬영한다.', '소스·실험 전후 레포트·사진·영상 링크를 GitHub README에서 연결한다.'), 'after-report')
    return d


def divider_gui(d, shot):
    d.frame('Vivado에서 이어서 진행', paras('VS Code의 정상·변경·원복 검사와 실험 전 레포트를 마친 뒤 Vivado를 연다.', '지금부터도 같은 학생 폴더의 소스를 사용한다. Design top은 lab2_clock_divider, Simulation top은 tb_clock_divider다.'), 'implementation')
    for title, name, caption in [
        ('새 프로젝트', '01-start', 'Quick Start → New Project. 이름은 lab2_clock_divider로 정한다.'),
        ('프로젝트 이름과 위치', '02-project-name', 'Project location은 자신의 lab2_02_clock_divider/vivado. Create project subdirectory를 해제하고 Next.'),
        ('RTL Project 선택', '03-rtl-project', 'RTL Project와 Do not specify sources at this time을 선택 → Next.'),
        ('정확한 부품 선택', '04-part', 'Parts에서 xc7s75fgga484-1을 검색하고 해당 행을 선택 → Next. 패키지 fgga484와 속도 등급 -1도 확인한다.'),
        ('생성 전 확인', '05-summary', '프로젝트 이름·위치·부품이 맞으면 Finish. 보드 top과 테스트벤치는 다음 단계에서 각각 등록한다.'),
        ('설계 소스 추가', '07-design-sources', 'Flow Navigator → Add Sources → Add or create design sources → Next.'),
        ('RTL 파일 찾기', '08-add-files', 'Add Files → 학생 폴더의 src를 연다. 앞에서 이름을 바꾸고 작성한 RTL 파일을 고른다.'),
        ('RTL 세 파일 선택', '09-select-rtl', 'clock_divider.v·input_frontend.v·lab2_clock_divider.v를 선택 → OK. 이 폴더에 세 파일만 있으면 목록 클릭 후 Ctrl+A로 선택할 수 있다.'),
        ('원본 소스 연결', '10-rtl-list', '목록의 세 파일을 확인한다. Copy sources into project를 해제 → Finish. VS Code에서 저장한 원본을 계속 참조한다.'),
        ('시뮬레이션 소스 추가', '11-sim-sources', 'Add Sources → Add or create simulation sources → Next → Add Files → sim/tb_clock_divider.sv.'),
        ('테스트벤치 등록 확인', '12-tb-list', 'sim_1과 Include all design sources for simulation을 유지한다. Copy sources into project 해제 → Finish.'),
        ('제약 소스 추가', '13-constraints', 'Add Sources → Add or create constraints → Next → Add Files → constraints/lab2_clock_divider.xdc.'),
        ('XDC 등록 확인', '14-xdc-list', 'Copy constraints files into project 해제 → Finish. XDC의 수정도 학생 폴더 원본에 저장한다.'),
        ('TB를 최상위로 지정', '15-tb-set-top', 'Sources → Simulation Sources → sim_1을 펼친다. tb_clock_divider 우클릭 → Set as Top.'),
        ('두 Top을 구분', '16-top-check', 'Simulation Sources에서 tb_clock_divider가 굵게 표시된다. Project Summary의 설계 Top은 lab2_clock_divider여야 한다.'),
        ('동작 시뮬레이션 실행', '17-run-behavioral', 'Flow Navigator → Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration이 끝날 때까지 기다린다.'),
        ('동일한 129개 검사 통과', '18-xsim-pass', 'Tcl Console에서 LAB2_PASS clock_divider checks=129와 436 ns 종료를 확인한다. PASS가 위로 숨으면 콘솔을 조금 위로 스크롤한다.'),
        ('Vivado 전체 파형', '19-xsim-wave', 'Untitled 1 파형 탭을 더블클릭해 넓힌 뒤 Zoom Fit을 누른다. divided 주기 100 ns, tick 폭 10 ns와 동작 중 리셋을 VS Code 파형과 대조한다.'),
        ('시뮬레이션 종료', '20-close-sim', 'File → Close Simulation → OK. 캡처와 레포트용 로그를 먼저 보관한다.'),
        ('RTL 회로 연결 확인', '21-elaborated', 'RTL Analysis → Open Elaborated Design → 안내 창 OK. 주 클록이 각 분주 회로에 연결되고 출력이 LED로 이어지는지 확인한다.'),
        ('핀 표 열기', '22-io-menu', 'Window → I/O Ports. 아래에 열린 I/O Ports 탭을 더블클릭하면 표가 넓어진다.'),
        ('LED와 스위치 핀', '23-bus-pins', 'All ports 우클릭 → Expand Selection. 각 비트의 Package Pin·I/O Std를 XDC와 대조한다.'),
        ('클록과 버튼 핀', '24-all-pins', 'Scalar ports도 펼친다. clk=B6, rst=K4, button=N8, 모두 LVCMOS33인지 확인한다.'),
        ('합성 실행', '25-synth-launch', 'Flow Navigator → Run Synthesis. Launch runs on local host와 jobs를 확인 → OK. 이 화면은 jobs=4로 실행했다.'),
        ('합성 완료 후 구현', '26-synth-complete', 'Synthesis successfully completed를 확인한다. Run Implementation 선택 → OK.'),
        ('구현 실행', '27-impl-launch', 'Launch runs on local host와 jobs를 확인 → OK. 배치배선 중에는 소스와 XDC를 수정하지 않는다.'),
        ('구현 완료 후 bit 생성', '28-impl-complete', 'Implementation successfully completed를 확인한다. Generate Bitstream 선택 → OK.'),
        ('비트스트림 실행', '29-bit-launch', 'Launch runs on local host와 jobs를 확인 → OK. 오른쪽 위 Running write_bitstream이 완료될 때까지 기다린다.'),
        ('비트스트림 생성 완료', '30-bit-complete', 'Bitstream Generation successfully completed를 확인한다. Open Implemented Design 선택 → OK. bit 생성 완료와 실제 장치 기록은 서로 다른 단계다.'),
        ('구현 타이밍 결과', '31-timing', 'Elaborated Design을 닫을지 묻는 창은 Yes. 아래 Timing → Design Timing Summary에서 Setup·Hold의 slack과 Failing Endpoints를 확인한다.'),
    ]:
        boxes = {
            '01-start':(40,108,518,381), '02-project-name':(229,325,1260,469),
            '03-rtl-project':(229,327,800,426), '04-part':(239,338,800,533),
            '05-summary':(233,239,650,433), '07-design-sources':(347,360,786,469),
            '08-add-files':(351,354,1133,580), '09-select-rtl':(94,254,575,375),
            '10-rtl-list':(352,362,1133,667), '11-sim-sources':(347,360,786,469),
            '12-tb-list':(352,370,1133,671), '13-constraints':(347,360,786,469),
            '14-xdc-list':(352,394,1133,669), '15-tb-set-top':(308,306,802,790),
            '16-top-check':(266,275,1140,411), '17-run-behavioral':(25,425,467,630),
            '18-xsim-pass':(279,793,570,867), '19-xsim-wave':(310,183,1480,530),
            '20-close-sim':(10,30,266,251), '21-elaborated':(694,213,1484,701),
            '22-io-menu':(272,32,553,421), '23-bus-pins':(268,215,1032,781),
            '24-all-pins':(268,780,1032,894), '25-synth-launch':(490,229,996,713),
            '26-synth-complete':(541,262,945,681), '27-impl-launch':(490,229,996,713),
            '28-impl-complete':(541,262,945,681), '29-bit-launch':(490,219,996,722),
            '30-bit-complete':(541,242,945,699),
            '31-timing':(515,676,1120,861),
        }
        shot(title, 'vivado/'+name, caption, boxes.get(name))
    d.frame('생성 파일과 검증 범위', paras('생성 파일: vivado/lab2_clock_divider.runs/impl_1/lab2_clock_divider.bit.', '이 교안의 실제 실행은 Vivado 2026.1에서 동일 학생 폴더의 시뮬레이션·합성·구현·bit 생성까지 확인했다.', '다음 장치 기록 절차는 학생이 실습 장비에서 수행한다. 이 교안의 bit 생성 화면은 보드 동작을 촬영한 결과가 아니다.'))
    d.frame('남은 경고도 레포트에 기록', paras('구현 보고서의 WNS=999996.312 ns, WHS=0.122 ns. 지정한 내부 타이밍 제약은 만족했다. 입력 주기가 1,000,000 ns이므로 WNS가 크게 나온다.', 'TIMING-18: 입출력 지연 제약이 빠져 있다. LED 관찰용 출력에는 외부 동기 수신기의 타이밍 조건을 정의하지 않았다. 내부 타이밍 통과를 모든 외부 입출력 타이밍 보장으로 해석하지 않는다.', 'CFGBVS-1: 설정 뱅크의 전압 속성이 지정되지 않았다. 보드 회로도·설정 전압을 확인한 뒤 값을 정하며, 경고를 없애려고 임의의 전압을 입력하지 않는다.'))
