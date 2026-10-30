# 소스 통합 기록

[메인 목차](../README.md) · [파일 출처·해시](source-inventory.json)

2026-10-30에 공개 리포 43개의 기본 브랜치를 확인하고, 메인 저장소 한 곳으로 소스를 모았다. 기존 메인 커밋은 `4be3cdfeeee97ebf5fe5da5e83b66681d08c6114`다.

## 기존 저장소와 새 위치

| 기존 저장소 | 가져온 커밋 | 통합 위치 |
|---|---|---|
| `ece2_474` | `dd94f01047ae` | [c/stm32](../c/stm32/README.md) |
| `fpga-lab-example-legacy-01-logic-gates` | `9055c8002ec5` | [verilog/variants/lab1_legacy/01_logic_gates](../verilog/variants/lab1_legacy/01_logic_gates/README.md) |
| `fpga-lab-example-legacy-02-full-adder` | `0fe260d29984` | [verilog/variants/lab1_legacy/02_full_adder](../verilog/variants/lab1_legacy/02_full_adder/README.md) |
| `fpga-lab-example-legacy-03-adder4` | `14578fedf93b` | [verilog/variants/lab1_legacy/03_adder4](../verilog/variants/lab1_legacy/03_adder4/README.md) |
| `fpga-lab-example-legacy-04-subtractor4` | `6383aa022813` | [verilog/variants/lab1_legacy/04_subtractor4](../verilog/variants/lab1_legacy/04_subtractor4/README.md) |
| `fpga-lab-example-legacy-05-comparator4` | `d8e0f25d8058` | [verilog/variants/lab1_legacy/05_comparator4](../verilog/variants/lab1_legacy/05_comparator4/README.md) |
| `fpga-lab-example-legacy-06-mux4to1` | `80d65af6339a` | [verilog/variants/lab1_legacy/06_mux4to1](../verilog/variants/lab1_legacy/06_mux4to1/README.md) |
| `fpga-lab-example-legacy-07-demux1to8` | `2e2ab8cf9647` | [verilog/variants/lab1_legacy/07_demux1to8](../verilog/variants/lab1_legacy/07_demux1to8/README.md) |
| `fpga-lab-example-legacy-08-encoder8to3` | `7f88377d78cf` | [verilog/variants/lab1_legacy/08_encoder8to3](../verilog/variants/lab1_legacy/08_encoder8to3/README.md) |
| `fpga-lab-example-legacy-09-decoder3to8` | `e4d672566606` | [verilog/variants/lab1_legacy/09_decoder3to8](../verilog/variants/lab1_legacy/09_decoder3to8/README.md) |
| `fpga-lab-example-legacy-10-seven-segment` | `ccd38e3159da` | [verilog/variants/lab1_legacy/10_seven_segment](../verilog/variants/lab1_legacy/10_seven_segment/README.md) |
| `fpga-lab-example-opensource-cli-integrated` | `b7c6c1d8c162` | [verilog/integrated/lab1](../verilog/integrated/lab1/README.md) |
| `fpga-lab-example-vivado-2026-1-01-logic-gates` | `8d25deb5c064` | [verilog/lab1/01_logic_gates](../verilog/lab1/01_logic_gates/README.md) |
| `fpga-lab-example-vivado-2026-1-02-full-adder` | `8b506af67d1e` | [verilog/lab1/02_full_adder](../verilog/lab1/02_full_adder/README.md) |
| `fpga-lab-example-vivado-2026-1-03-adder4` | `08543696c146` | [verilog/lab1/03_adder4](../verilog/lab1/03_adder4/README.md) |
| `fpga-lab-example-vivado-2026-1-04-subtractor4` | `f7d79cd1f95d` | [verilog/lab1/04_subtractor4](../verilog/lab1/04_subtractor4/README.md) |
| `fpga-lab-example-vivado-2026-1-05-comparator4` | `913b0f41c48c` | [verilog/lab1/05_comparator4](../verilog/lab1/05_comparator4/README.md) |
| `fpga-lab-example-vivado-2026-1-06-mux4to1` | `009d192cb7f8` | [verilog/lab1/06_mux4to1](../verilog/lab1/06_mux4to1/README.md) |
| `fpga-lab-example-vivado-2026-1-07-demux1to8` | `3e8c1e3f1cef` | [verilog/lab1/07_demux1to8](../verilog/lab1/07_demux1to8/README.md) |
| `fpga-lab-example-vivado-2026-1-08-encoder8to3` | `485a6c588c7c` | [verilog/lab1/08_encoder8to3](../verilog/lab1/08_encoder8to3/README.md) |
| `fpga-lab-example-vivado-2026-1-09-decoder3to8` | `d5a11d33868d` | [verilog/lab1/09_decoder3to8](../verilog/lab1/09_decoder3to8/README.md) |
| `fpga-lab-example-vivado-2026-1-10-seven-segment` | `6cad34ce6d13` | [verilog/lab1/10_seven_segment](../verilog/lab1/10_seven_segment/README.md) |
| `fpga-lab-example-vivado-2026-1-integrated` | `5a553ee80227` | [verilog/integrated/lab1](../verilog/integrated/lab1/README.md) |
| `fpga-lab-template` | `0b3318e466e9` | [templates/fpga](../templates/fpga/README.md) |
| `fpga-lab2-example-cli-09-integrated` | `27626dafed23` | [verilog/integrated/lab2](../verilog/integrated/lab2/README.md) |
| `fpga-lab2-example-legacy-01-counter` | `6751a9498b6f` | [verilog/lab2/01_counter](../verilog/lab2/01_counter/README.md) |
| `fpga-lab2-example-legacy-02-clock-divider` | `108f965aba6f` | [verilog/lab2/02_clock_divider](../verilog/lab2/02_clock_divider/README.md) |
| `fpga-lab2-example-legacy-03-register` | `97a2dfb10b27` | [verilog/lab2/03_register](../verilog/lab2/03_register/README.md) |
| `fpga-lab2-example-legacy-04-shift-register` | `8cf6d59a7769` | [verilog/lab2/04_shift_register](../verilog/lab2/04_shift_register/README.md) |
| `fpga-lab2-example-legacy-05-piso` | `691889cb3aa7` | [verilog/lab2/05_piso](../verilog/lab2/05_piso/README.md) |
| `fpga-lab2-example-legacy-06-moore` | `2337ddbf75f1` | [verilog/lab2/06_moore](../verilog/lab2/06_moore/README.md) |
| `fpga-lab2-example-legacy-07-mealy` | `ed8390e6ddb2` | [verilog/lab2/07_mealy](../verilog/lab2/07_mealy/README.md) |
| `fpga-lab2-example-legacy-08-segment-scan` | `1d2200705e4b` | [verilog/lab2/08_segment_scan](../verilog/lab2/08_segment_scan/README.md) |
| `fpga-lab2-example-vivado-01-counter` | `3bdaf407937c` | [verilog/lab2/01_counter](../verilog/lab2/01_counter/README.md) |
| `fpga-lab2-example-vivado-02-clock-divider` | `ded58ac24859` | [verilog/lab2/02_clock_divider](../verilog/lab2/02_clock_divider/README.md) |
| `fpga-lab2-example-vivado-03-register` | `e87315981a53` | [verilog/lab2/03_register](../verilog/lab2/03_register/README.md) |
| `fpga-lab2-example-vivado-04-shift-register` | `bb812644b197` | [verilog/lab2/04_shift_register](../verilog/lab2/04_shift_register/README.md) |
| `fpga-lab2-example-vivado-05-piso` | `2093860d3dd8` | [verilog/lab2/05_piso](../verilog/lab2/05_piso/README.md) |
| `fpga-lab2-example-vivado-06-moore` | `87eaa8a9110b` | [verilog/lab2/06_moore](../verilog/lab2/06_moore/README.md) |
| `fpga-lab2-example-vivado-07-mealy` | `6b5ae99fbac7` | [verilog/lab2/07_mealy](../verilog/lab2/07_mealy/README.md) |
| `fpga-lab2-example-vivado-08-segment-scan` | `bf96576f614b` | [verilog/lab2/08_segment_scan](../verilog/lab2/08_segment_scan/README.md) |
| `fpga-lab2-example-vivado-09-integrated` | `21b9d222cbda` | [verilog/integrated/lab2](../verilog/integrated/lab2/README.md) |

