"""Register teaching pages, with actual September 13 editor and Vivado captures."""
import json
from PIL import Image
from lab2_series import LAB, BASE, Deck, setup, code, paras, steps, table


def make(p):
    project = LAB / p['path']
    config = json.loads((project / 'simulation.json').read_text('utf-8'))
    d = Deck(p['id'])

    def shot(title, name, caption, box=None, common=False):
        folder = 'divider-0913' if common else 'register-0913'
        if box is None:
            box = {
                '06-vscode-pass': (353, 600, 1400, 866),
                '07-enable-vaporview': (353, 60, 1370, 400),
                '08-reopen-wave': (350, 30, 1100, 550),
                '09-netlist': (45, 35, 352, 380),
                '10-wave-ns': (352, 84, 1438, 398),
                'vivado/01-new-menu': (9, 30, 456, 220),
                'vivado/02-project-name': (229, 325, 1260, 470),
                'vivado/03-rtl-project': (229, 327, 800, 426),
                'vivado/04-part': (239, 338, 800, 533),
                'vivado/05-summary': (233, 239, 680, 433),
                'vivado/06-design-sources': (347, 360, 786, 469),
                'vivado/07-select-rtl': (94, 254, 660, 385),
                'vivado/08-rtl-list': (352, 362, 1133, 667),
                'vivado/09-sim-sources': (347, 360, 786, 469),
                'vivado/10-tb-list': (352, 370, 1133, 671),
                'vivado/11-constraints': (347, 360, 786, 469),
                'vivado/12-xdc-list': (352, 394, 1133, 669),
                'vivado/13-tb-top-menu': (307, 305, 790, 722),
                'vivado/14-top-check': (267, 275, 1140, 414),
                'vivado/15-run-behavioral': (25, 425, 467, 630),
                'vivado/16-xsim-pass': (282, 791, 585, 828),
                'vivado/17-xsim-wave': (310, 183, 1480, 509),
                'vivado/18-close-simulation': (10, 30, 266, 251),
                'vivado/19-elaborated': (694, 344, 1484, 575),
                'vivado/20-io-menu': (272, 32, 553, 421),
                'vivado/21-bus-pins': (268, 215, 1032, 781),
                'vivado/22-scalar-pins': (268, 780, 1032, 894),
                'vivado/23-synth-launch': (490, 229, 996, 713),
                'vivado/24-synth-complete': (541, 262, 945, 681),
                'vivado/25-impl-launch': (490, 229, 996, 713),
                'vivado/26-impl-complete': (541, 262, 945, 681),
                'vivado/27-bit-launch': (490, 219, 996, 722),
                'vivado/28-bit-complete': (541, 242, 945, 699),
                'vivado/29-timing': (515, 676, 1120, 861),
            }.get(name)
        trim = ''
        if box:
            x1, y1, x2, y2 = box
            with Image.open(BASE / 'assets' / folder / (name+'.png')) as im:
                width, height = im.size
            trim = ',trim='+' '.join(f'{v*.75:g}bp' for v in [x1,height-y2,width-x2,y1])+',clip'
        d.frame(title, r'\includegraphics[width=\textwidth,height=4.8cm,keepaspectratio'+trim+r']{assets/'+folder+'/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

    def common_workspace(title, name, caption, box=None):
        shot(title, name, caption+' 화면은 v2.0.0 빈 템플릿의 공통 예시다. v2.0.1에서도 여는 방법은 같고 .slang 설정이 추가되어 있다.', box, common=True)

    d.frame('LAB 2 · 레지스터', paras('작성일 2026. 09. 13. · 이해리', '빈 템플릿 → 직접 작성 → Icarus 시뮬레이션 → Vivado 구현'))
    d.frame('목차', r'\navlink{setup}{프로젝트 시작}\par\vspace{0.35cm}\navlink{code}{RTL·TB·XDC 작성}\par\vspace{0.35cm}\navlink{simulation}{VS Code 실행과 파형}\par\vspace{0.35cm}\navlink{reports}{실험 전 레포트}\par\vspace{0.35cm}\navlink{implementation}{Vivado 구현}\par\vspace{0.35cm}\navlink{after-report}{실험 후 레포트}', 'lab2-contents')
    setup(d, p, project, config, workspace_shot=common_workspace)
    d.frame('저장과 전달은 별개다', paras('stored는 입력을 저장하는 4비트 레지스터, value는 저장값을 전달받는 4비트 레지스터다.', '모두 clk 상승 에지에서 갱신된다. rst=1이면 두 레지스터를 먼저 0으로 만든다.', 'load=1이면 data_in을 stored에 저장한다. transfer=1이면 에지 직전 stored를 value에 전달한다.'), 'code')
    d.frame('한 에지의 다음 상태', table(['rst','load','transfer','다음 stored','다음 value'], [('1','무관','무관','0','0'),('0','0','0','유지','유지'),('0','1','0','data_in','유지'),('0','0','1','유지','이전 stored'),('0','1','1','data_in','이전 stored')]))
    d.frame('두 if와 nonblocking 대입', paras('두 if는 독립적으로 검사한다. else if로 바꾸면 load=1일 때 transfer를 검사하지 않게 된다.', 'stored <= data_in과 value <= stored의 오른쪽 항은 같은 에지의 이전 상태에서 읽는다.', '예: stored=A, data_in=3에서 두 제어가 1이면 에지 뒤 stored=3, value=A다. 다음 에지에도 둘 다 1이면 value=3이 된다.'))
    for name in config['sources']:
        code(d, project, name)
    d.frame('버튼을 클록으로 쓰지 않는다', paras('input_frontend는 외부 버튼과 스위치를 주 클록에 동기화한다. 버튼은 20회 연속 안정된 샘플을 확인한 뒤 한 클록의 press를 만든다.', '보드 주 클록은 1 kHz이므로 20샘플은 20 ms다. 버튼을 누르고 놓는 한 동작으로 한 번 실행한다.', 'ASYNC_REG 속성은 동기화 레지스터임을 도구에 알린다. 속성 자체가 버튼 디바운스 기능을 만드는 것은 아니다.'))
    d.frame('보드 입출력 연결', table(['항목','역할'], [('K4 / rst','두 레지스터 초기화'),('N8 / button','선택한 동작 한 번 실행'),('sw[0]','load 선택'),('sw[1]','transfer 선택'),('sw[7:4]','4비트 data_in'),('LED[7:4] / LED[3:0]','stored / value')])+paras('DIP SW1–SW8은 sw[7]–sw[0] 순서다. sw[3:2]는 사용하지 않는다.'))
    d.frame('테스트벤치의 일곱 검사', table(['검사 시각','입력 / 동작','stored,value'], [('6 ns','reset','0,0'),('16 ns','A 저장','A,0'),('26 ns','입력은 3, 저장값 전달','A,A'),('36 ns','3 저장과 전달 동시','3,A'),('46 ns','다음 에지에도 동시','3,3'),('56 ns','입력 F, 두 제어 0','3,3'),('66 ns','리셋과 두 제어 동시','0,0')]))
    d.frame('왜 에지 뒤 1 ns에 검사할까', paras('step은 @(posedge clk) 뒤 #1을 기다린다. nonblocking 갱신이 반영된 다음 상태를 비교하기 위해서다.', 'TB 클록 주기는 10 ns다. 첫 리셋 에지는 5 ns이고 비교는 6 ns에 실행한다.', '불일치가 있으면 LAB2_FAIL과 $fatal로 중단한다. 마지막 비교까지 통과해야 LAB2_PASS를 출력한다.'))
    code(d, project, config['testbench'])
    d.frame('XDC 전체를 직접 작성', paras('constraints/lab2_register.xdc를 만들고 다음 세 화면을 모두 입력한다.', 'lab2_register.v의 포트 이름·비트 번호와 get_ports를 대조한다.', 'Icarus는 XDC를 사용하지 않는다. 코어 TB 통과만으로 핀 연결과 실제 보드 동작이 검증되는 것은 아니다.'))
    code(d, project, p['constraints'])
    d.frame('VS Code에서 실행', steps('File → Save All로 모든 파일을 저장한다.', 'Terminal → Run Task... → 01 Check tools로 도구를 확인한다.', '같은 메뉴에서 02 Simulate를 선택한다. Ctrl+Shift+B도 기본 시뮬레이션 작업을 실행한다.', '컴파일 오류는 첫 오류의 파일·행 번호부터 확인한다.'), 'simulation')
    shot('작업 메뉴의 세 번호', '11-task-list', '같은 템플릿의 공통 작업 메뉴다. 01 도구 확인 → 02 시뮬레이션 → 03 파형 열기 순서로 진행한다.', (638,8,1240,256), common=True)
    shot('레지스터 검사 통과', '06-vscode-pass', 'LAB2_PASS register_pair checks=7과 66000 ps(66 ns) 종료를 확인한다. 이전 실행의 PASS가 아닌 방금 생성된 로그를 읽는다.')
    d.frame('편집기와 실행 도구 문제 구분', paras('WindowsApps·9009 오류가 나면 실제 Python 설치 경로를 확인한다. LAB1.code-workspace의 windows → command에는 자신의 python.exe 경로를 쓴다.', '정적 분석 확장과 Icarus 실행은 별개다. slang 확장과 서버 버전이 맞지 않으면 공식 릴리스의 호환 서버를 설치하고 slang.path를 자신의 경로로 지정한다.', '다른 사람의 C:/Users/... 경로를 복사하지 않는다. 환경 수정 내용과 실제 실행 버전을 레포트에 기록한다.'))
    shot('VaporView 활성화', '07-enable-vaporview', 'Extensions → @installed vaporview. 꺼져 있다면 Enable 옆 화살표 → Enable (Workspace)를 선택한다.')
    shot('VCD를 파형 편집기로 열기', '08-reopen-wave', 'build/sim/wave.vcd를 연다. 텍스트로 열리면 탭 우클릭 → Reopen Editor With... → VaporView를 선택한다.')
    shot('일곱 신호 추가', '09-netlist', 'Netlist View에서 tb_register_pair를 펼친다. clk·rst·load·transfer·data_in·stored·value를 차례로 더블클릭한다.')
    shot('전체 파형과 시간 단위', '10-wave-ns', 'Zoom Fit으로 0–66 ns 전체를 맞추고 Time Units → ns를 선택한다. 신호 이름이 잘리면 이름 열 경계를 오른쪽으로 넓힌다.')
    d.frame('파형 읽기: 저장 후 전달', paras('15 ns 에지에서 stored가 A가 되지만 value는 0이다. load는 저장만 수행하기 때문이다.', '25 ns에는 data_in이 이미 3이다. 그래도 value는 저장해 둔 A가 된다.', '이 구간이 입력을 직접 전달하는 회로와 레지스터 사이 전달 회로를 구분한다.'))
    d.frame('파형 읽기: 동시에 실행', paras('35 ns 에지에서 stored는 3으로 바뀌고 value는 이전 stored인 A를 유지한다.', '45 ns 에지에서 value가 3이 된다. 소스 코드의 위아래 순서로 즉시 전달되는 것으로 해석하지 않는다.', '55 ns에는 두 제어가 0이므로 입력 F를 무시하고 유지한다. 65 ns에는 rst가 두 제어보다 우선해 둘 다 0이 된다.'))
    d.frame('수정 실험: 저장값 대신 입력 전달', steps('정상 로그와 wave.vcd를 보관한다.', 'register_pair.v의 value <= stored를 value <= data_in으로 바꾼다. TB는 바꾸지 않는다.', '저장 → 02 Simulate. 26 ns의 transfer stored not live input 검사가 실패하는지 확인한다.', '그 순간 기대값 A와 잘못 전달된 입력 3을 비교한다.', 'RTL을 원복·저장·재실행해 checks=7 통과를 확인한다.'))
    d.frame('실험 전 레포트', steps('제어 입력별 다음 상태 표와 동시 동작의 계산 과정을 작성한다.', '직접 작성한 RTL·TB·simulation.json·XDC의 역할을 설명한다.', '정상·변경·원복 실행 로그와 검사 시각을 비교한다.', 'VS Code 전체 파형과 25/35/45 ns 확대 파형을 넣어 해석한다.', '보드의 입력 순서와 예상 LED를 계산한 뒤 Vivado를 시작한다.'), 'reports')
    register_gui(d, shot)
    d.frame('장치에 기록', steps('보드 전원·JTAG·주 클록 1 kHz를 확인한다.', 'Open Hardware Manager → Open Target → Auto Connect.', '장치 우클릭 → Program Device → 방금 생성한 lab2_register.bit → Program.', 'K4로 초기화한다. 아래 표대로 DIP 입력을 정하고 N8 버튼을 누른 뒤 놓는다.'))
    d.frame('보드 확인 순서', table(['sw[7:0] (16진수)','N8 한 번 실행 후 LED[7:0]'], [('A1','A0'),('32','AA'),('33','3A'),('33, 다시 누름','33'),('F0','33 유지'),('K4 초기화','00')])+paras('스위치를 먼저 안정시킨 다음 버튼을 누른다. 값과 제어 비트를 구분해 이 결과를 계산한다.'))
    d.frame('실험 후 레포트', steps('동일 TB의 XSim PASS·66 ns 종료·파형을 Icarus와 비교한다.', '부품·핀·클록·합성·구현·bit 파일과 타이밍·경고를 기록한다.', '실제 Program Device 화면과 보드 전체·LED 사진을 넣는다.', '동시 load/transfer를 두 번 실행하는 장면과 초기화 영상을 촬영한다.', '소스·전후 레포트·사진·영상 링크를 GitHub README에서 연결한다.'), 'after-report')
    return d


def register_gui(d, shot):
    d.frame('Vivado에서 같은 원본 연결', paras('VS Code에서 정상·변경·원복 검사와 실험 전 레포트를 마친 뒤 Vivado를 연다.', 'Design top은 lab2_register, Simulation top은 tb_register_pair다.'), 'implementation')
    captures = [
        ('새 프로젝트 메뉴','01-new-menu','File → Project → New... → Next. 기존 프로젝트를 열어 둔 경우에도 같은 메뉴로 시작한다.'),
        ('이름과 위치','02-project-name','Project name: lab2_register. Project location: 자신의 lab2_03_register/vivado. Create project subdirectory 해제 → Next.'),
        ('RTL 프로젝트','03-rtl-project','RTL Project와 Do not specify sources at this time 선택 → Next.'),
        ('정확한 부품','04-part','Parts에서 xc7s75fgga484-1 검색 → 같은 행 선택 → Next. fgga484 패키지와 -1 등급도 확인한다.'),
        ('생성 요약','05-summary','이름·위치·부품이 맞으면 Finish. 기존 프로젝트를 닫을지 묻는 창은 저장 상태 확인 후 Yes.'),
        ('설계 소스 추가','06-design-sources','Add Sources → Add or create design sources → Next → Add Files.'),
        ('RTL 세 파일 선택','07-select-rtl','src의 register_pair.v·input_frontend.v·lab2_register.v 선택 → OK.'),
        ('원본 RTL 연결','08-rtl-list','세 파일을 확인한다. Copy sources into project 해제 → Finish. VS Code에서 수정한 원본을 계속 참조한다.'),
        ('테스트벤치 추가','09-sim-sources','Add Sources → Add or create simulation sources → Next → Add Files → sim/tb_register_pair.sv.'),
        ('TB 등록 확인','10-tb-list','sim_1과 Include all design sources for simulation 유지. Copy sources into project 해제 → Finish.'),
        ('XDC 추가','11-constraints','Add Sources → Add or create constraints → Next → Add Files → constraints/lab2_register.xdc.'),
        ('XDC 원본 연결','12-xdc-list','Copy constraints files into project 해제 → Finish.'),
        ('TB를 Top으로 설정','13-tb-top-menu','Sources → Simulation Sources → sim_1. tb_register_pair 우클릭 → Set as Top.'),
        ('서로 다른 두 Top','14-top-check','TB 이름이 굵게 표시된다. Project Summary의 설계 Top은 lab2_register로 유지되어야 한다.'),
        ('동작 시뮬레이션','15-run-behavioral','Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration이 끝날 때까지 기다린다.'),
        ('XSim에서도 7개 통과','16-xsim-pass','Tcl Console에서 LAB2_PASS register_pair checks=7과 66 ns 종료를 확인한다. 로그가 숨으면 조금 위로 스크롤한다.'),
        ('XSim 전체 파형','17-xsim-wave','Untitled 1 탭을 더블클릭해 넓히고 Zoom Fit을 누른다. stored와 value의 변경 시각을 VS Code 파형과 대조한다.'),
        ('시뮬레이션 종료','18-close-simulation','File → Close Simulation → OK. 레포트용 로그와 파형을 먼저 보관한다.'),
        ('RTL 연결 확인','19-elaborated','RTL Analysis → Open Elaborated Design → OK. 입력 처리 회로의 press와 switches가 load·transfer를 만들고 주 클록이 레지스터로 들어가는지 확인한다.'),
        ('핀 표 열기','20-io-menu','Window → I/O Ports. 아래 I/O Ports 탭을 더블클릭해 표를 넓힌다.'),
        ('LED와 스위치의 핀','21-bus-pins','All ports 우클릭 → Expand Selection. 비트별 Package Pin·I/O Std를 직접 쓴 XDC와 대조한다.'),
        ('클록과 버튼 핀','22-scalar-pins','Scalar ports를 펼친다. button=N8, clk=B6, rst=K4와 LVCMOS33을 확인한다.'),
        ('합성 실행','23-synth-launch','Flow Navigator → Run Synthesis. Launch runs on local host와 jobs 확인 → OK. 이 실행은 jobs=4다.'),
        ('합성 완료','24-synth-complete','Synthesis successfully completed 확인 → Run Implementation → OK.'),
        ('구현 실행','25-impl-launch','Launch runs on local host와 jobs 확인 → OK. 배치배선 중에는 소스와 XDC를 수정하지 않는다.'),
        ('구현 완료','26-impl-complete','Implementation successfully completed 확인 → Generate Bitstream → OK.'),
        ('bit 생성 실행','27-bit-launch','Launch runs on local host와 jobs 확인 → OK. write_bitstream이 완료될 때까지 기다린다.'),
        ('bit 생성 완료','28-bit-complete','Bitstream Generation successfully completed 확인 → Open Implemented Design → OK. Elaborated Design을 닫을지 물으면 Yes.'),
        ('타이밍 결과 확인','29-timing','아래 Timing → Design Timing Summary에서 Setup·Hold의 slack과 Failing Endpoints를 확인한다.'),
    ]
    for title, name, caption in captures:
        shot(title, 'vivado/'+name, caption)
    d.frame('생성 파일과 검증 범위', paras('생성 파일: vivado/lab2_register.runs/impl_1/lab2_register.bit.', '이 교안의 실제 실행은 같은 학생 폴더의 Icarus·XSim 검사와 Vivado 합성·구현·bit 생성까지 확인했다.', '다음 장치 기록과 촬영은 학생이 실습 장비에서 수행한다. bit 생성 화면은 실제 보드 동작을 촬영한 결과가 아니다.'))
    d.frame('타이밍과 남은 경고', paras('WNS=999997.812 ns, WHS=0.119 ns. Setup·Hold의 실패 endpoint는 각각 0이며 지정한 내부 타이밍 제약을 만족했다. 보드 주기는 1,000,000 ns다.', 'TIMING-18: LED 출력 8개의 외부 지연 제약이 없다. 외부 동기 수신기의 조건을 정하지 않았으므로 내부 타이밍 통과를 모든 입출력 타이밍 보장으로 해석하지 않는다.', 'CFGBVS-1: 설정 뱅크의 전압 속성이 지정되지 않았다. 보드 회로도·설정 전압을 확인한 뒤 값을 정하며 임의의 전압을 입력해 경고만 없애지 않는다.'))
