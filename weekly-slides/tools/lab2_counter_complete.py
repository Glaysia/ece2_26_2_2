"""First LAB2 manual, backed by the VS Code and Vivado GUI session."""
from lab2_counter_vscode import d
from lab2_series import paras, steps

d.pages[0]=d.pages[0].replace('카운터: VS Code','카운터: VS Code → Vivado').replace('첫 카운터의 VS Code 단계 확인용 자료','첫 카운터 · Vivado 2026.1 실습')
d.pages[0]=d.pages[0].replace('소스 작성 → 기능 시뮬레이션 → 파형 확인','소스 작성 → 시뮬레이션 → 비트스트림 생성')
d.pages[1]=d.pages[1].replace(r'\navlink{reports}',r'\navlink{implementation}{Vivado 구현과 bit 생성}\par\vspace{0.4cm}\navlink{reports}')
d.pages[1]=d.pages[1].replace(r'\end{frame}',r'\par\vspace{0.4cm}\navlink{after-report}{실험 후 레포트}\end{frame}')

def shot(title,name,caption,box=(200,120,1288,820)):
    if box == (200,120,1288,820):
        box = {
            '02-project-name':(230,325,1255,472),
            '03-project-type':(233,326,1255,432),
            '04-part':(236,330,1250,526),
            '05-summary':(234,238,1000,421),
            '07-design-category':(349,365,900,465),
            '08-add-files':(349,360,1135,576),
            '10-rtl-import':(349,362,1135,665),
            '11-sim-category':(349,365,900,465),
            '12-tb-import':(349,365,1135,675),
            '13-xdc-category':(349,365,900,465),
            '14-xdc-import':(349,364,1135,666),
        }.get(name, box)
    x1,y1,x2,y2=box
    trim=' '.join(f'{v*.75:g}bp' for v in [x1,942-y2,1486-x2,y1])
    d.frame(title,r'\includegraphics[width=\textwidth,height=4.9cm,keepaspectratio,trim='+trim+r',clip]{assets/vivado-01-0911/'+name+r'.png}\par\vspace{0.18cm}'+paras(caption))

