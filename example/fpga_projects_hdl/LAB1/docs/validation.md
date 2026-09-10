# 제작 검증 현황

> 아래 GUI·bit 결과는 이전 강의 프로젝트의 제작 이력이다. 새 단일 프로젝트 구성의 22개 원격 clone·입력 해시·Icarus 재검증은 [서브모듈 검증 기록](submodule-validation.json)을 따른다.

[전체 프로젝트](../README.md) · [기계 판독 결과](validation-results.json) · [Icarus 교차검사](cli-simulation-results.json) · [VS Code·Vivado VCD 대조](simulation-comparison.json) · [CLI 빌드](cli.md) · [첫 회로 GUI](https://github.com/Glaysia/ece2_26_2_2/blob/3a521984ac1e0b6a2f69865aad1acf72b05959da/example/fpga_projects_hdl/LAB1/vivado_2026_1/01_logic_gates/VALIDATION.md)

## 현재 단일 프로젝트와 CLI 검증

현재 학생 템플릿은 **v2.0.0**의 프로젝트 하나입니다. 22개 완성 예시는 독립 저장소·서브모듈이며 [원격 clone 검사](submodule-validation.json)를 통과했습니다. CLI 갱신분은 [새 원격 clone·입력 해시·시뮬레이션·보조 도구 다운로드 검사](cli-pr15-evidence/fresh-clone-validation.json)로 추가 확인했습니다.

정확한 xc7s75fgga484-1에서 오픈소스 합성·배치배선·프레임·bit 생성이 모두 통과했습니다. [첫 실행](cli-pr15-evidence/validation.json), [학생 명령 재현](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/v2.0.1/evidence/openxc7/student-command-validation.json), [9,104프레임 체크섬 검사](cli-pr15-evidence/bitread.txt)를 제공합니다. 이 결과는 Vivado bit를 가져온 것이 아닙니다.

openFPGALoader v0.13.1의 지원 목록과 장치 탐색을 실행했습니다. [탐색 기록](cli-pr15-evidence/loader-validation.json)은 JTAG 장치 없음이며 실제 기록·촬영 성공으로 표시하지 않습니다. 학생용 매뉴얼은 SRAM 기록·LCD·10모드 촬영·레포트·GitHub 제출까지 안내합니다.

## 이전 Vivado 제작 이력

작성일 2026-09-10. PASS는 표의 해당 단계에 한정합니다. NOT_RUN은 미실행, RUNNING은 진행 중, FAIL은 실패입니다. 각 프로젝트의 evidence에 실제 로그·결과·소스 SHA-256을 보관합니다.

| 프로젝트 | 사전 시뮬레이션 | Vivado 시뮬레이션 | Vivado bit | 보드 기록·촬영 |
|---|---|---|---|---|
| [vivado_2026_1_01_logic_gates](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-01-logic-gates/blob/8d25deb5c064edd95d61488a32d643c4bb331fb8/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_02_full_adder](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-02-full-adder/blob/8b506af67d1e0cb7bc63854c8bb2a2633d3326be/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_03_adder4](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-03-adder4/blob/08543696c146164de20930270b01bfbd12ccdd72/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_04_subtractor4](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-04-subtractor4/blob/f7d79cd1f95d423edaa3746b75002b0ecf8c5eea/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_05_comparator4](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-05-comparator4/blob/913b0f41c48c2351cdaba21380d0d83770c43445/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_06_mux4to1](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-06-mux4to1/blob/009d192cb7f873a2b31d0386ea68cc451fdec89b/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_07_demux1to8](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-07-demux1to8/blob/3e8c1e3f1cef7f602d586e152754182f43ac3679/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_08_encoder8to3](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-08-encoder8to3/blob/485a6c588c7c9230222c4763deb372f36e5b3384/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_09_decoder3to8](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-09-decoder3to8/blob/d5a11d33868dfb9ff71b7e598644099a9ce59b65/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_10_seven_segment](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-10-seven-segment/blob/6cad34ce6d1385cd261b510024d50936dccb8f45/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_integrated](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-integrated/blob/5a553ee802270caf3f909395f5e29bdcbbd48352/evidence/historical-course/validation.json) | PASS | PASS | PASS | 미수행 |
| [opensource_cli_integrated](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/2c1e00f7ca38de27f1b933e836de210fb7682ca0/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_01_logic_gates](https://github.com/Glaysia/fpga-lab-example-legacy-01-logic-gates/blob/9055c8002ec5149907f393a1c781000d44125e38/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_02_full_adder](https://github.com/Glaysia/fpga-lab-example-legacy-02-full-adder/blob/0fe260d299847628fd01626c76ae87150f601ca1/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_03_adder4](https://github.com/Glaysia/fpga-lab-example-legacy-03-adder4/blob/14578fedf93bb22b3366f2070d80cfe4a46ff62e/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_04_subtractor4](https://github.com/Glaysia/fpga-lab-example-legacy-04-subtractor4/blob/6383aa022813906c7f438351eabe580c132879d5/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_05_comparator4](https://github.com/Glaysia/fpga-lab-example-legacy-05-comparator4/blob/d8e0f25d8058df9c07084f03cf997ae649fd84af/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_06_mux4to1](https://github.com/Glaysia/fpga-lab-example-legacy-06-mux4to1/blob/80d65af6339ade695aad964c39f66efb37ac7367/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_07_demux1to8](https://github.com/Glaysia/fpga-lab-example-legacy-07-demux1to8/blob/2e2ab8cf96476f44e9357cc4aa48570b7e18b613/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_08_encoder8to3](https://github.com/Glaysia/fpga-lab-example-legacy-08-encoder8to3/blob/7f88377d78cf60cece52021e238a9ecc62d70a0b/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_09_decoder3to8](https://github.com/Glaysia/fpga-lab-example-legacy-09-decoder3to8/blob/e4d6725666068c25fb4a261ba10512cd2e350ad7/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_10_seven_segment](https://github.com/Glaysia/fpga-lab-example-legacy-10-seven-segment/blob/ccd38e3159da27d975bcb65cb2a34911d881a701/evidence/historical-course/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |

첫 최신 회로는 공개 템플릿 740aef5를 새로 clone하여 실제 Vivado GUI로 시뮬레이션·bit 생성을 수행했습니다. 최신 02–10과 통합본도 배포 XPR을 GUI에서 열고 Behavioral Simulation을 직접 실행했습니다. 최신 11개 모두 실제 GUI 파형·PASS 기록을 확보했습니다. 02–10과 통합본은 정상 종료한 GUI VCD의 신호 선언·모든 시각·값 변화가 사전 결과와 완전히 일치합니다. 날짜·버전 메타데이터와 공백만 정규화합니다. 각 README의 GUI 기록을 확인하세요. [통합 GUI 기록](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-integrated/blob/5a553ee802270caf3f909395f5e29bdcbbd48352/evidence/historical-course/gui-simulation.json)은 2,560개 PASS·72,430ns 종료를 포함합니다. 02–10과 통합본의 bit는 앞서 수행한 배치 빌드 결과이며 이번 GUI에서는 기존 완료 상태를 확인했습니다. 학생용 매뉴얼은 GUI 클릭 순서입니다.

레거시 원본 XPR은 2020.1 형식을 유지했습니다. 표의 레거시 사전 PASS는 2026.1 XSim 검사이며, Vivado 2020.1 GUI·합성·보드 실행은 미수행입니다. CLI 통합은 Icarus와 별도 openXC7 결과를 확인합니다.

## 이전 제작 기록과 실물 검증 범위

최신 RTL·개별 자기검사 TB·통합 top·버튼·LCD·통합 TB의 실제 VS Code 화면을 확보했습니다. 코드 패널 52개의 [소스 줄 범위·해시](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/assets/lab1-circuits/provenance.json)를 기록했습니다. 최신 02–10의 실제 파형·PASS 로그·기존 구현 상태 패널 27개와 통합 LCD ASCII 파형·전체 종료 로그를 추가했습니다. [개별 GUI 출처](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/assets/latest-gui/provenance.json) · [통합 GUI 출처](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/assets/integrated-gui/provenance.json).

이전 다중 프로젝트 템플릿 66a8b43을 인증 없이 공백 포함 새 경로에 clone했습니다. 22개 workspace·21개 XPR·원본 41개 파일과 로컬 링크 검사가 통과했습니다. 실제 workspace 명령으로 첫 회로 도구 검사·시뮬레이션과 통합 회로 시뮬레이션도 통과했습니다. [새 clone 검증](template-clone-validation.json)에 명령별 로그를 연결했습니다.

최신 11개 bit 생성은 모두 PASS입니다. 통합 구현의 내부 1kHz 타이밍은 WNS 999994.562ns, WHS 0.193ns, 실패 endpoint 0개입니다. 외부 I/O 지연 미지정(TIMING-18)과 구성 전압 미지정(CFGBVS-1) 경고는 남아 있습니다. [타이밍·DRC 해석](integrated.md#구현-타이밍과-drc)에서 범위를 확인합니다.

실제 FPGA 기록, LCD 실물 동작, 보드 사진·영상은 미수행입니다. 레포트 양식과 촬영 절차는 제공하지만 결과를 꾸며 채우지 않습니다. 이 항목은 학생이 실제 실험에서 수행하고 제출할 실물 검증이며 교안·소프트웨어 빌드의 검증과 구분합니다.
