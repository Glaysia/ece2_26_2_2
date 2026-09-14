"""Circuit-specific teaching material, derived from the checked-in RTL and TB."""
from lab2_intro import paras, steps, table


def before_code(d, p):
    top=p['top']
    if top=='lab2_integrated':
        from lab2_integrated_explanations import architecture
        architecture(d)
    if top=='piso4':
        d.frame('네 비트를 저장하고 한 비트씩 읽는다', paras('PISO는 Parallel In, Serial Out이다. load=1인 상승 에지에서 data_in의 네 비트를 value에 한 번에 저장한다.', 'serial_out은 항상 value[3]이다. 먼저 현재 MSB를 읽고, enable=1인 다음 상승 에지에서 {value[2:0], 0}으로 이동한다.', '입력을 bit 3에 넣었던 앞 실험과 달리, 이번에는 저장값을 bit 3 방향으로 옮기고 bit 0을 0으로 채운다.'))
        d.frame('PISO의 제어 우선순위', table(['rst','load','enable','다음 value'], [('1','무관','무관','0'),('0','1','무관','data_in'),('0','0','1','{이전 value[2:0], 0}'),('0','0','0','유지')])+paras('load와 enable이 모두 1이면 load가 우선이다. serial_out은 별도의 출력 레지스터가 아니라 저장값의 MSB를 연결한 선이다.'))
        d.frame('1010을 읽는 정확한 시점', table(['관찰 시점','value','serial_out'], [('load 직후, 첫 shift 전','1010','1'),('첫 shift 후','0100','0'),('둘째 shift 후','1000','1'),('셋째 shift 후','0000','0'),('넷째 shift 후','0000','0')])+paras('네 비트 1,0,1,0을 읽으려면 각 shift 에지 전에 출력값을 기록한다. shift 뒤에만 네 번 읽으면 첫 비트를 놓친다.'))
    elif top=='moore_cycle':
        d.frame('Moore: 상태 자체가 출력이다', paras('value는 2비트 상태 레지스터이면서 출력이다. S0=00, S1=01, S2=10으로 이름을 붙인다.', 'rst가 0일 때 enable과 advance가 모두 1인 상승 에지에서만 다음 상태로 간다.', 'advance만 바꾸고 유효한 상승 에지를 주지 않으면 출력은 그대로다. 다음 상태가 입력에 의존하더라도 출력이 상태에만 의존하면 Moore다.'))
        d.frame('세 상태의 순환과 유지', table(['현재 상태','enable AND advance = 1','그 외'], [('S0 / 00','S1 / 01','S0'),('S1 / 01','S2 / 10','S1'),('S2 / 10','S0 / 00','S2')])+paras('rst=1이면 다른 조건보다 먼저 00으로 초기화한다. case의 default는 10뿐 아니라 11도 처리하지만, 그 분기는 enable AND advance가 1일 때만 실행된다.'))
        d.frame('상태 비트 수와 회로 동작', paras('2비트로 네 값을 표현할 수 있지만 이 회로의 정상 순환은 세 상태다. 단순 2비트 증가 카운터와 같지 않다.', 'case는 이전 상태를 읽고 <=로 다음 상태를 예약한다. 00 → 01 → 10 → 00의 각 화살표에 유효한 클록 에지가 하나씩 필요하다.', '보드의 N8 버튼은 clk가 아니라 enable 펄스를 만든다. SW1은 advance이며 두 제어를 구분한다.'))
    elif top=='mealy_toggle':
        d.frame('Mealy: 상태와 입력으로 출력 계산', paras('state는 상승 에지에서 바뀌는 1비트 레지스터다. value는 state와 bit_in을 읽는 조합 출력이다.', 'enable=1, bit_in=1인 상승 에지마다 state를 반전한다. bit_in=0이면 상태는 유지한다.', 'enable=0은 상태 전이만 멈춘다. bit_in을 바꾸면 상태가 그대로여도 value는 달라질 수 있다.'))
        d.frame('상태 전이 표와 출력 표를 구분', table(['현재 state','bit_in','value','enable=1 에지 뒤 state'], [('S0 / 0','0','00','S0'),('S0 / 0','1','10','S1'),('S1 / 1','0','00','S1'),('S1 / 1','1','01','S0')])+paras('표의 value는 현재 상태 기준이다. 입력 1을 유지하고 에지를 지나면 상태가 바뀌므로 출력도 다시 계산된다. rst=1인 에지는 state=0이 우선이다.'))
        d.frame('리셋인데 출력이 0이 아닐 수 있다', paras('rst는 state를 초기화한다. assign value에는 rst 조건이 없다.', 'bit_in=1인 채 리셋 에지를 지나면 state=0, value=10이다. {state,value}=010이 정상 기대값이다.', 'bit_in을 0으로 내려야 value=00이 된다. 이 동작을 TB의 마지막 두 검사와 대조한다.'))
    elif top=='segment_scan8':
        d.frame('여덟 자리를 시간으로 나누어 켠다', paras('digits는 8개의 4비트 숫자를 묶은 32비트 입력이다. index=0은 가장 낮은 4비트, index=7은 가장 높은 4비트를 선택한다.', 'index는 3비트라 7 다음 증가에서 0으로 순환한다. nibble = digits >> (index * 4)의 결과를 4비트에 대입하여 해당 숫자를 얻는다.', 'select는 논리적인 active-high 자리 선택이다. 실제 COM 핀의 순서와 극성은 보드 모듈에서 변환한다.'))
        d.frame('켜기와 blank 구간', table(['이전 blank','enable','에지 뒤 동작'], [('1','1','같은 index 활성화, blank=0'),('0','1','다음 index 준비, blank=1'),('무관','0','index와 blank 유지')])+paras('리셋은 index=0, blank=1로 시작한다. blank 동안 select=00이라 모든 자리가 꺼지고 다음 숫자의 세그먼트 값이 준비된다.'))
        d.frame('1 kHz에서 자리당 62.5 Hz', paras('보드 모듈은 enable을 항상 1로 연결한다. 한 자리의 활성 1 ms와 blank 1 ms를 합쳐 2 ms다.', '8자리 순회는 16 ms이므로 각 자리의 반복 주파수는 1 / 0.016 = 62.5 Hz다. 각 자리는 16 ms 중 1 ms 켜진다.', 'TB는 유지 조건도 검사하기 위해 enable을 중간에 0으로 내린다. TB의 파형 길이를 실제 보드 스캔 주기로 그대로 해석하지 않는다.'))
        d.frame('숫자와 물리 핀의 순서', paras('segments[7:0]은 a,b,c,d,e,f,g,dp 순서다. 예를 들어 0은 FC, 1은 60이며 dp는 0으로 꺼져 있다.', '보드의 seg_data는 segments를 그대로 전달한다. seg_com은 자리 순서를 뒤집고 반전한다.', 'index=0이면 COM[7]만 0이라 seg_com=7F다. 다음 자리는 BF, 그다음 DF다. blank에서는 FF로 모두 꺼진다.'))


