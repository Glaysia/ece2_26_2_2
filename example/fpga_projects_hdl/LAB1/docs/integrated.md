# 버튼과 LCD로 10개 회로 선택

[전체 프로젝트](../README.md) · [Vivado 통합](../vivado_2026_1/11_integrated/README.md) · [CLI 통합](../opensource_cli/integrated/README.md) · [검증](validation.md)

두 통합 프로젝트는 같은 [lab1_integrated.v](../common/rtl/lab1_integrated.v), [버튼 처리](../common/rtl/button_onepulse.v), [LCD 제어](../common/rtl/lcd_modes.v), [자기검사 TB](../common/tb/tb_lab1_integrated.sv), [보드 핀](../common/constraints/lab1_integrated.xdc)을 사용합니다. 디바이스는 `xc7s75fgga484-1`입니다.

## 보드 연결

원본 LCD 실습의 1kHz 클록을 사용합니다. `clk=B6`, `rst=K4(KEY1)`, `mode_button=N8(KEY2)`입니다. KEY1을 누르면 모드 01로 돌아가고 KEY2를 눌렀다 떼면 다음 모드로 진행합니다. 버튼은 active-high입니다. DIP1부터 DIP8까지는 `sw[7]`부터 `sw[0]`, LED1부터 LED8까지는 `led[7]`부터 `led[0]`입니다.

LCD 8비트 버스 `lcd_data[0]`부터 `[7]`까지는 A4/B2/C3/D4/A2/C5/C1/D1, E=A6, RS=G6, RW=D6입니다. DIP 핀은 Y1/W3/U2/T1/W4/W1/V4/U4, LED 핀은 L4/M4/M2/N7/M7/M3/M1/N5입니다. 단일 7세그먼트의 a,b,c,d,e,f,g,dp는 P1/P3/P7/N3/T5/R2/R4/R6입니다. 다른 보드에는 이 XDC를 그대로 쓰지 않습니다.

## 모드별 조작

LED에 쓰지 않는 하위 비트는 0입니다. 통합본은 모드 버튼과 reset을 확보하기 위해 개별 실습의 KEY 입력을 DIP로 옮겼습니다.

| 모드 | LCD 이름 | 입력 | 출력 |
|---|---|---|---|
| <a id="mode-01"></a>01 | AND OR XOR | a=DIP1, b=DIP2 | LED1=AND, LED2=OR, LED3=XOR |
| <a id="mode-02"></a>02 | FULL ADDER | a=DIP1, b=DIP2, cin=DIP3 | LED1=carry, LED2=sum |
| <a id="mode-03"></a>03 | 4 BIT ADDER | a=DIP1–4, b=DIP5–8 | LED1=carry, LED2–5=sum[3:0] |
| <a id="mode-04"></a>04 | 4 BIT SUBTRACT | a=DIP1–4, b=DIP5–8 | LED1=borrow, LED2–5=diff[3:0] |
| <a id="mode-05"></a>05 | 4 BIT COMPARE | a=DIP1–4, b=DIP5–8 | LED1=큼, LED2=같음, LED3=작음 |
| <a id="mode-06"></a>06 | 4 TO 1 MUX | i=DIP1–4, s=DIP7–8 | LED1=i[3-s] |
| <a id="mode-07"></a>07 | 1 TO 8 DEMUX | i=DIP1, s=DIP6–8 | LED1–8, s=0이면 LED1 |
| <a id="mode-08"></a>08 | 8 TO 3 ENCODER | i=DIP1–8, 한 비트만 1 | LED1–3=번호, DIP1→0, DIP8→7 |
| <a id="mode-09"></a>09 | 3 TO 8 DECODER | a,b,c=DIP6,7,8 | abc=0이면 LED8, 7이면 LED1 |
| <a id="mode-10"></a>10 | HEX 7 SEGMENT | bcd=DIP5–8 | 단일 7세그먼트와 LED에 a–dp 패턴 |

## 버튼과 표시 타이밍

`button_onepulse`는 2단 동기화 뒤 20클록 연속 안정된 입력을 받아들입니다. 1kHz에서 약 20ms 디바운스에 동기화 지연이 추가됩니다. 길게 누르는 동안 한 번만 전환하고, 뗀 뒤 다시 누르면 한 번 더 전환합니다. 모드 10 다음은 01입니다.

LCD는 전원 대기 50ms 뒤 `38,38,38,0C,06` 명령으로 8비트·2행·표시 켜짐·자동 증가를 설정합니다. E는 1ms 동안 높고 각 바이트는 최소 4ms 간격입니다. 화면의 첫 줄은 `MODE 01`…`MODE 10`, 두 번째 줄은 회로 이름입니다. 한 화면 갱신 시작 때 모드를 저장하여 두 줄이 다른 모드로 섞이지 않게 합니다. 바뀐 모드는 현재 전송이 끝난 다음 갱신되므로 즉시 표시되지 않을 수 있습니다.

## 사전 검증

TB는 검사 속도를 위해 클록을 10ns로, 디바운스 4클록·전원 대기 5클록으로 줄입니다. 이 값은 TB 인스턴스에서만 재정의하며 합성 top 기본값은 1kHz 보드용입니다. 10개 모드마다 DIP 256개 값을 비교하여 총 2,560개를 검사합니다. 출력 외에도 reset, 버튼 바운스, 길게 누르기, 10→01 순환, LCD 초기 명령과 외부 LCD 버스에서 완성된 두 줄을 검사합니다.

성공 문구는 `LAB1_PASS lab1_integrated cases=2560`입니다. XSim 검증은 72430ns에 끝났습니다. 축소된 TB 시간만으로 실제 LCD의 전기적 연결·전압·실물 표시를 검증했다고 해석하지 않습니다.

## 실제 실험에서 촬영할 내용

reset 직후 MODE 01, KEY2를 눌러 다음 모드로 바뀌는 장면, 길게 눌렀을 때 한 번만 바뀌는 장면, 10→01 순환을 촬영합니다. 각 모드에서 정상·경계 입력 하나씩을 선택해 DIP와 출력이 동시에 보이도록 기록합니다. LCD 화면이 갱신될 시간을 준 뒤 읽습니다. 영상 타임스탬프 10개를 레포트의 모드 표와 연결합니다.

제작 환경의 보드 기록·LCD 실물·사진·영상은 아직 **미수행**입니다.
