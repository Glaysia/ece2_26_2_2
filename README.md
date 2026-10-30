# 전자전기컴퓨터설계실험Ⅱ · 소스코드 모음

교안·장비 제공 원본, 새로 제공한 Verilog 실습과 STM32 C 예제를 한 곳에 모았다. 일반 `git clone` 또는 GitHub의 Download ZIP으로 모든 소스를 받을 수 있다. 서브모듈 초기화나 별도 예제 저장소 접근은 필요하지 않다.

## 소스 찾기

| 찾는 자료 | 위치 |
|---|---|
| 장치 이름으로 찾기 | [장치·기능별 목차](docs/devices.md) |
| 교안·장비 제공 Verilog 원본 39개 | [교안 원본](verilog/textbook/README.md) |
| 새 제공 Verilog 실습 | [LAB1·LAB2·LAB3·추가·통합 실습](verilog/README.md) |
| STM32 C와 일반 C | [C 소스 모음](c/README.md) |
| 장비 제공 VHDL 통합 데모 | [Full Demo](vhdl/full_demo/README.md) |
| 직접 작성할 FPGA 틀 | [빈 템플릿](templates/fpga/README.md) |
| 기존 강의자료·TeX·PDF | [강의자료 목록](weekly-slides/README.md) |
| 출처·중복 처리·파일 해시 | [소스 통합 기록](docs/source-map.md) |

## 수록 범위

새 제공 정규 Verilog는 개별 실습 33종과 LAB1·LAB2 통합 실습 2종이다. LAB1 Legacy 비교판 10개, 보조 소스 3묶음과 공용 소스도 보존했다. 같은 LAB2 Legacy/Vivado 및 통합 Vivado/CLI 소스는 합쳤다.

C는 STM32G474 기본 프로젝트 1개와 일반 C 예시 1개다. STM32 매뉴얼의 제공 코드 9종은 별도 예제 파일로 찾을 수 있다. 과제 12개의 정답을 추가한 것은 아니다.

소스 보존과 탐색을 위한 통합본이다. 이번 통합에서 빌드·시뮬레이션·언어 서버를 검증하지 않았다. 기존 강의자료는 당시 배포 자료로 유지하며, 현재 소스 위치는 이 목차를 기준으로 찾는다.

## 강의자료 관리

강의 본문의 원본은 기존 TeX이며 PDF는 배포본이다. 기존 원고와 PDF는 이번 통합에서 수정하지 않았다. [문서 관리 안내](docs/README.md)에서 과거 초안과 기록을 구분한다.

원자료의 저작권·라이선스 표기는 각 파일과 기존 자료에 보존한다.
