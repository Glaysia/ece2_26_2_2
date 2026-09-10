# FEEDBACK_0223 반영 대조

작성일 2026-09-10. [피드백 원문](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/FEEDBACK_0223.md) · [제작 목표](../../../../daily_goal/GOAL0910.md) · [전체 프로젝트](../README.md) · [실행 검증](validation.md)

## 피드백별 구현과 증거

| 요구 | 현재 구현 | 확인 근거 |
|---|---|---|
| 최신 Vivado → 오픈소스 → 구버전 | 목차 PDF·ZIP·강의자료 목록·프로젝트 허브·템플릿 목록을 같은 순서로 구성 | [목록](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/README.md), [PDF 링크·ZIP 검사](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/pdf-package-validation.json), [문서 탐색 검사](navigation-validation.json) |
| 레거시 첫 자료에서 VS Code와 Vivado 목차 분리 | 모든 실습의 2쪽을 VS Code 사전·Vivado/CLI·사후 정리로 분리, 각 PDF 목차 버튼은 2쪽 | [레거시 첫 TeX](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/04.LAB1_11_LOGIC_GATES_LEGACY.tex), 위 PDF 링크 검사 |
| 고정된 공개 템플릿에서 git clone으로 시작 | 별도 fpga-lab-template과 루트 LAB1 workspace, 프로젝트별 22개 workspace | [공개 템플릿](https://github.com/Glaysia/fpga-lab-template), [익명 새 clone·실행 기록](template-clone-validation.json) |
| 시작할 때 버전 확인과 미설치 안내 | task 01에서 실제 도구 검사, 누락·잘못된 버전 출력은 실패 처리, 설치·PATH 안내 | [실행기](../tools/lab1.py), [첫 clone 도구 출력](template-clone-01_logic_gates-01.txt), [설치 안내](setup.md) |
| 최신 코드와 실제 레거시 코드 구분 | 최신 공통 RTL과 레거시 original 분리, 원본 41개 해시 보존, 감산기 수정본·보충 TB 별도 | [원본 대응](legacy-provenance.md), [구성 검사](../tools/verify_layout.py) |
| workspace에서 빌드 명령 제공 | 후속 사용자 요청에 따라 01 도구 검사·02 사전 시뮬레이션·03 파형만 제공. 기본 Build Task는 02이며 Vivado는 GUI 실습 | [첫 workspace](../vivado_2026_1/01_logic_gates/vivado_2026_1_01_logic_gates.code-workspace), 22개 구성 검사 |

새 clone 실행 증거의 소스 커밋은 `66a8b43`이다. 이후 템플릿 변경은 검증 문서·목록 순서·검사 도구이며 이 기록을 후속 커밋의 GUI 실행 결과라고 표시하지 않는다.

## 검증 범위

`verify_layout.py`는 22개 목록과 개별 설정의 ID·edition·part·top·TB top·소스·제약·검사 수가 같은지 확인한다. 작업 명령·실행 폴더·기본 Build Task, 21개 XPR의 실제 fileset 구성과 top·part·상대경로, 원본 41개 해시를 확인한다. XPR이 실제 Vivado 2020.1에서 열렸다는 검사는 아니다.

`verify_navigation.py`는 LAB1 Markdown의 실제 파일과 내부 앵커, 22개 프로젝트의 허브 복귀 링크, 최신·CLI·레거시 순서를 검사한다. 코드 블록 안의 학생용 예시는 실제 산출물 링크로 세지 않는다. 외부 URL의 HTTP 응답·영상 재생은 이 검사에 포함하지 않는다. PDF의 GoTo/GoToR과 압축 해제 후 연결은 별도 PDF 검사로 확인한다.

## 추가 반영 결과와 남은 작업

1. **추가 GUI 캡처 완료:** 실제 VS Code 코드 패널 52개를 확보하고 최종 소스의 줄 범위·해시를 기록했다. 최신 개별 10개와 통합 1개 모두 Vivado GUI 파형·PASS를 확인했다. 최신 02–10의 파형·PASS 로그·기존 구현 상태 패널 27개를 추가했고 통합 LCD ASCII 문자열도 확보했다. GUI 정상 종료 후 02–10과 통합본의 전체 VCD가 사전 결과와 일치했다. [통합 GUI 증거](../vivado_2026_1/11_integrated/evidence/gui-simulation.json)는 2,560개 PASS와 72,430ns 종료를 포함한다. 02–10과 통합 bit는 기존 배치 빌드 결과이며 GUI에서는 완료 상태를 확인했다.
2. **캡처 반영·가독성:** 새 코드 화면마다 파일명·줄 범위·입력 생성·기대값·실패 처리 해설을 붙였다. 21개 TeX/PDF에 반영했고 원본 PNG는 새로 추적하지 않는다. 수정 PDF 1,154쪽을 렌더링해 기존 본문 1,009쪽의 동일성과 변경 화면 82종의 가독성을 확인했다. [화면 검수 기록](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/code-page-validation.json). 추가 GUI 페이지는 [GUI 화면 검수](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/gui-page-validation.json)에 기록한다. PDF/ZIP의 최종 페이지 수와 검사 결과는 [강의자료 목록](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/README.md)과 [배포 검사](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/pdf-package-validation.json)를 따른다.
3. **구버전 실행:** 실제 Vivado 2020.1 환경에서 레거시 XPR 열기·시뮬레이션·구현을 확인한다. 현재 PASS는 XSim 2026.1의 원본 RTL 검사다.
4. **CLI bit:** 검증한 S75 DB에서 통합 필요 핀 38개 중 28개가 누락되어 nextpnr가 실패했다. 정확한 S75 핀·타일 DB를 확보한 뒤 [CLI 재개 절차](cli.md)를 따른다. 합성 성공을 bit 생성 완료로 바꾸지 않는다.
5. **실물 실험:** 연결된 xc7s75 장치와 보드 전원·JTAG를 확인하고 각 bit를 기록한다. 입력·출력·10모드·버튼·LCD를 실측하고 직접 사진·영상을 촬영해 [사후 레포트](reports.md)에 연결한다. 이 자료는 현재 없다.

3–5번 실물·도구 검증 항목 때문에 전체 실험 GOAL은 미완료다. 보드·촬영 결과는 시뮬레이션이나 생성 이미지로 대신하지 않는다.