def before_tb(d,p):
    top=p['top']
    if top=='lab2_integrated':
        from lab2_integrated_explanations import testbench
        testbench(d)
    if top=='piso4':
        d.frame('TB는 모든 4비트 입력을 검사한다', paras('word=0부터 15까지 반복한다. 각 word에서 load 우선, hold, 직렬 출력 4개, 네 번 shift 후 0 채움을 검사한다.', '한 word당 7개 검사 × 16개 입력 + 처음 리셋 + 마지막 리셋 우선 = 114개다.', 'TB는 MSB를 먼저 비교한 뒤 step으로 이동한다. 같은 시각에 hold 검사와 첫 직렬 출력 검사가 함께 실행될 수 있다.'))
        d.frame('입력 A가 나오는 파형 구간', table(['시각','관찰'], [('616 ns','A 병렬 load 검사'),('626 ns','hold와 첫 serial bit=1 검사'),('636 ns','둘째 bit=0 검사'),('646 ns','셋째 bit=1 검사'),('656 ns','넷째 bit=0 검사'),('666 ns','네 번 shift 후 value=0')])+paras('TB 전체 종료는 976 ns다. 위 시각은 반복문의 word=10 구간이며 첫 word=0 구간과 혼동하지 않는다.'))
    elif top=='moore_cycle':
        d.frame('TB 첫 순환의 검사 시각', table(['검사 시각','자극','value'], [('6 ns','reset','00'),('7 ns','advance만 1로 변경','00 유지'),('16 ns','유효 에지','01'),('26 ns','advance=0','01 유지'),('36 ns','enable=0','01 유지'),('46 ns','두 제어 모두 1','10'),('56 ns','다음 유효 에지','00')]))
        d.frame('네 번 반복하고 비영 상태에서 리셋', paras('첫 순환의 다섯 에지 검사를 총 네 번 반복한다. 마지막 순환의 00 복귀 검사는 206 ns다.', '215 ns 에지에서 다시 01로 간 뒤 rst=1을 설정한다. 226 ns에 00 초기화를 검사한다.', '처음 2개 + 순환 5개 × 4회 + 마지막 리셋 1개 = 23개 검사다. 7 ns 검사는 클록 사이 입력 변화가 출력을 바꾸지 않는지 확인한다.'))
    elif top=='mealy_toggle':
        d.frame('클록 사이와 에지 뒤를 함께 검사', table(['검사 시각','자극 / 결과','{state,value}'], [('6 ns','reset, 입력 0','000'),('7 ns','입력만 1','010'),('16 ns','enable=0 유지','010'),('26 ns','enable=1 전이','101'),('27 ns','입력만 0','100'),('36 ns','입력 0 상태 유지','100')]))
        d.frame('전이·리셋 뒤의 조합 출력', table(['검사 시각','자극 / 결과','{state,value}'], [('37 ns','S1에서 입력만 1','101'),('46 ns','S0로 전이','010'),('56 ns','S1로 다시 전이','101'),('66 ns','입력 1인 채 리셋','010'),('67 ns','입력만 0','000')])+paras('총 11개 검사다. 7·27·37·67 ns는 에지 사이 출력 변화를 비교하므로 파형을 상승 에지만 찍어서 설명하지 않는다.'))
    elif top=='segment_scan8':
        d.frame('TB는 0–F와 자리 순서를 검사한다', paras('digits=76543210에서 0–7, digits=FEDCBA98에서 8–F를 읽는다. 각 묶음마다 여덟 자리를 두 바퀴 돈다.', '한 자리에서 index, one-hot 선택, 숫자 패턴, 활성 유지, blank, blank 유지의 여섯 항목을 검사한다.', '2묶음 × 2바퀴 × 8자리 × 6개 + 처음/마지막 리셋 2개 = 194개다. 전체 종료는 1306 ns다.'))
        d.frame('첫 두 자리의 파형을 읽는다', table(['검사 시각','index','select','동작'], [('6 ns','0','00','리셋 blank'),('16 ns','0','01','숫자 0 활성, segments=FC'),('26 ns','0','01','enable=0 활성 유지'),('36 ns','1','00','다음 자리 준비'),('46 ns','1','00','enable=0 blank 유지'),('56 ns','1','02','숫자 1 활성, segments=60')])+paras('blank에서도 segments는 다음 숫자를 나타낼 수 있다. 꺼짐 여부는 segments=0이 아니라 자리 선택 select=0으로 판단한다.'))


