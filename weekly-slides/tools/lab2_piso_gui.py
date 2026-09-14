"""PISO walkthrough using captures from the actual student Vivado project."""
from PIL import Image
from lab2_intro import paras


def walkthrough(d, base):
    folder = base / 'assets/piso-0913/vivado'

    def shot(title, name, caption, box=None):
        trim = ''
        if box:
            with Image.open(folder / (name + '.png')) as im:
                width, height = im.size
            x1, y1, x2, y2 = box
            assert 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height
            trim = ',trim=' + ' '.join(f'{v*.75:g}bp' for v in (x1, height-y2, width-x2, y1)) + ',clip'
        d.frame(title, r'\includegraphics[width=\textwidth,height=4.8cm,keepaspectratio'+trim+r']{assets/piso-0913/vivado/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

    d.frame('Vivado에서 같은 PISO 원본 연결', paras('VS Code 정상·변경·원복 검사와 실험 전 레포트를 마친 뒤 시작한다.', '설계 Top은 lab2_piso, 시뮬레이션 Top은 tb_piso4다. 두 모듈의 용도를 구분한다.'), 'implementation')
    rows = [
        ('프로젝트 이름과 위치', '02-project-name', 'File → Project → New → Next. 이름은 lab2_piso, 위치는 자신의 lab2_05_piso/vivado. Create project subdirectory 해제 → Next.', (28,190,1053,350)),
        ('RTL 프로젝트 선택', '03-rtl-project', 'RTL Project와 Do not specify sources at this time을 선택한다. Next.', (28,195,600,300)),
        ('정확한 부품 선택', '04-part', 'Parts 검색란에 xc7s75fgga484-1을 입력한다. 같은 행 선택 → Next. -1IL·-1Q와 구분한다.', (30,202,700,403)),
        ('생성 요약 확인', '05-project-summary', 'lab2_piso·Spartan-7·fgga484·-1을 확인하고 Finish. 이전 프로젝트가 열려 있으면 저장 상태 확인 후 닫는다.', (27,106,670,300)),
        ('빈 프로젝트 확인', '06-empty-project', 'Project Summary에서 이름·위치·부품을 확인한다. 아직 소스를 넣지 않았으므로 Top module은 Not defined다.', (787,233,1465,506)),
        ('설계 RTL 세 파일 선택', '07-select-design-files', 'Add Sources → Add or create design sources → Next → Add Files. src에서 input_frontend.v·lab2_piso.v·piso4.v를 선택하고 OK.', (26,54,700,202)),
        ('원본 RTL 참조', '08-design-no-copy', '세 파일을 확인한다. Copy sources into project 해제 → Finish. VS Code에서 편집한 원본을 계속 참조한다.', (33,207,812,486)),
        ('테스트벤치 등록', '09-simulation-no-copy', 'Add Sources → Add or create simulation sources → Next → Add Files → sim/tb_piso4.sv. sim_1과 Include all design sources 유지, Copy sources 해제 → Finish.', (32,210,810,517)),
        ('XDC 원본 참조', '10-xdc-no-copy', 'Add Sources → Add or create constraints → Next → Add Files → constraints/lab2_piso.xdc. Copy constraints files into project 해제 → Finish.', (32,211,813,512)),
        ('테스트벤치를 Top으로', '11-set-sim-top-menu', 'Simulation Sources → sim_1을 펼친다. tb_piso4 우클릭 → Set as Top. 보드용 lab2_piso와 혼동하지 않는다.', (402,616,772,726)),
        ('서로 다른 Top 확인', '12-simulation-top', 'tb_piso4가 굵게 표시된다. Project Summary의 설계 Top은 lab2_piso다. 이 상태로 시뮬레이션한다.', (268,273,1100,414)),
        ('XSim 실행', '13-run-behavioral-menu', '왼쪽 Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration이 끝날 때까지 기다린다.', (26,423,470,634)),
        ('XSim 114개 검사 통과', '14-xsim-pass', 'Tcl Console에서 LAB2_PASS piso4 checks=114와 $finish 976 ns를 확인한다. 1000 ns 실행 요청보다 먼저 TB가 종료되는 것은 정상이다.', (281,734,595,777)),
        ('전체 파형 확인', '15-xsim-wave-full', '파형 탭 더블클릭 → Zoom Fit. data_in이 0부터 F까지 바뀌며 모든 4비트 입력을 검사한다. Icarus와 같은 RTL·TB로 얻은 결과다.', (313,217,1480,552)),
        ('A 입력을 직렬로 내보내기', '16-xsim-wave-a', 'A 구간을 클릭한 뒤 Zoom In으로 확대한다. 615 ns에 A를 로드하고 625 ns에는 유지한다. 635·645·655 ns에 value가 4·8·0이 되며 MSB가 1·0·1·0 순서로 관찰된다.', (313,217,1480,552)),
        ('LED 핀 확인', '17-io-led', 'Open Elaborated Design → OK. 오른쪽 위 I/O Planning → I/O Ports 탭 더블클릭. led를 펼쳐 Package Pin·LVCMOS33을 XDC와 대조한다.', (267,212,1036,528)),
        ('스위치 핀 확인', '18-io-switches', 'sw를 펼쳐 여덟 핀을 확인한다. DIP SW1–SW4는 sw[7:4] 병렬 입력, SW8은 sw[0] load다. 스위치 번호와 비트 번호를 구분한다.', (267,530,1036,781)),
        ('버튼·클록·리셋 핀 확인', '19-io-all', 'Scalar ports를 펼친다. button=N8, clk=B6, rst=K4다. 19개 포트 모두 LVCMOS33이다. B6 주 클록은 1 kHz로 설정한다.', (267,782,1036,895)),
        ('합성 실행', '20-synthesis-launch', '왼쪽 Run Synthesis. Launch runs on local host와 jobs를 확인하고 OK. 이 실행은 jobs=4다.', (20,112,486,278)),
        ('합성 완료', '21-synthesis-complete', 'Synthesis successfully completed를 확인한다. Run Implementation 선택 → OK.', (20,48,386,239)),
        ('구현 실행', '22-implementation-launch', 'Launch runs on local host와 jobs를 확인하고 OK. 구현 도중에는 RTL·XDC를 수정하지 않는다.', (20,112,486,278)),
        ('구현 완료', '23-implementation-complete', 'Implementation successfully completed를 확인한다. Generate Bitstream 선택 → OK.', (20,48,386,239)),
        ('비트스트림 생성 실행', '24-bitstream-launch', 'Launch runs on local host와 jobs를 확인하고 OK. write_bitstream 완료까지 기다린다.', (20,130,486,296)),
        ('비트스트림 생성 완료', '25-bitstream-complete', 'Bitstream Generation successfully completed 확인. Open Implemented Design → OK. 이전 Elaborated Design을 닫을지 물으면 Yes.', (20,49,386,278)),
        ('타이밍 확인', '26-timing', 'Timing → Design Timing Summary. Setup·Hold의 slack과 Number of Failing Endpoints를 확인한다.', (515,675,1120,868)),
    ]
    for title, name, caption, box in rows:
        shot(title, name, caption, box)
    d.frame('검사 결과와 생성 파일', paras('XSim: LAB2_PASS piso4 checks=114, 976 ns 종료. Icarus와 같은 TB와 원복한 RTL을 사용했다.', '생성 파일: vivado/lab2_piso.runs/impl_1/lab2_piso.bit.', 'GUI 합성·구현·bit 생성까지 확인했다. 장치 기록과 보드 사진·영상은 학생이 실습 장비에서 수행한다.'))
    d.frame('타이밍과 경고 해석', paras('WNS=999997.500 ns, WHS=0.121 ns. Setup·Hold 실패 endpoint는 각각 0이다. 주 클록 제약은 1,000,000 ns다.', 'TIMING-18: 외부 입출력 지연 관련 경고다. 비동기 입력에는 false path를 적용했고 LED 출력 지연은 지정하지 않았다. 내부 타이밍 통과가 모든 외부 입출력 타이밍을 보장하지는 않는다.', 'CFGBVS-1: 설정 뱅크 전압 속성이 없다. 보드 회로도와 설정 전압을 확인하여 값을 정한다. 경고만 없애려고 임의의 전압을 입력하지 않는다.'))
