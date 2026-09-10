# 레거시 원본과 수정 범위

[전체 프로젝트](../README.md) · [감산기](../legacy/04_subtractor4/README.md)

10개 프로젝트의 `original/` RTL·testbench·XPR은 저장소의 장비 제공 ZIP에서 추출했습니다. 각 프로젝트의 `provenance.json`에 원본 ZIP·파일 해시를 기록합니다. 원본 XPR은 Vivado 2020.1 형식입니다.

학생용 `vivado/<top>.xpr`은 원본의 버전·실행 전략을 유지하고 소스 경로를 `$PPRDIR` 기준 상대경로로 바꿨습니다. Design Sources, Simulation Sources, Constraints를 배포 파일로 연결하고 자기검사 TB를 simulation top으로 지정했습니다. 구버전 Vivado 2020.1 실행은 제작 환경에서 수행하지 않았습니다. 2026.1 XSim에서 RTL 검사를 통과한 것과 구버전 도구에서 프로젝트를 실행한 것을 구분합니다.

`create_project.tcl`은 경로·설정을 확인하고 프로젝트를 재생성하기 위한 보조 원본입니다. 학생 강의의 Vivado 과정은 GUI 메뉴를 직접 누르며 task 04–06을 사용하지 않습니다.

## 감산기 borrow 오류

원본 `sub_4bit.v`는 `a>b`일 때 borrow=0, 나머지는 1로 설정합니다. 그래서 a=b에서 잘못된 borrow=1이 발생합니다. 보충 파일 `corrected/sub_4bit.v`는 `a>=b`일 때 borrow=0으로 고쳤습니다. 차이의 하위 4비트는 같은 규칙입니다.

원본은 그대로 보존하고 workspace·배포 XPR은 수정본을 참조합니다. 256개 전체 입력의 자기검사는 a=b에서도 borrow=0을 기대합니다. [원본 오류 검출](../legacy/04_subtractor4/evidence/original-borrow-negative.txt)과 수정본 [실행 결과](../legacy/04_subtractor4/evidence/validation.json)를 비교합니다. 원본 교안 이미지는 고치지 않고 앞부분에 보충 설명을 넣었습니다.

## 원본 교안 이미지

레거시 PDF의 원문 페이지는 2022년 보관 PDF에서 추출했습니다. 첫 회로는 기존에 검토한 4:3 재구성을 보존하고 나머지는 원본 16:9 페이지를 4:3 안에 비율을 유지해 배치합니다. 원문 내용·사진·코드·순서는 유지합니다. 새로운 VS Code 사전 실습은 원문 앞에 추가했습니다. 각 `assets/legacy-XX/provenance.json`은 원본 PDF 해시와 페이지 번호를 연결합니다.

## MUX 핀표의 원문 불일치

원본 MUX 교안의 핀 대응 표는 i[0]을 Y4로 표기하지만 이어지는 Vivado I/O 화면과 배포 ZIP의 XDC는 N1입니다. 보존한 원문 이미지는 수정하지 않았으며, 실습 프로젝트는 원본 XDC의 N1(KEY4)을 사용합니다. 핀표의 LVCMOSS33 오타도 실제 설정에서는 LVCMOS33으로 입력합니다.
