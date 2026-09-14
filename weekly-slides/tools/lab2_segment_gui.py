"""Segment scanner walkthrough backed by the student Vivado GUI run."""
from PIL import Image
import json
from lab2_intro import paras


def walkthrough(d, base):
    folder = base / 'assets/segment-0914/vivado'
    proof = json.loads((base.parents[2]/'output/evidence/lab2-segment-0914/vivado-gui-validation.json').read_text('utf-8'))
    assert proof['status'] == 'GUI_XSIM_SYNTHESIS_IMPLEMENTATION_BIT_VERIFIED'

    def shot(title, name, caption, box=None):
        trim = ''
        if box:
            with Image.open(folder/(name+'.png')) as im:
                width, height = im.size
            x1,y1,x2,y2 = box
            assert 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height
            trim = ',trim='+' '.join(f'{v*.75:g}bp' for v in (x1,height-y2,width-x2,y1))+',clip'
        d.frame(title,r'\includegraphics[width=\textwidth,height=4.8cm,keepaspectratio'+trim+r']{assets/segment-0914/vivado/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

    d.frame('Vivado에 같은 원본 연결',paras('VS Code 정상·변경·원복 검사와 실험 전 레포트를 마친 뒤 시작한다.','설계 Top은 lab2_segment_scan, 시뮬레이션 Top은 tb_segment_scan8이다. 시뮬레이션은 코어를 검사하며 보드 연결 모듈은 실제 핀 극성을 연결한다.'),'implementation')
    rows = [
        ('프로젝트 이름과 위치','02-project-name','File → Project → New → Next. 이름은 lab2_segment_scan, 위치는 자신의 lab2_08_segment_scan/vivado. Create project subdirectory 해제 → Next.',(28,190,1053,350)),
        ('RTL 프로젝트 선택','03-rtl-project','RTL Project와 Do not specify sources at this time을 선택한다. Next.',(28,195,600,300)),
        ('정확한 부품 선택','04-part','Parts 검색란에 xc7s75fgga484-1을 입력한다. 같은 행 선택 → Next. -1IL·-1Q와 구분한다.',(30,202,700,403)),
        ('생성 요약 확인','05-project-summary','lab2_segment_scan·Spartan-7·fgga484·-1을 확인하고 Finish. 이전 프로젝트가 열려 있으면 저장 상태를 확인한 뒤 닫는다.',(27,106,670,300)),
        ('원본 RTL 참조','06-design-sources','Add Sources → Add or create design sources → Next → Add Files. src의 input_frontend.v·lab2_segment_scan.v·segment_scan8.v 선택 → OK. 빈 design.v는 선택하지 않는다. Copy sources into project 해제 → Finish.',(33,207,812,486)),
        ('테스트벤치 등록','07-simulation-source','Add Sources → Add or create simulation sources → Next → Add Files → sim/tb_segment_scan8.sv. sim_1과 Include all design sources 유지, Copy sources 해제 → Finish.',(32,210,810,517)),
        ('XDC 원본 참조','08-constraints','Add Sources → Add or create constraints → Next → Add Files → constraints/lab2_segment_scan.xdc. Copy constraints files into project 해제 → Finish. VS Code에서 편집한 원본을 계속 참조한다.',(32,211,813,512)),
        ('테스트벤치를 Top으로','09-set-top','Simulation Sources → sim_1을 펼친다. tb_segment_scan8 우클릭 → Set as Top. 보드용 lab2_segment_scan과 혼동하지 않는다.',(450,693,820,728)),
        ('서로 다른 Top 확인','10-tops','Design Sources의 lab2_segment_scan과 Simulation Sources → sim_1의 tb_segment_scan8이 각각 굵게 표시되는지 확인한다.',(269,215,1110,413)),
        ('XSim 실행','11-run-simulation','왼쪽 Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration이 끝날 때까지 기다린다.',(28,423,466,636)),
        ('1000 ns에서 끝내지 않기','12-run-all','기본 실행은 1000 ns에서 멈춘다. 이때 checks=150으로 아직 검사가 끝나지 않았다. Run → Run All 또는 F3를 눌러 테스트벤치의 $finish까지 실행한다.',(463,67,757,287)),
        ('XSim 194개 검사 통과','13-simulation-pass','Tcl Console에서 LAB2_PASS segment_scan8 checks=194와 $finish 1306 ns를 확인한다. 오류로 중단되거나 검사 수가 다르면 통과한 것으로 기록하지 않는다.',(290,791,566,831)),
        ('전체 파형 확인','14-wave-full','파형 탭 더블클릭 → Zoom Fit. digits는 76543210에서 fedcba98로 바뀐다. 각 입력 묶음에서 index=0~7을 두 번 순회한다. enable=0에서 유지되고 마지막 rst에서 index=0·select=00이 되는지 VS Code 파형과 대조한다.',(313,215,1480,610)),
        ('핀 확인 화면 열기','15-elaborated','Open Elaborated Design → OK. 오른쪽 위 레이아웃에서 I/O Planning 선택 → I/O Ports 탭 더블클릭. All ports는 35개다.',(269,630,1107,899)),
        ('LED 핀 확인','16-io-led','led 왼쪽 화살표를 펼쳐 8개 Package Pin을 XDC와 대조한다. led[0]부터 N5·M1·M3·M7·N7·M2·M4·L4다. 모든 I/O Std는 LVCMOS33이다.',(267,212,1055,528)),
        ('자리 선택 핀 확인','17-io-seg-com','led를 접고 seg_com을 펼친다. seg_com[0]부터 K5·K3·K1·L6·G3·G1·H6·H4다. 코어 index=0은 비트 반전과 순서 변경을 거쳐 COM[7]을 선택한다.',(267,212,1055,556)),
        ('세그먼트 데이터 핀 확인','18-io-seg-data','seg_com을 접고 seg_data를 펼친다. seg_data[0]부터 H2·J7·J3·J1·E4·E2·F5·F1이다. 이름·비트 번호·Package Pin을 모두 확인한다.',(267,212,1055,584)),
        ('스위치 핀 확인','19-io-sw','seg_data를 접고 sw를 펼친다. sw[0]부터 U4·V4·W1·W4·T1·U2·W3·Y1이다. SW1~4는 sw[7:4]로 첫 자리 숫자를 정한다.',(267,212,1055,612)),
        ('버튼·클록·리셋 핀 확인','20-io-scalar','Scalar ports를 펼친다. button=N8, clk=B6, rst=K4다. B6 주 클록은 1 kHz다. 이 회로는 자동 스캔하므로 N8 버튼을 누를 필요가 없다.',(267,614,1055,729)),
        ('합성 실행','21-synthesis-launch','왼쪽 Run Synthesis. Launch runs on local host와 jobs를 확인하고 OK. 이 실행은 jobs=4다.',(20,112,486,278)),
        ('합성 완료','22-synthesis-complete','Synthesis successfully completed 확인 → Run Implementation 선택 → OK.',(20,48,386,239)),
        ('구현 실행','23-implementation-launch','Launch runs on local host와 jobs를 확인하고 OK. 구현 도중에는 RTL·XDC를 수정하지 않는다.',(20,112,486,278)),
        ('구현 완료','24-implementation-complete','Implementation successfully completed 확인 → Generate Bitstream 선택 → OK.',(20,48,386,239)),
        ('비트스트림 생성 실행','25-bitstream-launch','Launch runs on local host와 jobs를 확인하고 OK. write_bitstream 완료까지 기다린다.',(20,130,486,296)),
        ('비트스트림 생성 완료','26-bitstream-complete','Bitstream Generation successfully completed 확인. Open Implemented Design → OK. 이전 Elaborated Design을 닫을지 물으면 Yes.',(20,49,386,278)),
        ('타이밍 확인','27-timing','Timing → Design Timing Summary. Setup·Hold의 slack과 Number of Failing Endpoints를 확인한다.',(515,675,1120,868)),
    ]
    for title,name,caption,box in rows:
        shot(title,name,caption,box)
    d.frame('검사 결과와 생성 파일',paras('XSim: LAB2_PASS segment_scan8 checks=194, 1306 ns 종료. Icarus와 같은 TB와 원복한 RTL을 사용했다.','생성 파일: vivado/lab2_segment_scan.runs/impl_1/lab2_segment_scan.bit.','GUI 합성·구현·bit 생성까지 확인했다. 장치 기록과 보드 사진·영상은 학생이 실습 장비에서 수행한다.'))
    d.frame('타이밍과 경고 해석',paras(f"WNS={proof['wns_ns']:.3f} ns, WHS={proof['whs_ns']:.3f} ns. Setup·Hold 실패 endpoint는 각각 0이다. 주 클록 제약은 1,000,000 ns다.",'TIMING-18: LED·자리 선택·세그먼트 데이터의 출력 24개에 외부 출력 지연이 지정되지 않았다. 비동기 입력에는 false path를 적용했다. 내부 타이밍 통과가 외부 입출력 타이밍까지 보장하지는 않는다.','CFGBVS-1: 설정 뱅크 전압 속성이 없다. 보드 회로도와 설정 전압을 확인하여 값을 정한다. 경고만 없애려고 임의의 전압을 입력하지 않는다.'))
