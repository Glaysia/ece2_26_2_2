# 강의자료

[저장소 안내](../README.md) · [문서 관리 및 남은 작업](../docs/README.md)

## 현재 파일

TeX가 강의 내용의 SSOT이며 PDF는 배포본이다. 아래 목록은 파일 존재 기준이며, 모든 실습의 장비 검증 완료를 뜻하지 않는다.

| 자료 | 원본 | 배포본 |
|---|---|---|
| 레거시 HDL 통합 교재 | [TeX](weekly-slides/LAB0_OT_0907/00.legacy_hdl.tex) | [PDF](weekly-slides/LAB0_OT_0907/00.legacy_hdl.pdf) |
| 오리엔테이션 | [TeX](weekly-slides/LAB0_OT_0907/02.LAB0_OT_0907.tex) | [PDF](weekly-slides/LAB0_OT_0907/02.LAB0_OT_0907.pdf) |
| Vivado 2026.1 설치 | [TeX](weekly-slides/LAB1_FPGA_0914/01.vivado_2026_1_설치_매뉴얼.tex) | [PDF](weekly-slides/LAB1_FPGA_0914/01.vivado_2026_1_설치_매뉴얼.pdf) |
| VS Code Verilog 환경설정 | [TeX](weekly-slides/LAB1_FPGA_0914/02.vscode_verilog_환경설정_매뉴얼.tex) | [PDF](weekly-slides/LAB1_FPGA_0914/02.vscode_verilog_환경설정_매뉴얼.pdf) |
| LAB1 목차·공통 안내 | [TeX](weekly-slides/LAB1_FPGA_0914/04.LAB1_00_CONTENTS.tex) | [PDF](weekly-slides/LAB1_FPGA_0914/04.LAB1_00_CONTENTS.pdf) |
| LAB1 01 논리 게이트 — 최신 | [TeX](weekly-slides/LAB1_FPGA_0914/04.LAB1_01_LOGIC_GATES_VIVADO.tex) | [PDF](weekly-slides/LAB1_FPGA_0914/04.LAB1_01_LOGIC_GATES_VIVADO.pdf) |
| LAB1 버튼·LCD 통합 — 최신 | [TeX](weekly-slides/LAB1_FPGA_0914/04.LAB1_10A_INTEGRATED_VIVADO.tex) | [PDF](weekly-slides/LAB1_FPGA_0914/04.LAB1_10A_INTEGRATED_VIVADO.pdf) |
| LAB1 버튼·LCD 통합 — CLI | [TeX](weekly-slides/LAB1_FPGA_0914/04.LAB1_10B_INTEGRATED_CLI.tex) | [PDF](weekly-slides/LAB1_FPGA_0914/04.LAB1_10B_INTEGRATED_CLI.pdf) |
| LAB1 01 논리 게이트 — 레거시 | [TeX](weekly-slides/LAB1_FPGA_0914/04.LAB1_11_LOGIC_GATES_LEGACY.tex) | [PDF](weekly-slides/LAB1_FPGA_0914/04.LAB1_11_LOGIC_GATES_LEGACY.pdf) |

- [LAB1 안내·22개 매뉴얼](weekly-slides/LAB1_FPGA_0914/README.md)
- [22개 FPGA 프로젝트·workspace](../example/fpga_projects_hdl/LAB1/README.md) · [학생용 템플릿](https://github.com/Glaysia/fpga-lab-template)
- [LAB1 PDF 묶음 ZIP](weekly-slides/LAB1_FPGA_0914/04.LAB1_0910_PDF.zip) — 전체 압축 해제 후 목차 PDF에서 시작
- [레거시 교재 편집·재빌드 상태](weekly-slides/LAB0_OT_0907/00.legacy_hdl.README.md)
- [공용 템플릿 4:3](templates/weekly_presentation_template_4x3.tex) — LAB1 조합회로 자료에 사용
- [기존 공용 템플릿 16:9](templates/weekly_presentation_template.tex)

자료에는 두 자리 번호를 사용하고 같은 자료의 TeX·PDF 이름을 맞춘다. 현재 OT와 VS Code 매뉴얼은 서로 다른 주차 폴더에서 `02`를 사용한다. 파일명은 그대로 두었으며, 기존의 “저장소 전체에서 고유한 연속 번호”라는 안내는 적용하지 않는다. 예정 파일을 완성된 자료처럼 목록에 넣지 않는다.

## 편집

- 설명·일정·정책·실습 요구사항은 해당 TeX에서 수정한다.
- 도식·표는 TeX/TikZ를 사용하고, 실제 화면·파형 캡처와 설명용 도식을 구분한다.
- 공용 시립대 로고, UOS Blue (`#005EB8`), D2Coding을 사용한다. LAB1 조합회로 자료는 4:3 Beamer 템플릿을 사용하며 기존 16:9 템플릿과 자료는 보존한다.
- 리소스 경로는 해당 TeX 기준 상대경로로 유지한다.
- 새 슬라이드 캡처 PNG는 로컬 빌드 자료로 무시하고 PDF를 커밋한다. 기존 추적 PNG는 유지하며 다른 장치에서 TeX를 재빌드할 필요는 없다.
- 기존 Markdown 원고는 [초안·기록 보관소](../docs/README.md)로 분리했다. 병행 원본으로 관리하지 않는다.

## 빌드

XeLaTeX가 설치된 환경에서 **빌드할 TeX가 있는 폴더**로 이동한 뒤 같은 명령을 두 번 실행한다. 예를 들어 이 README가 있는 폴더에서:

```powershell
cd weekly-slides/LAB1_FPGA_0914
xelatex -interaction=nonstopmode -halt-on-error '01.vivado_2026_1_설치_매뉴얼.tex'
xelatex -interaction=nonstopmode -halt-on-error '01.vivado_2026_1_설치_매뉴얼.tex'
```

직접 XeLaTeX를 실행하는 방법은 latexmk·Perl을 요구하지 않는다. 빌드 후 오류·잘린 목차·누락 이미지·페이지 구성을 확인하고 PDF를 갱신한다.

**예외:** 레거시 교재는 입력 코드 이미지가 삭제되어 현재 그대로 재빌드할 수 없다. 기존 PDF와 원본 TeX는 보존되어 있다.
