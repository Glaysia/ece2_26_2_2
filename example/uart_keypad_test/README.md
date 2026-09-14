# USB-UART + 숫자 키 테스트

Combo II-DLD / XC7S75-FGGA484-1 전용 테스트 프로젝트. Vivado 2026.1을 사용한다.

- MAIN CLOCK: **F, 50 MHz**. KEYPADS SEL: **아래, Button Switch**.
- 내장 USB Serial Port **9600 baud, 8 data bits, no parity, 1 stop bit**, 흐름 제어 없음. 최초 COM4였으며 재연결 후 COM5로 인식됐다. 실제 포트 번호를 확인한다.
- PC가 `BLABLA\n`을 보내면 FPGA는 LF 수신 뒤 `LB|BLABLA\n`을 반환한다. CR은 무시한다.
- 숫자 키를 누르면 `KP|1\n`~`KP|9\n`, `KP|0\n`을 보낸다. 별표·샵은 `KP|*\n`, `KP|#\n`이다.
- 키는 10 ms 안정 후 한 번 전송하며 길게 눌러도 반복하지 않는다. 동시 키는 물리적 1~9, *, 0, # 순서로 처리한다. 같은 키의 미처리 이벤트는 하나로 합쳐진다.
- 줄 본문은 최대 128바이트다. 초과하면 LF에서 `ERR|LINE_TOO_LONG\n`을 반환한 뒤 다음 줄을 받는다. RX FIFO는 2047바이트이며 무제한 스트리밍용은 아니다. 응답을 받은 뒤 다음 요청을 보내는 방식이 권장된다.
- 키 메시지는 줄 응답 도중에 끼어들지 않는다. 줄 응답과 키 메시지는 같은 UART TX를 사용한다.
- 초기화는 FPGA configuration 직후 자동 수행한다. 숫자 1 키를 리셋에 겸용하지 않는다.

## GPIO에서 UART 파형 보기

- **BDIO 0~7**: 모두 FPGA → PC의 TX(F6) 복제 출력. 응답과 키패드 메시지가 나온다.
- **BDIO 8~15**: 모두 PC → FPGA의 RX(C6) 복제 출력. 외부 UART를 입력받는 핀이 아니라 관찰용 출력이다.
- 16개 핀 모두 **3.3 V LVCMOS 출력**이다. 측정기 GND를 보드 GND에 연결하고 입력 프로브로 관찰한다.
- UART 디코더: **9600, 8N1, LSB first, 반전 없음**. 유휴 HIGH, 1비트 약 104.16 μs. 오실로스코프 시작 설정: 1 ms/div, 하강 에지, 약 1.5 V 트리거. `KP|1\n`은 약 5.2 ms이다.
- BDIO 0~7 중 하나의 하강 에지로 트리거하고 키를 눌러 `KP|숫자\n`을 관찰한다. 기존 UART C6/F6는 그대로 사용한다. `#`도 일반 키이며 사각파 전환 기능은 없다.

제조사 `Xilinx S7 Pin Map.pdf`의 BreadBoard I/O 핀 배정:

| BDIO | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| TX 핀 | F8 | E8 | A7 | G8 | D7 | B7 | G7 | F7 |

| BDIO | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|
| RX 복제 핀 | C8 | D8 | C9 | B8 | A9 | B9 | A10 | B10 |

## 열기 및 실행

`UART.code-workspace`를 연다. `build/vivado/uart_keypad_test.xpr`은 빌드 후 Vivado에서 직접 열 수 있다.

```powershell
New-Item -ItemType Directory -Force build | Out-Null
& C:/AMDDesignTools/2026.1/Vivado/bin/vivado.bat -mode batch -source tools/build.tcl -log build/build.log
& C:/AMDDesignTools/2026.1/Vivado/bin/vivado.bat -mode batch -source tools/program.tcl -log build/program.log
python -m pip install pyserial==3.5
python tools/serial_test.py --port COM4
python tools/serial_test.py --port COM4 --monitor 60
```

