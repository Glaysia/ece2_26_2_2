# 제작 검증 현황

[전체 프로젝트](../README.md) · [기계 판독 결과](validation-results.json) · [Icarus 교차검사](cli-simulation-results.json) · [VS Code·Vivado VCD 대조](simulation-comparison.json) · [CLI 빌드](cli.md) · [첫 회로 GUI](../vivado_2026_1/01_logic_gates/VALIDATION.md)

작성일 2026-09-10. PASS는 표의 해당 단계에 한정합니다. NOT_RUN은 미실행, RUNNING은 진행 중, FAIL은 실패입니다. 각 프로젝트의 evidence에 실제 로그·결과·소스 SHA-256을 보관합니다.

| 프로젝트 | 사전 시뮬레이션 | Vivado 시뮬레이션 | Vivado bit | 보드 기록·촬영 |
|---|---|---|---|---|
| [vivado_2026_1_01_logic_gates](../vivado_2026_1/01_logic_gates/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_02_full_adder](../vivado_2026_1/02_full_adder/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_03_adder4](../vivado_2026_1/03_adder4/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_04_subtractor4](../vivado_2026_1/04_subtractor4/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_05_comparator4](../vivado_2026_1/05_comparator4/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_06_mux4to1](../vivado_2026_1/06_mux4to1/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_07_demux1to8](../vivado_2026_1/07_demux1to8/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_08_encoder8to3](../vivado_2026_1/08_encoder8to3/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_09_decoder3to8](../vivado_2026_1/09_decoder3to8/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_10_seven_segment](../vivado_2026_1/10_seven_segment/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [vivado_2026_1_integrated](../vivado_2026_1/11_integrated/evidence/validation.json) | PASS | PASS | PASS | 미수행 |
| [opensource_cli_integrated](../opensource_cli/integrated/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_01_logic_gates](../legacy/01_logic_gates/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_02_full_adder](../legacy/02_full_adder/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_03_adder4](../legacy/03_adder4/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_04_subtractor4](../legacy/04_subtractor4/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_05_comparator4](../legacy/05_comparator4/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_06_mux4to1](../legacy/06_mux4to1/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_07_demux1to8](../legacy/07_demux1to8/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_08_encoder8to3](../legacy/08_encoder8to3/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_09_decoder3to8](../legacy/09_decoder3to8/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |
| [legacy_10_seven_segment](../legacy/10_seven_segment/evidence/validation.json) | PASS | NOT_RUN | NOT_RUN | 미수행 |

첫 최신 회로는 공개 템플릿 740aef5를 새로 clone하여 실제 Vivado GUI로 시뮬레이션·bit 생성을 수행했습니다. 나머지 최신 회로는 같은 입력 파일의 Vivado 2026.1 배치 실행으로 검증합니다. 두 XSim 경로의 VCD에서 날짜·버전 메타데이터만 제외하고 신호 선언·모든 시간과 값 변화를 대조한 결과도 별도로 보관합니다. 학생용 매뉴얼은 GUI 클릭 순서입니다. 이 두 수행 방식을 혼동하지 않습니다.

레거시 원본 XPR은 2020.1 형식을 유지했습니다. 표의 레거시 사전 PASS는 2026.1 XSim 검사이며, Vivado 2020.1 GUI·합성·보드 실행은 미수행입니다. CLI 통합은 Icarus와 별도 openXC7 결과를 확인합니다.

## 남아 있는 실제 장비·캡처 확인

첫 회로 공통 GUI와 full_adder/half_adder, adder_4bit, sub_4bit, compare_4 소스 캡처는 실제 화면입니다. 추가 캡처 중 Windows 잠금 화면이 나타나 GUI 작업을 중단했습니다. 나머지 회로 전용 코드·파형·Vivado 결과 캡처는 미확보이며, 공통 예시 화면과 해당 회로의 실행 결과를 구분합니다.

공개 템플릿 66a8b43을 인증 없이 공백 포함 새 경로에 clone했습니다. 22개 workspace·21개 XPR·원본 41개 파일과 로컬 링크 검사가 통과했습니다. 실제 workspace 명령으로 첫 회로 도구 검사·시뮬레이션과 통합 회로 시뮬레이션도 통과했습니다. [새 clone 검증](template-clone-validation.json)에 명령별 로그를 연결했습니다.

최신 11개 bit 생성은 모두 PASS입니다. 통합 구현의 내부 1kHz 타이밍은 WNS 999994.562ns, WHS 0.193ns, 실패 endpoint 0개입니다. 외부 I/O 지연 미지정(TIMING-18)과 구성 전압 미지정(CFGBVS-1) 경고는 남아 있습니다. [타이밍·DRC 해석](integrated.md#구현-타이밍과-drc)에서 범위를 확인합니다.

실제 FPGA 기록, LCD 실물 동작, 보드 사진·영상은 미수행입니다. 레포트 양식과 촬영 절차는 제공하지만 결과를 꾸며 채우지 않습니다. 이 항목이 남아 있으므로 GOAL의 전체 완료로 표시하지 않습니다.
