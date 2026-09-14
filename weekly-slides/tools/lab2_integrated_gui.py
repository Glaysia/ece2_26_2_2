"""Integrated Vivado walkthrough using actual student-project captures."""
from PIL import Image
import json
from lab2_intro import paras


def walkthrough(d, base):
    folder = base / 'assets/integrated-0914/vivado-final'
    proof = json.loads((base.parents[2]/'output/evidence/lab2-integrated-0914/vivado-gui-validation.json').read_text('utf-8'))
    assert proof['status'] == 'GUI_XSIM_SYNTHESIS_IMPLEMENTATION_BIT_VERIFIED'

    def shot(title, name, caption, box=None):
        trim = ''
        if box:
            with Image.open(folder/(name+'.png')) as im:
                width,height = im.size
            x1,y1,x2,y2 = box
            assert 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height
            trim = ',trim='+' '.join(f'{v*.75:g}bp' for v in (x1,height-y2,width-x2,y1))+',clip'
        d.frame(title,r'\includegraphics[width=\textwidth,height=4.8cm,keepaspectratio'+trim+r']{assets/integrated-0914/vivado-final/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

    d.frame('Vivado에 같은 원본 연결',paras('VS Code 검사와 실험 전 레포트를 마친 뒤 Vivado를 연다.','설계 Top은 lab2_integrated, 시뮬레이션 Top은 tb_lab2_integrated다. 빈 design.v와 기본 TB는 추가하지 않는다.'),'implementation')
    rows = [
        ('프로젝트 이름과 위치','02-project-name','File → Project → New → Next. 이름은 lab2_integrated. 위치는 자신의 프로젝트 폴더/vivado. Create project subdirectory 해제 → Next.',(28,190,1053,350)),
        ('RTL 프로젝트 선택','03-rtl-project','RTL Project와 Do not specify sources at this time 선택 → Next.',(28,195,700,300)),
        ('정확한 부품 선택','04-part','Parts 검색란에 xc7s75fgga484-1 입력. 정확히 같은 행 선택 → Next. -1IL·-1Q와 구분한다.',(30,202,800,403)),
        ('생성 요약 확인','05-project-summary','lab2_integrated·Spartan-7·fgga484·-1 확인 → Finish.',(27,106,700,300)),
        ('12개 RTL 원본 연결','06-design-sources','Add Sources → Add or create design sources → Next → Add Files. 앞에서 작성한 src의 12개 RTL을 선택한다. 빈 design.v 제외. Copy sources into project 해제 → Finish.',(33,207,812,510)),
        ('통합 테스트벤치 등록','07-simulation-source','Add Sources → Add or create simulation sources → Next → Add Files → sim/tb_lab2_integrated.sv. sim_1과 Include all design sources 유지. Copy sources 해제 → Finish.',(32,210,810,517)),
        ('통합 XDC 등록','08-constraints','Add Sources → Add or create constraints → Next → Add Files → constraints/lab2_integrated.xdc. Copy constraints files into project 해제 → Finish.',(32,211,813,512)),
        ('설계와 시뮬레이션 Top','09-tops','Design Sources의 lab2_integrated, Simulation Sources → sim_1의 tb_lab2_integrated가 굵게 표시된다. 다르면 해당 이름 우클릭 → Set as Top. 캡처에서는 자동 선택되었다.',(267,214,776,384)),
        ('XSim 실행','10-run-simulation','왼쪽 Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration을 기다린다.',(28,423,466,636)),
        ('Run All로 끝까지 실행','11-run-all','기본 1000 ns에서는 checks=37로 검사가 남아 있다. Run → Run All 또는 F3. 테스트벤치의 $finish까지 실행한다.',(463,67,757,287)),
        ('8모드 · 2848개 검사 통과','12-simulation-pass','Tcl Console의 LAB2_INTEGRATED_PASS modes=8 checks=2848, 종료 시각 34326 ns를 확인한다. VS Code와 같은 결과다.',(283,786,620,832)),
        ('전체 파형 비교','13-wave-full','Untitled 1 파형 탭 더블클릭 → Zoom Fit. mode_button의 전환, step_button·sw 입력에 따른 led, 마지막 구간의 세그먼트 스캔과 리셋을 VS Code 파형과 대조한다.',(314,214,1470,610)),
    ]
    for row in rows: shot(*row)
    pin_rows = [
        ('핀 확인 화면 열기','14-elaborated','Open Elaborated Design → OK. 오른쪽 위에서 I/O Planning 선택 → I/O Ports 탭 더블클릭. All ports는 47개다.',(269,629,1120,900)),
        ('LCD 데이터 핀','15-io-lcd','lcd_data 화살표를 펼친다. 비트 0부터 A4·B2·C3·D4·A2·C5·C1·D1이다. 모든 I/O Std는 LVCMOS33이다.',(267,214,1055,530)),
        ('LED 핀','16-io-led','lcd_data를 접고 led를 펼친다. 비트 0부터 N5·M1·M3·M7·N7·M2·M4·L4를 XDC와 대조한다.',(267,214,1055,558)),
        ('자리 선택 핀','17-io-seg-com','led를 접고 seg_com을 펼친다. 비트 0부터 K5·K3·K1·L6·G3·G1·H6·H4다. 활성 자리의 출력은 0이다.',(267,214,1055,585)),
        ('세그먼트 데이터 핀','18-io-seg-data','seg_com을 접고 seg_data를 펼친다. 비트 0부터 H2·J7·J3·J1·E4·E2·F5·F1이다.',(267,214,1055,613)),
        ('스위치 핀','19-io-sw','seg_data를 접고 sw를 펼친다. 비트 0부터 U4·V4·W1·W4·T1·U2·W3·Y1이다.',(267,214,1055,641)),
        ('클록·버튼·LCD 제어 핀','20-io-scalar','sw를 접고 Scalar ports를 펼친다. clk=B6, rst=K4, mode_button=N8, step_button=N4. lcd_e=A6, lcd_rs=G6, lcd_rw=D6. 이름 열의 경계를 끌어 긴 이름까지 확인한다.',(267,214,1150,641)),
        ('합성 실행','21-synthesis-launch','왼쪽 Run Synthesis. Launch runs on local host와 jobs 확인 → OK. 캡처에서는 jobs=4다.',(20,112,486,278)),
        ('합성 완료','22-synthesis-complete','Synthesis successfully completed 확인 → Run Implementation 선택 → OK.',None),
        ('구현 실행','23-implementation-launch','Launch runs on local host와 jobs 확인 → OK. 실행 중에는 RTL·XDC를 수정하지 않는다.',None),
        ('구현 완료','24-implementation-complete','Implementation successfully completed 확인 → Generate Bitstream 선택 → OK.',None),
        ('비트스트림 생성 실행','25-bitstream-launch','Launch runs on local host와 jobs 확인 → OK. 완료 창이 나타날 때까지 기다린다.',None),
        ('비트스트림 생성 완료','26-bitstream-complete','Bitstream Generation successfully completed 확인. Open Implemented Design 선택 → OK. Elaborated Design을 닫을지 물으면 Yes.',None),
        ('내부 타이밍 확인','27-timing','Timing 탭 더블클릭 → Design Timing Summary. Setup·Hold의 slack과 Number of Failing Endpoints를 확인한다.',(270,184,1117,420)),
    ]
    for row in pin_rows: shot(*row)
    d.frame('검사 결과와 생성 파일',paras('XSim: 8개 모드, 2848개 검사, 34326 ns 종료. VS Code와 같은 RTL·TB를 사용했다.','생성 파일: vivado/lab2_integrated.runs/impl_1/lab2_integrated.bit.','GUI 합성·구현·bit 생성을 확인했다. 실제 장치 기록·사진·영상은 다음 장의 학생 실험에서 수행한다.'))
    d.frame('타이밍 결과 읽기',paras(f"WNS={proof['wns_ns']:.3f} ns, WHS={proof['whs_ns']:.3f} ns. Setup·Hold 실패 endpoint는 각각 0이다.",'주 클록 제약은 1,000,000 ns이며 보드도 1 kHz로 설정한다. 비동기 입력에는 false path를 적용했다.','외부 출력 지연이 없는 LED·세그먼트·LCD 출력은 내부 타이밍 통과만으로 외부 장치의 타이밍까지 보장되지 않는다.'))
    d.frame('경고를 읽고 기록한다',paras('TIMING-18: 외부 출력 지연이 지정되지 않은 출력 34개가 보고된다. 상수로 고정된 lcd_rw와 나머지 LCD·LED·세그먼트 출력을 구분한다.','CFGBVS-1: 설정 뱅크 전압 속성이 지정되지 않았다. 보드 회로도와 설정 전압을 확인하여 값을 정한다. 경고만 없애려고 임의의 값을 넣지 않는다.','실험 후 레포트에는 경고 이름·원인·실측 범위를 남긴다.'))