## 보존·중복 처리

- 교안 ZIP 40개 중 소스가 있는 39개를 보존했다. 빈 `servo.zip` 대신 `servo_ctrl.zip`이 서보 소스를 제공한다.
- Full Demo는 VHDL 21개를 포함하는 별도 통합 예제다.
- LAB2의 Legacy/Vivado 8쌍은 설계·TB·핀 제약의 동일 파일을 한 위치로 합쳤다. Legacy에 함께 있던 교안 원본은 `verilog/textbook/`에서 찾는다.
- LAB1·LAB2 통합 예제의 Vivado/CLI 동일 소스도 합쳤고, CLI 전용 도구가 있으면 함께 보존했다.
- LAB1 Legacy 비교판 10개는 구형 구현 비교를 위해 남겼다.
- 보고서 실험 16~21은 공통 소스 한 벌과 `EXPERIMENT` 선택값으로 정리했다.
- 추가 Verilog 8개와 C 제공 예제 9종은 Markdown 인용 기호와 코드 울타리만 제거해 파일로 분리했다.
- 학생 과제 정답·FPGA SPI 구현은 새로 만들지 않았다.
- 원본 ZIP의 빌드 산출물 대신 HDL·핀 제약·프로젝트 입력 파일을 수록했다. 원본 저장소 이력과 ZIP은 별도로 백업했다.

## 확인 범위

원본 소스의 바이트·해시, 코드블록 분리 결과, 중복 대응, Git 서브모듈 제거와 Markdown 탐색 경로를 확인한다. 이번 통합 작업에서 시뮬레이션·C 빌드·언어 서버 검증은 수행하지 않는다. 기존 매뉴얼에 적힌 과거 실행 결과는 당시 기록이다.
