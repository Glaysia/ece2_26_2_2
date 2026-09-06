# Lab 5: 클록·순차논리·카운터 응용

원본: legacy/Post-lab5_2021440107_이해리.zip의 보고서 PDF, 실험 16~21.
ZIP에는 HDL 파일이 없어 PDF의 코드 이미지와 실험 내용을 기준으로 재작성했다.
실험 모듈은 공통 top_main에서 선택하여 호출한다. Vivado 프로젝트 설정은 별도로 등록해야 한다.

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
iverilog -g2012 -Wall -s tb_top_main -o top_sim top_main.v counter.v clock_divider.v stepper.v tone.v piano.v watch.v tb_top_main.sv
vvp top_sim
```

테스트벤치는 `tb_top_main.sv` 하나만 사용하며, `top_main`에서 선택한 실험을 실행하고 `top_main.vcd`를 생성한다.
테스트벤치의 클록은 빠른 논리 관찰용 10ns이다.
이 VCD의 시간축을 실제 보드의 Hz나 실제 경과시간으로 보고하지 않는다.
이 테스트는 파형 관찰용이며 전체 실험의 자동 통과 판정을 수행하지 않는다.
실물 동작과 계측 결과는 아직 검증하지 않았다.

## 보고서 작성 시 구분

- 원본 PDF와 영상은 2022년 실험의 기록이다.
- 새 코드의 시뮬레이션은 재작성한 설계의 검증 결과다.
- 새 코드의 보드 시연은 별도로 수행해야 하며 원본 영상으로 대체해 주장하지 않는다.



## 공통 top에서 실험 선택

- 빈 파일의 오타 이름 `tob_main.v`를 `top_main.v`로 정리했다.
- `top_main.v` 상단의 `EXPERIMENT` 선언 중 원하는 번호 **한 줄만** 주석 해제한다. 기본값은 16이다.
- Vivado Design Sources에 top과 모든 하위 설계 파일을 등록하고 설계 top을 `top_main`으로 고정한다. 테스트벤치는 Simulation Sources에 등록한다.
- `generate if`는 선택한 실험의 회로만 생성한다. 선택하지 않은 출력은 0, FND 자리 선택은 꺼짐 값으로 고정한다.
- 실제 입력 클록은 실험별 조건에 맞춘다. 피에조·피아노의 `TONE_CLK_HZ`와 시계의 `WATCH_CLK_HZ`는 실제 클록 주파수와 일치해야 한다. 파라미터 변경 자체가 입력 클록을 분주하지는 않는다.
- 공통 top의 외부 포트에 맞는 검증된 XDC가 필요하다. 사용하지 않는 출력도 외부 포트로 남으므로 핀·I/O 규격 검사를 생략하면 안 된다. 현재 변경만으로 보드 다운로드 준비가 완료된 것은 아니다.
- Vivado의 별도 파라미터 override가 소스의 선택을 덮어쓰지 않는지 확인하고, 변경 후 합성·구현·비트스트림 생성을 다시 실행한다.

### 선택한 실험만 파형 확인

시뮬레이션 top은 `tb_top_main`으로 선택한다. 테스트벤치가 `top_main`의 실험 번호를 그대로 사용한다.

`top_main.vcd`를 열어 `dut` 아래의 선택한 회로를 관찰한다. 10ns 주기의 가속 클록으로 reset 이후 10100클록을 실행하며, 중간에 up과 key를 바꾼다. 이 테스트는 파형 관찰용이지 자동 통과 판정용이 아니다.
