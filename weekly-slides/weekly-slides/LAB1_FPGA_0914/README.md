# LAB1 — FPGA

[전체 강의자료](../../README.md) · [문서 관리](../../../docs/README.md)

## 현재 자료

첫 회로 최신 검토본: [PDF](04.LAB1_01_LOGIC_GATES_VIVADO.pdf) · [소스·workspace·검증](../../../example/fpga_projects_hdl/LAB1/vivado_2026_1/01_logic_gates/README.md). 템플릿 clone부터 두 시뮬레이션과 비트스트림 생성까지 포함한다.

| 자료 | 원본 | 배포본 |
|---|---|---|
| Vivado 설치 | [TeX](01.vivado_2026_1_설치_매뉴얼.tex) | [PDF](01.vivado_2026_1_설치_매뉴얼.pdf) |
| VS Code Verilog 환경설정 | [TeX](02.vscode_verilog_환경설정_매뉴얼.tex) | [PDF](02.vscode_verilog_환경설정_매뉴얼.pdf) |
| 01 논리 게이트 — VS Code → Vivado 2026.1, 59쪽 | [TeX](04.LAB1_01_LOGIC_GATES_VIVADO.tex) | [PDF](04.LAB1_01_LOGIC_GATES_VIVADO.pdf) |
| LAB1 목차·공통 안내 — 4:3, 5쪽 | [TeX](04.LAB1_00_CONTENTS.tex) | [PDF](04.LAB1_00_CONTENTS.pdf) |
| 01 논리 게이트 — VS Code 사전 실습 + 레거시 Vivado, 101쪽 | [TeX](04.LAB1_11_LOGIC_GATES_LEGACY.tex) | [PDF](04.LAB1_11_LOGIC_GATES_LEGACY.pdf) |

학생 배포용: [PDF 묶음 ZIP](04.LAB1_0910_PDF.zip). ZIP 전체를 풀고 `04.LAB1_00_CONTENTS.pdf`부터 연다. 각 PDF 좌하단의 ‘목차’는 같은 파일의 목차로 이동한다. 레거시 01에서는 2쪽의 실습 목차로 돌아간다. ‘전체 목차 PDF’는 별도 파일로 이동하는 링크다. 폴더 구조와 파일명을 유지한다. PDF 뷰어에 따라 외부 파일 링크 지원이 다르므로 링크가 동작하지 않으면 같은 폴더의 대상 PDF를 직접 연다.

기존 묶음에는 목차·레거시 01·기존 Vivado 설치·VS Code 환경설정 PDF가 포함된다. 01번은 [VS Code 사전 실습 32쪽](sections/vscode_01_logic_gates.tex)부터 시작한다. 새 창·workspace·확장 활성화·작업 선택·실행 로그·VaporView 파형·실험 전 레포트를 안내하며 [실행용 프로젝트와 workspace](../../../example/fpga_projects_hdl/LAB1/legacy/01_logic_gates/README.md)를 제공한다. 뒤의 [레거시 원문 69쪽](sections/legacy_01_logic_gates.tex)은 원본의 프로젝트 생성부터 보드 동작 확인까지 보존한다. [원문 대응표](assets/legacy-01/README.md)와 [새 캡처의 검증 범위](assets/vscode-01/README.md)를 구분한다. 나머지 21개 프로젝트의 상세 안내는 이후 추가한다.

TeX는 `04.LAB1_번호_내용.tex` 형식으로 분리한다. [공통 서식](shared/lab1_preamble.tex)과 [목차 본문](sections/lab1_overview.tex)을 재사용한다. 중복된 COMB 통합 검토본은 사용하지 않는다. 새 캡처 PNG는 로컬 빌드 자료로 Git에서 무시하며, 다른 장치의 TeX 재빌드는 요구하지 않는다. PDF와 ZIP을 배포·커밋한다.

PDF 빌드 후 [묶음 생성 스크립트](../../tools/package_lab1_pdfs.py)를 실행하면 PDF의 파일 간 링크·목적지와 ZIP 압축 해제 후의 연결을 검사한다. 실행에는 Python과 `pypdf`가 필요하다.

수업 내용과 도구 사용 절차는 위 TeX에서 수정한다. 이 README에는 강의 본문·실습 명세를 중복 작성하지 않는다. 빌드 방법은 [공통 안내](../../README.md)를 따른다.

## 제작 대기

- LAB1 조합회로 본문: [현재 제작 목표](../../../daily_goal/GOAL0910.md)에 따라 나머지 레거시 실습, 최신 Vivado, 통합 프로젝트, 상세 VS Code 사전 시뮬레이션·실험 전·후 레포트와 CLI 절차를 이어 작성.
- 별도 조합회로 시뮬레이션 자료와 보고서 예시: 현재 배포할 파일을 확정한 뒤 목록에 추가.
- 예제 경로와 실행 절차: 기존 HDL 프로젝트 삭제 이후 현재 저장소 기준으로 재검증.

기존 README의 상세 실습 구상은 초안으로 보존했다. 기존 VS Code Markdown 원고는 [이전 원고](../../../docs/archive/LAB1_VSCode_환경설정_이전원고.md)로 보관하며, 현재 매뉴얼은 TeX만 수정한다.

첫 회로 검토용 별도 묶음: [PDF 3개 ZIP](04.LAB1_01_REVIEW.zip). 최신 01 실습과 설치·환경설정 보조 PDF를 포함하며 기존 레거시 묶음과 구분한다.

학생용 실행 템플릿: [Glaysia/fpga-lab-template](https://github.com/Glaysia/fpga-lab-template). clone 후 루트의 LAB1.code-workspace를 열며, 최신 01 PDF도 이 주소를 기준으로 안내합니다.
