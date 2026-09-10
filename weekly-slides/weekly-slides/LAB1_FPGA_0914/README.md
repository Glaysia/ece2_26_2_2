# LAB1 — FPGA 실습 22개

작성일 2026-09-10 · 4:3 슬라이드 · 09-14 수업 전 예습

[전체 목차 PDF](04.LAB1_00_CONTENTS.pdf) · [PDF 25개 ZIP](04.LAB1_0910_PDF.zip) · [학생용 템플릿](https://github.com/Glaysia/fpga-lab-template) · [22개 프로젝트](../../../example/fpga_projects_hdl/LAB1/README.md) · [검증 현황](../../../example/fpga_projects_hdl/LAB1/docs/validation.md) · [제작 목표](../../../daily_goal/GOAL0910.md)

VS Code 새 창 → workspace → 예상값·소스·TB → task 01·02·03 → 실험 전 레포트 → Vivado GUI 또는 CLI → 보드 기록·촬영 → GitHub·실험 후 레포트 순서입니다. 최신 첫 회로는 실제 GUI를 세분화한 59쪽 안내이며, 이후 회로는 공통 화면과 회로별 파일·핀·검사값을 구분하고 실제 GUI 파형·PASS 로그를 설명합니다.

ZIP 전체를 풀고 목차 PDF부터 엽니다. 각 실습 좌하단 목차는 같은 PDF 2쪽입니다. 외부 PDF 링크를 지원하지 않는 뷰어에서는 같은 폴더의 파일을 직접 여세요.

| 실습 | 쪽 | 강의자료 | 실행 프로젝트 |
|---|---:|---|---|
| 01_LOGIC_GATES_VIVADO | 59 | [PDF](04.LAB1_01_LOGIC_GATES_VIVADO.pdf) · [TeX](04.LAB1_01_LOGIC_GATES_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/01_logic_gates/README.md) |
| 02_FULL_ADDER_VIVADO | 42 | [PDF](04.LAB1_02_FULL_ADDER_VIVADO.pdf) · [TeX](04.LAB1_02_FULL_ADDER_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/02_full_adder/README.md) |
| 03_ADDER4_VIVADO | 43 | [PDF](04.LAB1_03_ADDER4_VIVADO.pdf) · [TeX](04.LAB1_03_ADDER4_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/03_adder4/README.md) |
| 04_SUBTRACTOR4_VIVADO | 43 | [PDF](04.LAB1_04_SUBTRACTOR4_VIVADO.pdf) · [TeX](04.LAB1_04_SUBTRACTOR4_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/04_subtractor4/README.md) |
| 05_COMPARATOR4_VIVADO | 42 | [PDF](04.LAB1_05_COMPARATOR4_VIVADO.pdf) · [TeX](04.LAB1_05_COMPARATOR4_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/05_comparator4/README.md) |
| 06_MUX4TO1_VIVADO | 42 | [PDF](04.LAB1_06_MUX4TO1_VIVADO.pdf) · [TeX](04.LAB1_06_MUX4TO1_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/06_mux4to1/README.md) |
| 07_DEMUX1TO8_VIVADO | 42 | [PDF](04.LAB1_07_DEMUX1TO8_VIVADO.pdf) · [TeX](04.LAB1_07_DEMUX1TO8_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/07_demux1to8/README.md) |
| 08_ENCODER8TO3_VIVADO | 42 | [PDF](04.LAB1_08_ENCODER8TO3_VIVADO.pdf) · [TeX](04.LAB1_08_ENCODER8TO3_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/08_encoder8to3/README.md) |
| 09_DECODER3TO8_VIVADO | 42 | [PDF](04.LAB1_09_DECODER3TO8_VIVADO.pdf) · [TeX](04.LAB1_09_DECODER3TO8_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/09_decoder3to8/README.md) |
| 10_SEVEN_SEGMENT_VIVADO | 45 | [PDF](04.LAB1_10_SEVEN_SEGMENT_VIVADO.pdf) · [TeX](04.LAB1_10_SEVEN_SEGMENT_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/10_seven_segment/README.md) |
| 10A_INTEGRATED_VIVADO | 69 | [PDF](04.LAB1_10A_INTEGRATED_VIVADO.pdf) · [TeX](04.LAB1_10A_INTEGRATED_VIVADO.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/11_integrated/README.md) |
| 10B_INTEGRATED_CLI | 56 | [PDF](04.LAB1_10B_INTEGRATED_CLI.pdf) · [TeX](04.LAB1_10B_INTEGRATED_CLI.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/opensource_cli/integrated/README.md) |
| 11_LOGIC_GATES_LEGACY | 95 | [PDF](04.LAB1_11_LOGIC_GATES_LEGACY.pdf) · [TeX](04.LAB1_11_LOGIC_GATES_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/01_logic_gates/README.md) |
| 12_FULL_ADDER_LEGACY | 65 | [PDF](04.LAB1_12_FULL_ADDER_LEGACY.pdf) · [TeX](04.LAB1_12_FULL_ADDER_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/02_full_adder/README.md) |
| 13_ADDER4_LEGACY | 62 | [PDF](04.LAB1_13_ADDER4_LEGACY.pdf) · [TeX](04.LAB1_13_ADDER4_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/03_adder4/README.md) |
| 14_SUBTRACTOR4_LEGACY | 63 | [PDF](04.LAB1_14_SUBTRACTOR4_LEGACY.pdf) · [TeX](04.LAB1_14_SUBTRACTOR4_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/04_subtractor4/README.md) |
| 15_COMPARATOR4_LEGACY | 63 | [PDF](04.LAB1_15_COMPARATOR4_LEGACY.pdf) · [TeX](04.LAB1_15_COMPARATOR4_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/05_comparator4/README.md) |
| 16_MUX4TO1_LEGACY | 63 | [PDF](04.LAB1_16_MUX4TO1_LEGACY.pdf) · [TeX](04.LAB1_16_MUX4TO1_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/06_mux4to1/README.md) |
| 17_DEMUX1TO8_LEGACY | 63 | [PDF](04.LAB1_17_DEMUX1TO8_LEGACY.pdf) · [TeX](04.LAB1_17_DEMUX1TO8_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/07_demux1to8/README.md) |
| 18_ENCODER8TO3_LEGACY | 63 | [PDF](04.LAB1_18_ENCODER8TO3_LEGACY.pdf) · [TeX](04.LAB1_18_ENCODER8TO3_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/08_encoder8to3/README.md) |
| 19_DECODER3TO8_LEGACY | 63 | [PDF](04.LAB1_19_DECODER3TO8_LEGACY.pdf) · [TeX](04.LAB1_19_DECODER3TO8_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/09_decoder3to8/README.md) |
| 20_SEVEN_SEGMENT_LEGACY | 67 | [PDF](04.LAB1_20_SEVEN_SEGMENT_LEGACY.pdf) · [TeX](04.LAB1_20_SEVEN_SEGMENT_LEGACY.tex) | [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/legacy/10_seven_segment/README.md) |

보조 자료: [Vivado 설치](01.vivado_2026_1_설치_매뉴얼.pdf) · [VS Code 환경설정](02.vscode_verilog_환경설정_매뉴얼.pdf). ZIP은 실습 22개·전체 목차 1개·보조 2개를 포함합니다.

## 검증 범위

실제 로그·VCD·비트스트림과 SHA-256은 프로젝트 evidence와 release에서 확인합니다. 레거시 원본 2020.1 XPR과 보충 자기검사 TB를 구분합니다. 원본 감산기의 동일 입력 borrow 오류는 원본을 보존하고 corrected 소스로 수정했습니다.

CLI는 macOS ARM64 배포를 확인하고 WSL에서 실행했습니다. 통합 시뮬레이션·Yosys 합성은 통과했으나 사용한 S75 데이터베이스의 핀 누락으로 배치배선에 실패하여 CLI bit는 미생성입니다. [실패 로그와 분석](../../../example/fpga_projects_hdl/LAB1/docs/cli.md)을 확인하세요.

실제 VS Code 코드 패널 52개와 입력·기대값·실패 처리 해설을 추가했고 공통 메뉴·폴더 화면을 확대했습니다. 최신 11개 프로젝트의 실제 Vivado GUI 파형·PASS를 확인했습니다. 최신 02–10의 파형·로그·기존 구현 완료 화면 27개와 통합 LCD ASCII 파형을 추가했고, GUI 종료 후 전체 VCD가 사전 결과와 일치합니다. [코드 출처](assets/lab1-circuits/provenance.json) · [개별 GUI 출처](assets/latest-gui/provenance.json) · [통합 GUI 출처](assets/integrated-gui/provenance.json) · [코드 화면 검수](code-page-validation.json) · [GUI 화면 검수](gui-page-validation.json). 02–10과 통합 bit는 기존 배치 생성 결과이며 GUI에서는 완료 상태를 확인했습니다. Vivado 2020.1 실행, CLI bit 생성, 실제 보드 기록·사진·영상은 미완료입니다. VCD 도표와 실제 GUI 캡처를 구분해 표시합니다.

## 제작 파일

[실험 전·후 레포트 양식과 예시](../../../example/fpga_projects_hdl/LAB1/docs/reports.md) · [공통 TeX 서식](shared/lab1_preamble.tex) · [분할 문서 생성기](../../tools/lab1_series.py) · [PDF 링크·ZIP 검증기](../../tools/package_lab1_pdfs.py)

새 PNG는 로컬 빌드 자료로 무시하고 TeX·PDF·ZIP을 커밋합니다. 다른 장치에서 TeX를 다시 빌드하는 것은 배포 요건이 아닙니다. 프로젝트 소스·workspace는 clone 후 실행할 수 있도록 상대경로를 검증합니다.
