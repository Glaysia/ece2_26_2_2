"""Actual shift-register Vivado walkthrough; implementation review continues."""
from lab2_intro import paras


def shift_gui(d, shot):
    d.frame('Vivado에서 같은 원본 연결', paras('VS Code 정상·변경·원복 검사와 실험 전 레포트를 마친 뒤 시작한다.', '설계 Top은 lab2_shift_register, 시뮬레이션 Top은 tb_shift_register4다.'), 'implementation')
    captures = [
        ('프로젝트 이름과 위치','02-project-name','File → Project → New. 이름은 lab2_shift_register, 위치는 자신의 lab2_04_shift_register/vivado. Create project subdirectory 해제 → Next.'),
        ('RTL 프로젝트 선택','03-rtl-project','RTL Project와 Do not specify sources at this time을 선택한다. Next.'),
        ('부품 검색과 선택','04-part','Parts 검색란에 xc7s75fgga484-1을 입력한다. 같은 이름의 행을 선택한다. -1IL·-1Q와 구분한다. Next.'),
        ('생성 요약 확인','05-project-summary','이름·Spartan-7·fgga484·-1을 확인하고 Finish. 이전 프로젝트가 열려 있으면 저장 상태 확인 후 닫는다.'),
        ('빈 프로젝트 확인','06-empty-project','Project Summary에서 부품을 확인한다. 아직 소스를 넣지 않았으므로 Top module은 Not defined다.'),
        ('설계 소스 추가','07-add-design','왼쪽 Add Sources → Add or create design sources → Next → Add Files.'),
        ('RTL 세 파일 선택','08-select-rtl','자신의 src 폴더를 연다. input_frontend.v·lab2_shift_register.v·shift_register4.v를 모두 선택하고 OK.'),
        ('원본 RTL 참조','09-rtl-reference','세 파일을 확인한다. Copy sources into project를 해제하고 Finish. VS Code에서 수정하는 원본과 연결한다.'),
        ('테스트벤치 추가','10-add-simulation','Add Sources → Add or create simulation sources → Next → Add Files. sim/tb_shift_register4.sv를 선택한다.'),
        ('TB 등록 확인','11-tb-reference','sim_1과 Include all design sources for simulation을 유지한다. Copy sources into project를 해제하고 Finish.'),
        ('XDC 추가','12-add-constraints','Add Sources → Add or create constraints → Next → Add Files. constraints/lab2_shift_register.xdc를 선택한다.'),
        ('XDC 원본 참조','13-xdc-reference','Copy constraints files into project를 해제하고 Finish. 핀 변경도 같은 원본 파일에 반영한다.'),
        ('테스트벤치를 Top으로','14-set-tb-top','Sources → Simulation Sources → sim_1을 펼친다. tb_shift_register4 우클릭 → Set as Top.'),
        ('서로 다른 Top 확인','15-tb-top','tb_shift_register4가 굵게 표시된다. Project Summary의 설계 Top은 lab2_shift_register로 유지한다.'),
        ('XSim 실행','16-run-behavioral','왼쪽 Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration이 끝날 때까지 기다린다.'),
        ('XSim 전체 파형','17-xsim-wave','파형 탭을 더블클릭해 확대하고 Zoom Fit을 누른다. 106 ns 종료와 checks=8을 확인한다. value는 0 → 8 → 4 유지 → A → 5 → 2 → 1 → 0이다.'),
        ('보드 회로 연결 확인','18-elaborated','Open Elaborated Design → OK. 입력 처리 회로의 press가 enable, switches[7]이 serial_in으로 연결되는지 확인한다.'),
        ('19개 포트의 핀 확인','19-all-pins','오른쪽 위 레이아웃 → I/O Planning. I/O Ports 탭을 더블클릭하고 Expand All. Package Pin과 LVCMOS33을 XDC와 대조한다.'),
        ('합성 실행','20-launch-synthesis','왼쪽 Run Synthesis. Launch runs on local host와 Number of jobs를 확인하고 OK. 이 실행은 jobs=4다.'),
        ('합성 완료','21-synthesis-complete','Synthesis successfully completed를 확인한다. Run Implementation 선택 → OK.'),
        ('구현 실행','22-launch-implementation','Launch runs on local host → OK. 구현 중에는 RTL과 XDC를 수정하지 않는다.'),
        ('구현 완료','23-implementation-complete','Implementation successfully completed를 확인한다. Generate Bitstream 선택 → OK.'),
        ('비트스트림 생성 실행','24-launch-bitstream','Launch runs on local host와 jobs를 확인하고 OK. write_bitstream 완료까지 기다린다.'),
        ('비트스트림 생성 완료','25-bitstream-complete','Bitstream Generation successfully completed 확인. Open Implemented Design → OK. 이전 Elaborated Design을 닫을지 물으면 Yes.'),
        ('타이밍 확인','26-timing','Timing → Design Timing Summary. Setup·Hold의 slack과 Number of Failing Endpoints를 확인한다.'),
    ]
    for title,name,caption in captures:
        box = {
            '02-project-name':(28,190,1053,350), '03-rtl-project':(28,195,600,300),
            '04-part':(30,202,700,403), '05-project-summary':(27,106,670,300),
            '06-empty-project':(787,233,1465,506), '07-add-design':(29,205,510,305),
            '08-select-rtl':(26,54,700,181), '09-rtl-reference':(33,207,812,486),
            '10-add-simulation':(29,205,510,306), '11-tb-reference':(32,210,810,517),
            '12-add-constraints':(29,205,510,306), '13-xdc-reference':(32,211,813,512),
            '14-set-tb-top':(427,611,798,728), '15-tb-top':(268,273,1100,414),
            '16-run-behavioral':(26,423,470,634), '17-xsim-wave':(312,185,1480,444),
            '18-elaborated':(695,350,1480,574), '19-all-pins':(267,212,1036,895),
            '20-launch-synthesis':(20,112,486,278), '21-synthesis-complete':(20,48,386,239),
            '22-launch-implementation':(20,112,486,278), '23-implementation-complete':(20,48,386,239),
            '24-launch-bitstream':(20,130,486,296), '25-bitstream-complete':(20,49,386,278),
            '26-timing':(515,675,1120,868),
        }.get(name)
        if name == '19-all-pins':
            shot('LED 핀 확인','vivado/'+name,'I/O Planning → I/O Ports 탭 더블클릭 → Expand All. led[7:0]의 Package Pin과 LVCMOS33을 XDC와 대조한다.',(267,212,1036,528))
            shot('스위치 핀 확인','vivado/'+name,'같은 표의 sw[7:0]을 확인한다. 이 회로의 직렬 입력은 sw[7]이며 보드의 SW1에 대응한다.',(267,530,1036,781))
            shot('버튼·클록·리셋 핀 확인','vivado/'+name,'Scalar ports의 button=N8, clk=B6, rst=K4와 LVCMOS33을 확인한다. LED 8개·스위치 8개·단일 포트 3개, 총 19개다.',(267,782,1036,895))
            continue
        shot(title,'vivado/'+name,caption,box)
    d.frame('검사 결과와 생성 파일',paras('XSim: LAB2_PASS shift_register4 checks=8, 106 ns 종료. Icarus와 같은 TB와 원복한 RTL을 사용했다.', '생성 파일: vivado/lab2_shift_register.runs/impl_1/lab2_shift_register.bit.', 'GUI 합성·구현·bit 생성까지 확인했다. 다음 장치 기록과 보드 촬영은 학생이 실습 장비에서 수행한다.'))
    d.frame('타이밍과 경고 해석',paras('WNS=999997.000 ns, WHS=0.122 ns. Setup·Hold 실패 endpoint는 각각 0이다. 주 클록 제약은 1,000,000 ns다.', 'TIMING-18: LED의 외부 출력 지연을 지정하지 않았다. 내부 타이밍 통과를 모든 외부 입출력 타이밍 보장으로 해석하지 않는다.', 'CFGBVS-1: 설정 뱅크 전압 속성이 없다. 보드 회로도와 설정 전압을 확인하여 값을 정한다. 경고만 없애려고 임의의 전압을 입력하지 않는다.'))