def after_simulation(d,p):
    top=p['top']
    if top=='lab2_integrated':
        from lab2_integrated_explanations import waveform
        waveform(d)
    content={
        'piso4':('PISO 파형·수정 실험 해설', ['파형에 clk·rst·load·enable·data_in·value·serial_out을 추가한다. value는 2진수로 표시하면 비트 이동을 읽기 쉽다.', 'assign serial_out = value[3]을 value[0]으로 바꾸면 word=1의 첫 출력 검사인 86 ns에서 실패한다. 기대값은 MSB=0, 변경 회로의 출력은 LSB=1이다.', 'TB를 바꾸지 않고 RTL을 원복한다. 114개 PASS와 976 ns 종료를 확인하고 정상·변경·원복의 출력 순서를 비교한다.']),
        'moore_cycle':('Moore 파형·수정 실험 해설', ['파형에 clk·rst·enable·advance·value를 추가한다. value를 2진수로 표시하고 7·16·26·36·46 ns를 비교한다.', "2'b01의 다음 상태를 2'b10에서 2'b00으로 바꾸면 46 ns의 S1 to S2 검사가 실패한다. 기대 상태는 10, 변경된 상태는 00이다.", 'RTL 원복 뒤 23개 PASS와 226 ns 종료를 확인한다. enable=0과 advance=0이 각각 상태를 유지하는 근거를 설명한다.']),
        'mealy_toggle':('Mealy 파형·수정 실험 해설', ['파형에 clk·rst·enable·bit_in·state·value를 추가한다. 6–16 ns와 26–37 ns를 확대하여 입력 변화와 상태 전이를 분리한다.', '입력 1일 때 두 상태의 출력 01과 10을 서로 바꾸면 7 ns의 S0 input changes between clocks 검사가 실패한다. 기대값은 {state,value}=010, 변경값은 001이다.', 'RTL 원복 뒤 11개 PASS와 67 ns 종료를 확인한다. 입력 1인 채 리셋했을 때 value=10인 이유도 레포트에 적는다.']),
        'segment_scan8':('스캔 파형·수정 실험 해설', ['clk·rst·enable·digits·index·select·segments를 추가한다. index는 정수, select와 segments는 16진수로 보면 표와 비교하기 쉽다.', "select 식의 blank ? 8'h00 : 부분을 제거하면 6 ns의 reset blanks digit zero 검사가 먼저 실패한다. 기대 select=00 대신 01이 나온다.", '이 변형은 자리 사이 blank뿐 아니라 리셋 blank도 없앤다. 첫 실패가 왜 리셋 검사인지 설명하고 원복 뒤 194개 PASS·1306 ns 종료를 확인한다.'])}
    if top in content:
        title,words=content[top];d.frame(title,paras(*words))