`program.tcl`은 이 실행에서 확인한 케이블 `13724327082d01`과 `xc7s75_0`만 대상으로 **SRAM**을 기록한다. 전원을 끄면 사라지며 Flash는 변경하지 않는다. 다른 케이블을 쓰면 `tools/probe.tcl`로 식별자를 확인한다.

## LED 진단

LED[7]: RX FIFO overflow, LED[6]: UART framing error, LED[5]: 초기화 완료, LED[4]: TX busy, LED[3:0]: 마지막 수신 바이트 하위 4비트. 오류 LED는 재configuration 때 초기화된다.

## 핀 근거

- USB RX=C6, TX=F6, clk=B6: 저장소 `legacy/notebook/cpp/Combo II default/Example/usb232/usb232.srcs/constrs_1/new/usb232.xdc`.
- 숫자 1~9, *, 0, # = K4 N8 N4 N1 P6 N6 L5 J2 K2 L7 L1 K6: `legacy/교안 (신 장비)/Lab-02 Data Flow Modeling/HBE Combo II-DLD.pdf` 버튼 핀 표 및 제조사 Full Demo XDC.
- MAIN CLOCK F=50 MHz: 같은 보드 자료의 Clock 제어 블록 표.

## 검증 기록

`sim/tb_uart_keypad.sv`는 실제 직렬선의 비트 중심을 독립적으로 샘플링한다. LF 전 무응답, 빈 줄·CRLF, 연속 줄, 12개 키, hold/bounce, 길이 제한·초과 후 복구를 검사한다.

2026-09-14 검증 결과:

- Icarus 및 Vivado 2026.1 XSim: `UART_KEYPAD_PASS bytes=240`. [Icarus](evidence/icarus.txt), [XSim](evidence/xsim.log).
- GPIO 16개 / 9600 baud 버전 합성·배치배선·bitstream 생성 성공. 50 MHz 내부 타이밍 WNS +9.234 ns, WHS +0.081 ns, 위반 0. [타이밍](evidence/timing.rpt), [I/O 보고서](evidence/io.rpt).
- 기본 50 MHz / 9600 설정을 별도의 직렬선 자극·디코더로 검사해 `LB|U\n` 응답 통과. [9600 검사](evidence/uart-9600-sim.txt). 이전 하드웨어 7/7 기록은 115200 버전 결과이며 9600 실물 재검사 결과가 아니다.
- DRC 오류 0. CFGBVS/CONFIG_VOLTAGE 미지정 경고 1건은 남아 있다. 비동기 입력은 동기화기 앞 false path로 처리했고 UART/LED 출력은 외부 동기식 출력 지연을 지정하지 않았다. [DRC](evidence/drc.rpt).
- 16:10 GPIO 16개 버전을 연결된 `xc7s75_0` SRAM에 주입 완료. startup HIGH 및 DONE=1 확인. GPIO 물리 파형 검증은 아직 완료되지 않았다.
- GPIO 추가 전 버전 COM4 115200 8N1 실제 검사 **7/7 통과**: 기본 응답, 빈 줄, CRLF, 연속 두 줄, 최대 길이, 길이 초과, 다음 줄 복구. [송수신 기록](evidence/serial-loopback.json). GPIO 추가 후에는 PC에서 USB-UART 포트가 사라져 실제 UART 재검사를 수행하지 못했다. GPIO 물리 파형도 측정기에서 별도 확인해야 한다.
- 키패드 12개·hold/bounce는 시뮬레이션 통과. 주입 후 120초 실제 수신 감시에서는 키 메시지가 수신되지 않았다. 사용자의 실제 키 누름 여부는 확인되지 않아 하드웨어 키 검증은 미완료다. [감시 기록](evidence/keypad-monitor.json).

GPIO 16개 / 9600 baud bitstream SHA-256: `8d41e31cea5d335f1cd60e8defd5f7963b950b5882429ec408409ccd8a4c7b61`.

Vivado의 `launch_simulation` 연결 단계가 멈춰, 빌드 스크립트는 Vivado가 생성한 compile/elaborate 스크립트와 독립 `xsim -runall`을 실행한다. PASS 문자열 확인 후에만 합성으로 넘어간다.
