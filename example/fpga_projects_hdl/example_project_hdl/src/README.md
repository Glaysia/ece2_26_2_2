# Lab 5: 클록·순차논리·카운터 응용

원본: legacy/Post-lab5_2021440107_이해리.zip의 보고서 PDF, 실험 16~21.
ZIP에는 HDL 파일이 없어 PDF의 코드 이미지와 실험 내용을 기준으로 재작성했다.
기존 src 예제와 Vivado 프로젝트 설정은 변경하지 않았다.

| 실험 | 파일 / top module | 입력 조건 |
|---|---|---|
| 16 카운터 | counter.v / lab5_counter | up=1 증가, up=0 감소 |
| 17 분주기 | clock_divider.v / lab5_clock_divider | clk=100Hz → 100/50/10/2Hz |
| 18 스텝모터 | stepper.v / lab5_stepper | 클록마다 0011→0110→1100→1001 |
| 19 피에조 | tone.v / lab5_piezo | clk=1MHz, 약 294Hz |
| 20 피아노 | piano.v + tone.v / lab5_piano | clk=1MHz, key[7:0]=도~높은 도 |
| 21 시계 | watch.v / lab5_watch | clk=1kHz, 00:00~59:59, 4자리 스캔 |

모든 모듈은 active-high 비동기 reset이다. rst를 먼저 인가한다.
피아노는 원본의 정수 분주값을 음계 주파수 기준 반올림값으로 정리했다.
무입력·동시 키 입력은 무음이며, 키 변경 시 첫 반주기는 짧아질 수 있다.
시계의 세그먼트는 {a,b,c,d,e,f,g,dp} active-high, 자리 선택은 active-low이다.
원본과 같은 보드인지는 핀맵·극성·클록 설정을 별도로 확인해야 한다.
모터는 FPGA 핀에 직접 연결하지 않고 보드의 모터 구동 회로를 사용한다.

## 시뮬레이션

이 폴더에서 실행한다. Icarus는 이번 검증용이며 에디터 설정을 변경하지 않는다.

```powershell
iverilog -g2012 -Wall -s tb_lab5 -o lab5_sim counter.v clock_divider.v stepper.v tone.v piano.v watch.v tb_lab5.sv
vvp lab5_sim
```

성공하면 ALL LAB5 CHECKS PASSED가 출력되며 lab5.vcd가 생성된다.
테스트벤치의 클록은 빠른 논리 검증용 10ns이고, 시계는 4클록을 가상 1초로 사용한다.
이 VCD의 시간축을 실제 보드의 Hz나 실제 경과시간으로 보고하지 않는다.
카운터 순환·분주비·모터 순서·8음의 분주값·무음·시계 1시간 순환을 검사한다.
실물 동작과 계측 결과는 아직 검증하지 않았다.

## 보고서 작성 시 구분

- 원본 PDF와 영상은 2022년 실험의 기록이다.
- 새 코드의 시뮬레이션은 재작성한 설계의 검증 결과다.
- 새 코드의 보드 시연은 별도로 수행해야 하며 원본 영상으로 대체해 주장하지 않는다.