def board_check(d,p):
    top=p['top']
    if top=='lab2_integrated':
        from lab2_integrated_explanations import board
        board(d)
    if top=='piso4':
        d.frame('PISO 보드 조작 순서', table(['스위치 / 버튼','LED[7:0]'], [('SW1..4=1010, SW8=1, N8','A1'),('SW8=0, N8 한 번','40'),('N8 한 번 더','81'),('N8 한 번 더','00'),('N8 한 번 더','00')])+paras('상위 네 LED는 value, LED0은 직렬 출력이다. load 후 shift 전에 LED0=1을 먼저 읽고 이후 0,1,0을 관찰한다.'))
    elif top=='moore_cycle':
        d.frame('Moore 보드 조작 순서', steps('K4로 초기화한다. LED[1:0]=00.', 'SW1=1로만 바꾼다. N8을 누르지 않으면 00 유지.', 'N8을 누르고 놓는다. 01로 전이.', 'SW1=0에서 N8을 누르고 놓는다. 01 유지.', 'SW1=1로 바꾸고 N8을 두 번 누르고 놓는다. 10 → 00.'))
    elif top=='mealy_toggle':
        d.frame('버튼 없이 출력이 바뀌는 장면', table(['조작','LED[2:0]'], [('K4 초기화, SW1=0','000'),('SW1=1, N8 누르지 않음','010'),('N8 한 번','101'),('SW1=0, N8 누르지 않음','100'),('SW1=0에서 N8 한 번','100'),('SW1=1 후 N8 한 번','010')])+paras('LED2는 state, LED[1:0]은 value다. 실제 SW1은 동기화 회로를 거친다. 버튼 없이 출력이 바뀌지만 물리 스위치 변화와 지연 없이 즉시 같아지는 것은 아니다.'))
    elif top=='segment_scan8':
        d.frame('장비에서 확인할 순서', steps('주 클록을 1 kHz로 맞추고 K4로 초기화한다.', 'SW1..4를 1001로 정한다. COM[7]부터 9,1,2,3,4,5,6,7을 확인한다.', 'SW1..4를 바꿔 첫 자리만 변하는지 확인한다. N8은 스캔 진행에 필요하지 않다.', 'LED[2:0]은 현재 index다. 빠른 변화를 눈으로 모두 구분할 수 있다고 가정하지 않는다.', '카메라 줄무늬나 일부 자리 누락은 촬영 주기와 스캔 주기의 차이도 확인한다. 정상 숫자 사진과 입력 변경 영상을 함께 남긴다.'))