d.frame('Vivado에서 이어서 구현',steps('VS Code에서 작성한 RTL·TB·XDC를 모두 저장한다.','Vivado 2026.1을 실행한다.','새 RTL 프로젝트에 작성한 파일을 등록한다.','같은 테스트벤치로 시뮬레이션한 뒤 bit를 만든다.'),'implementation')
shot('New Project','01-start','Quick Start → New Project를 누른다.',(40,105,980,850))
shot('프로젝트 이름과 위치','02-project-name','이름은 lab2_counter. 자신의 실습 폴더 아래 vivado 폴더를 지정한다. Create project subdirectory 해제 → Next.')
shot('RTL Project 선택','03-project-type','RTL Project와 Do not specify sources at this time을 선택한 채 Next. 파일은 프로젝트 생성 후 직접 등록한다.')
shot('정확한 FPGA 부품 선택','04-part','Parts 검색란에 xc7s75fgga484-1 입력 → 정확히 -1로 끝나는 행 선택 → Next. -1IL·-1Q와 구분한다.')
shot('생성 전 마지막 확인','05-summary','Spartan-7, fgga484, Speed Grade -1을 확인하고 Finish.')
shot('Add Sources','06-empty-project','왼쪽 Project Manager → Add Sources를 누른다. 아래 화면은 파일 등록을 마친 예시다.',(0,100,780,420))
shot('RTL은 Design Sources','07-design-category','Add or create design sources 선택 → Next.')
shot('Add Files 선택','08-add-files','Add Files를 누르고 VS Code 프로젝트의 src 폴더로 이동한다.')
shot('RTL 세 파일 선택','09-rtl-files','counter4.v·input_frontend.v·lab2_counter.v를 함께 선택하고 OK.',(68,198,1420,830))
shot('원본 RTL을 참조하도록 등록','10-rtl-import','세 파일 이름 확인 → Copy sources into project는 해제 → Finish. 이후 VS Code 수정 내용은 저장 후 Vivado에 반영한다.')
shot('TB는 Simulation Sources','11-sim-category','Add Sources → Add or create simulation sources → Next → Add Files.')
shot('테스트벤치 등록','12-tb-import','sim/tb_counter4.sv 등록 → Include all design sources for simulation 유지 → Finish.')
shot('XDC는 Constraints','13-xdc-category','Add Sources → Add or create constraints → Next → Add Files.')
shot('핀 제약 파일 등록','14-xdc-import','constraints/lab2_counter.xdc를 등록한다. Copy constraints files into project 해제 → Finish.')
shot('시뮬레이션 최상위 지정','15-sim-set-top','Simulation Sources → sim_1 → tb_counter4 우클릭 → Set as Top. 이미 굵은 이름이면 지정된 상태이며 메뉴가 비활성화된다.',(265,280,790,725))
shot('두 최상위 모듈 구분','16-tops','Simulation Sources의 굵은 이름은 tb_counter4. 오른쪽 Project Summary의 Top module name은 lab2_counter.',(265,148,1486,665))
shot('Behavioral Simulation 실행','17-run-behavioral','왼쪽 Run Simulation → Run Behavioral Simulation을 누른다.',(0,280,780,665))
shot('36개 검사 완료','18-sim-finish','checks=36, Sim Time=356 ns. VS Code 실행 결과와 비교한다. $finish 위치에서 멈추는 것은 정상이다.',(265,145,1486,942))
shot('전체 파형 보기','19-wave-fit','파형 탭을 선택하고 우상단 사각형으로 확대한다. Zoom Fit을 눌러 0~356 ns 전체 구간을 확인한다.',(310,148,1486,475))
d.frame('파형과 시뮬레이션 로그',paras('GUI 실행 로그에도 LAB2_PASS counter4 checks=36과 356 ns 종료가 남는다.','value는 16진수로 표시된다. a~f는 10~15다. 증가·감소·유지·초기화 구간을 VS Code 파형과 대조한다.','코어 테스트벤치의 통과와 실제 보드 버튼·LED 동작 확인은 별개다.'))
shot('Generate Bitstream','06-empty-project','왼쪽 Generate Bitstream을 누른다. 합성·구현 실행 여부를 물으면 Yes. Launch runs on local host 선택 → OK.',(0,610,267,917))
d.frame('합성 → 구현 → bit 생성',steps('합성은 RTL을 FPGA 논리 소자로 변환한다.','구현은 소자를 배치하고 신호를 배선한다.','마지막으로 FPGA에 기록할 .bit 파일을 생성한다.','우상단 진행 상태와 하단 Design Runs를 확인하며 기다린다.','실패하면 Messages의 첫 Error를 확인한다. 완료 전 같은 작업을 다시 실행하지 않는다.'))
shot('비트스트림 생성 완료','23-bit-complete','Design Runs의 impl_1 상태가 write_bitstream Complete!인지 확인한다. 이번 GUI 실행은 2026-09-11에 완료했다.',(267,668,1486,843))
d.frame('생성된 파일 찾기',paras('프로젝트 폴더 → lab2_counter.runs → impl_1 → lab2_counter.bit','이 파일이 FPGA에 기록할 비트스트림이다. .xpr는 Vivado 프로젝트 설정 파일이다.','파일 탐색기에서 수정 시각을 확인한다. 소스를 수정했다면 합성·구현·bit 생성까지 다시 실행해야 한다.'))
d.frame('이번 구현의 경고 해석',paras('상위 LED 4개는 코드에서 0으로 고정하므로 상수 출력 경고가 발생한다.','TIMING-18 경고는 외부 입출력 지연 제약이 없는 항목이다. 버튼은 비동기 입력이고 LED는 외부 클록으로 샘플링되는 인터페이스가 아니다.','1 kHz 클록의 내부 경로 타이밍과 DRC를 확인한다. 이 결과를 모든 외부 인터페이스의 타이밍 검증 완료로 해석하지 않는다.'))
shot('구현 후 타이밍 확인','24-timing','Open Implemented Design → Timing. Setup·Hold의 Failing Endpoints가 0인지 확인한다. 현재 WHS는 0.122 ns다.',(270,630,1486,911))
shot('DRC 결과 읽기','25-drc','DRC 탭을 연다. 이번 결과는 오류 0개, CFGBVS-1 경고 1개다. 구성 뱅크 전압 속성 미지정 경고이며 bit 생성은 완료됐다.',(270,630,1486,911))
d.frame('CFGBVS 경고를 수정하려면',paras('CFGBVS와 CONFIG_VOLTAGE는 구성 뱅크의 실제 보드 배선·전압에 맞춰 지정하는 속성이다.','일반 I/O의 LVCMOS33 설정만 보고 구성 뱅크 전압도 같다고 추정하지 않는다. 보드 회로도에서 확인한 뒤 XDC에 반영한다.','이번 제작 검증에서는 이 속성을 임의로 추가하지 않았다. 레포트에는 남은 경고와 확인 범위를 함께 적는다.'))
shot('LED 핀 확인','26-io-ports','Window → I/O Ports → 패널 확대 → Expand All. led[0..7]의 Package Pin과 LVCMOS33을 XDC와 대조한다.',(268,148,1082,535))
shot('스위치·버튼·클록 핀 확인','26-io-ports','sw[0]=U4, button=N8, clk=B6, rst=K4. sw[0]은 보드 DIPSW8에 대응한다. 클록은 1 kHz로 설정한다.',(268,530,1082,899))
d.frame('보드에서 실행하는 순서',steps('Combo II-DLD S75의 전원·JTAG 연결을 확인하고 메인 클록을 1 kHz로 맞춘다.','Vivado 왼쪽 Open Hardware Manager를 누른다.','Open Target → Auto Connect를 선택한다.','검색된 xc7s75 장치를 우클릭 → Program Device.','Bitstream file에서 lab2_counter.bit 선택 → Program.'))
d.frame('기록 후 동작 확인',steps('리셋 입력(K4)을 활성화해 하위 LED 4개가 0인지 확인한다.','방향 입력 sw[0](DIPSW8)을 0으로 두고 N8 버튼을 눌렀다 놓는다. 한 번에 1씩 증가해야 한다.','15에서 한 번 더 누르면 0으로 순환하는지 본다.','sw[0]=1로 바꾸고 버튼을 눌러 감소와 0→15 순환을 확인한다.','버튼을 길게 누르면 연속 증가하지 않고, 놓았다 다시 눌러야 다음 값으로 바뀌는지 확인한다.'))
d.frame('실험 후 레포트',steps('Vivado의 소스 계층·시뮬레이션 PASS·파형을 넣고 VS Code 결과와 비교한다.','사용한 부품·핀·1 kHz 클록 제약과 합성·구현 결과를 기록한다.','write_bitstream Complete 화면, 생성 파일, 남은 경고와 해석을 첨부한다.','실제 보드의 초기화·증가·감소·순환 동작을 사진과 영상으로 남긴다.','자신의 GitHub 저장소에 소스·레포트·사진·영상 링크를 올리고 README에서 연결한다.'),'after-report')
d.frame('제작 검증 범위',paras('완료: VS Code와 Vivado에서 동일 코어 테스트벤치 36개 검사 통과, 356 ns 종료.','완료: xc7s75fgga484-1 합성·배치·배선·비트스트림 생성, 내부 타이밍 및 핀 배치 확인.','이 자료의 보드 기록·사진·영상 단계는 학생 실험 절차다. 실제 장치 기록과 물리 동작은 이번 제작 검증에 포함되지 않았다.'))

if __name__=='__main__':
    print(d.write('05.LAB2_01_COUNTER_VIVADO.tex','LAB2 카운터 · VS Code → Vivado'))
