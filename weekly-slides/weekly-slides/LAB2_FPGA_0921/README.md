# LAB2 · 9월 21일 순차논리 실습

작성일: 2026-09-14. 최신 Vivado 개별 8개 + 버튼·LCD 통합 1개를 완성했다. CLI 교안은 이번 배포에서 제외한다.

[전체 PDF 다운로드 · ZIP](05.LAB2_0921_VIVADO_8plus1.zip) · [전체 목차](05.LAB2_00_CONTENTS.pdf) · [공통 예습](05.LAB2_00_START.pdf)

매뉴얼 9개와 공통 예습·목차 2개, 총 11개 PDF / 758쪽이다. ZIP 전체를 같은 폴더에 풀어 사용한다. 각 PDF 좌하단 목차는 해당 PDF의 2쪽으로 이동한다. PDF 간 링크는 같은 폴더의 상대 파일을 가리킨다. 뷰어가 외부 PDF 열기를 제한하면 전체 목차의 파일명으로 직접 연다.

## 매뉴얼

| 순서 | 자료 | 쪽 | 원고 |
|---|---|---:|---|
| 1 | [업/다운 카운터](05.LAB2_01_COUNTER_VIVADO.pdf) | 76 | [TeX](05.LAB2_01_COUNTER_VIVADO.tex) |
| 2 | [클록 분주](05.LAB2_02_CLOCK_DIVIDER_VIVADO.pdf) | 80 | [TeX](05.LAB2_02_CLOCK_DIVIDER_VIVADO.tex) |
| 3 | [레지스터: 데이터 저장과 이동](05.LAB2_03_REGISTER_VIVADO.pdf) | 79 | [TeX](05.LAB2_03_REGISTER_VIVADO.tex) |
| 4 | [시프트 레지스터](05.LAB2_04_SHIFT_REGISTER_VIVADO.pdf) | 75 | [TeX](05.LAB2_04_SHIFT_REGISTER_VIVADO.tex) |
| 5 | [PISO](05.LAB2_05_PISO_VIVADO.pdf) | 74 | [TeX](05.LAB2_05_PISO_VIVADO.tex) |
| 6 | [Moore 상태 머신](05.LAB2_06_MOORE_VIVADO.pdf) | 71 | [TeX](05.LAB2_06_MOORE_VIVADO.tex) |
| 7 | [Mealy 상태 머신](05.LAB2_07_MEALY_VIVADO.pdf) | 71 | [TeX](05.LAB2_07_MEALY_VIVADO.tex) |
| 8 | [7세그먼트 자리 스캔](05.LAB2_08_SEGMENT_SCAN_VIVADO.pdf) | 82 | [TeX](05.LAB2_08_SEGMENT_SCAN_VIVADO.tex) |
| 9 | [8모드 버튼·LCD 통합](05.LAB2_08A_INTEGRATED_VIVADO.pdf) | 120 | [TeX](05.LAB2_08A_INTEGRATED_VIVADO.tex) |

## 학생 진행 순서

[v2.0.1 빈 템플릿](https://github.com/Glaysia/fpga-lab-template/tree/v2.0.1)을 새 프로젝트명으로 clone한 뒤 PDF의 실제 VS Code 코드 화면을 보며 RTL·테스트벤치·XDC를 직접 작성한다. VS Code에서는 Icarus 시뮬레이션을 실행하고, 입력·예상 결과·파형·실행 로그를 실험 전 레포트에 정리한다.

이후 Vivado 2026.1 GUI에서 같은 원본을 연결하여 XSim → 핀 확인 → 합성 → 구현 → 비트스트림 생성을 수행한다. 실제 보드에 기록하고 사진·영상·관찰 결과를 실험 후 레포트 및 GitHub에 연결한다.

## 확인한 범위

9개 매뉴얼의 시뮬레이션과 Vivado GUI 비트스트림 생성 증거를 반영했다. 통합판은 Icarus·XSim에서 8모드, 2848개 검사, 34326 ns 종료를 확인했다. 실제 보드 동작·사진·영상은 학생 실험 절차이며 이번 제작에서 실측 완료로 표시하지 않았다.

전체 PDF는 4:3 비율이다. 변경 페이지를 렌더링하여 검수했으며, 변경하지 않은 페이지는 기존 검수본과 해시 또는 픽셀 비교로 확인했다. 코드 캡처·원본 해시, 각 페이지의 목차, PDF 간 링크 목적지, ZIP 재압축 해제 후 파일 해시를 검사했다.

- [PDF 검수 기록](final-visual-review.json)
- [ZIP 및 링크 검증 결과](pdf-package-validation.json)
- [통합 Vivado 실행 기록](../../../output/evidence/lab2-integrated-0914/vivado-gui-validation.json)
- [통합 VS Code 실행 기록](../../../output/evidence/lab2-integrated-0914/vscode-gui-result.json)
- [코드 캡처와 원본 연결](required-code-captures.json)
- [현재 계획 및 완료 기록](../../../daily_goal/GOAL0914_LAB2_RELEASE.md)
- [공개 예시 프로젝트](../../../example/fpga_projects_hdl/LAB2/README.md)

이전 계획·CLI 자료는 이력으로 보존하며 위 배포 ZIP에는 포함하지 않는다. 새 PNG는 기존 ignore 정책을 유지한다.
