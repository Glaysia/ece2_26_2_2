# LAB2 순차논리 제작 목표

작성일: 2026-09-10 / 수업일: 2026-09-21

사용자 요청: 다음 주 LAB2도 완성한다. 범위의 기준은 [OT](../weekly-slides/weekly-slides/LAB0_OT_0907/03.LAB0_OT_0907.tex)의 LAB2 8개 실험이다.

| 교육 번호 | 실험 | 원본 실험 번호 |
|---|---|---|
| 11 | 업/다운 카운터 | 16 |
| 12 | 클록 분주 | 17 |
| 13 | 레지스터: 데이터 저장과 이동 | 26 |
| 14 | 시프트 레지스터 | 27 |
| 15 | PISO | 28 |
| 16 | Moore 상태 머신 | 29 |
| 17 | Mealy 상태 머신 | 30 |
| 18 | 7세그먼트 배열의 자리 스캔 | 12 |

## 결과물

- 최신 8개, 레거시 8개, 최신 Vivado 통합 1개, 오픈소스 CLI 통합 1개: 총 18개의 독립 예시 프로젝트와 개별 workspace.
- 학생은 하나의 빈 템플릿을 `git clone --branch v2.0.0 https://github.com/Glaysia/fpga-lab-template.git lab2_01_counter`처럼 다른 이름으로 복제한다. 템플릿에 정답 모음을 넣지 않는다.
- 완성 예시 프로젝트는 수업 저장소의 LAB2 아래 서브모듈로 연결한다. 초기 제작 중인 일반 디렉터리를 최종 서브모듈로 오인하지 않는다.
- [LAB2 자료 폴더](../weekly-slides/weekly-slides/LAB2_FPGA_0921)에 4:3 TeX·PDF·PDF 간 상대 링크 목차·일괄 ZIP을 만든다. 날짜는 작성일이다.

## 학생 수행 순서

1. 태그 고정 clone, VS Code 새 창, workspace 열기, 추천 확장 확인.
2. RTL·TB·simulation.json·XDC를 직접 입력하고 저장한다. 소스는 이미지로 보여 주며 긴 TB와 XDC는 첫 행부터 마지막 행까지 나눈다.
3. VS Code에서 시뮬레이션 작업을 실행하고 자기검사 로그와 파형을 확인한다.
4. 지정한 RTL 한 부분을 수정해 검사가 실패하는 이유를 설명하고 복구해 다시 통과시킨다.
5. 실험 전 레포트: 상태표·타이밍 예상, 코드 설명, 정상/변경/복구 로그, 파형, 예상과 결과의 비교.
6. Vivado GUI에서 새 프로젝트·RTL·시뮬레이션 소스·XDC 등록, top 확인, 시뮬레이션, 핀 확인, 합성, 구현, bit 생성. 자동화 task로 GUI 수업을 대체하지 않는다.
7. 실험 후 레포트: Vivado 결과·실제 장치 기록·관찰 사진·영상·GitHub 링크. CLI판은 Vivado 없이 Yosys→nextpnr→S75 bit→openFPGALoader 경로를 사용한다.

## 회로 검증 기준

- 공통: 상승 에지와 입력 변경 시점을 구분하고 동기 리셋·enable·이전 상태를 검사한다. TB는 DUT 내부 식을 그대로 복사하지 않고 기대하는 관찰 결과를 확인한다.
- 카운터: 증가·감소·양방향 wrap·hold·리셋 우선순위.
- 클록 분주: 주기·듀티·첫 전이·리셋·clock-enable 간격. 파생 클록을 다른 학습 회로의 클록으로 연결하지 않는다.
- 레지스터: 독립 load/transfer, 동시 실행 시 이전 레지스터 값 전달, nonblocking 의미.
- 시프트: 비트 이동 방향·직렬 입력·hold·리셋.
- PISO: load 우선, MSB-first 직렬 출력, 네 번 이동 뒤 zero-fill.
- Moore: 00→01→10→00, 입력만 바꿀 때 출력 유지.
- Mealy: 두 상태, 입력 0의 출력 00, 입력 1의 출력 10/01, 클록 사이 입력 변화에 따른 출력 변화.
- 자리 스캔: 8자리 순환·한 자리만 선택·자리 전환 시 blanking·0–F decode·리셋. 실제 극성과 핀은 장비 자료에 근거한다.
- 공통 버튼 동기화·디바운스와 blocking/nonblocking 설명 및 실험을 넣는다.
- 통합: 버튼으로 8개 모드를 바꾸고 LCD에 모드 표시, 각 회로의 관찰 출력과 검증 절차를 제공한다.

## 제작 제약과 증거

GUI 조작은 사용자의 명시적 중단 지시를 유지한다. 기존 실제 화면은 출처와 현재 경로 차이를 설명하고 재사용할 수 있다. 새 GUI 캡처를 조작하거나 실제 실행했다고 표시하지 않는다. 현재 소스와 일치하는 실제 VS Code 화면을 확보하지 못한 부분은 완료로 판정하지 않는다.

명령어는 검정 배경·흰색 7pt. PDF에 선택 가능한 HDL 본문/OCR을 덧붙이지 않는다. 새 PNG는 기존 ignore 정책을 따른다. 이미 추적 중인 파일과 사용자 변경을 보존한다.

## 완료 검사

- [x] 8개 최신 회로의 RTL·TB·XDC·단일 workspace와 독립 시뮬레이션
- [x] 버튼 처리 및 통합 2개와 실제 S75 CLI bit 생성 검증
- [x] 18개 예시 서브모듈·공개 고정 커밋·새 clone 시뮬레이션
- [ ] 18개 매뉴얼의 전체 코드 이미지와 단계별 GUI 설명
- [ ] 실험 전후 레포트·코드 수정 실험·오류 해석
- [ ] 전체 PDF 렌더 검수·목차/상대 링크·ZIP 새 압축 해제 검증
- [ ] TeX·PDF·예시·검증 기록 커밋 및 배포

실제 장치 실행·사진·영상은 학생 수행 절차와 제작자의 실제 수행 증거를 구분한다. 연결되지 않은 장치를 실행했다고 기록하지 않는다.

## 제작 기록 · 2026-09-10

- 8개 기능 코어·독립 TB·simulation.json·workspace를 작성했다. [소스 목록](../example/fpga_projects_hdl/LAB2/circuits.json).
- 임시 복사본에서 정상 8회, 의도한 변경 검출 8회, 복구 8회를 실행했다. 복구한 VCD는 생성 날짜를 제외한 전체 내용이 정상 실행과 일치한다. [실행 로그·입력 해시](../example/fpga_projects_hdl/LAB2/docs/core-simulation-validation.json).
- [공통 예습 TeX](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_00_START.tex)와 [26쪽 PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_00_START.pdf)를 작성했다. 전체 페이지를 렌더링해 검수했고, 4:3 및 내부 링크 30개·각 페이지 목차의 2쪽 복귀를 확인했다.
- 아직 장비 wrapper·XDC와 개별 18개 매뉴얼·통합·서브모듈 배포는 완료하지 않았다. 위 완료 검사 항목을 부분 결과만으로 체크하지 않는다. GUI 조작은 재개하지 않았다.

### 장비 연결·통합과 원고 확장

- 8개 wrapper·XDC와 입력 동기화·20 ms 디바운스·한 클록 펄스를 작성했다. 장비 연결 TB에서 버튼 튐, 긴 누름, 리셋, LED와 배열 극성을 확인했다. [검사 기록](../example/fpga_projects_hdl/LAB2/docs/board-simulation-validation.json).
- 분주는 원본의 /2·/10·/50 관찰을 유지하고 1 kHz 주 클록에서 /1000=1 Hz 기준을 추가했다. 최신판과 통합판의 LED 배치를 함께 바꿨다.
- 8모드 통합과 CLI 통합의 RTL·TB는 동일하다. 버튼 전환·새 모드 초기화·동시 버튼·LCD E/RS/RW/DATA의 실제 바이트를 검사하여 두 프로젝트 모두 2,848개 검사를 통과했다.
- WSL에서 최종 통합 소스로 정확한 S75 bit를 다시 생성했다. 3,686,926바이트, IDCODE 0x037c8093, 9,104프레임 읽기 통과. [입력 해시와 DB·bit 근거](../example/fpga_projects_hdl/LAB2/docs/cli-validation.json). nextpnr가 무시하는 set_false_path와 실제 보드·Mac 미실행을 명시한다.
- 레거시 8개 원본 파일과 현대 실행 코드의 차이를 보존했다. [18개 모두 독립 시뮬레이션](../example/fpga_projects_hdl/LAB2/docs/18-project-simulation-validation.json)을 통과했다. 서브모듈 공개 및 새 clone 검증은 다음 단계다.
- 개별 18개 TeX 원고와 원본 레거시 221쪽을 연결했다. 새 소스와 일치하는 실제 VS Code 화면 [97개 구간](../weekly-slides/weekly-slides/LAB2_FPGA_0921/required-code-captures.json)이 남아 있다. GUI 중단 지시에 따라 임의의 화면을 만들지 않고 원고에 제작 중 표시를 둔다. 개별 PDF를 완성 배포본으로 복사하지 않는다.
- Vivado batch 구현은 GUI를 조작하지 않고 순차 실행 중이다. 실행 중 변경된 분주 wrapper의 초기 결과는 [재실행 대상](../example/fpga_projects_hdl/LAB2/docs/vivado-invalidated-runs.json)으로 분리했다. 현행 소스와 일치하는 결과만 최종 근거로 사용한다.

### 공개 예시와 최종 소스 검증

- 18개 공개 저장소를 서브모듈로 연결했다. [공개 URL·고정 커밋](../example/fpga_projects_hdl/LAB2/docs/example-repositories.json)과 [새 clone 검증](../example/fpga_projects_hdl/LAB2/docs/fresh-submodule-validation.json)을 남겼다. 모든 프로젝트에서 입력 바이트 해시, 직접 시뮬레이션, Git 작업 트리 청결을 확인했다. Windows JSON 줄바꿈은 저장소 속성으로 보존한다.
- 최신 8개 및 통합 1개 모두 Vivado 2026.1 XSim과 합성·배치·배선·bit 생성을 통과했다. [XSim](../example/fpga_projects_hdl/LAB2/docs/xsim-batch-validation.json), [현행 소스·bit 감사](../example/fpga_projects_hdl/LAB2/docs/vivado-current-audit.json). 분주 초기 결과는 최종 소스로 재실행해 대체했다. GUI 실행 증거는 아니다.
- 9개 구현의 DRC 오류는 0개다. CFGBVS-1 경고가 남으므로 실제 장비 설정 뱅크 전압 확인을 완료했다고 주장하지 않는다. 실제 장치 다운로드·사진·영상은 아직 수행하지 않았다.
- 개별 18개 원고는 총 1,113쪽이며 정상 PASS 결과, 변경·복구 실험, 레포트, GUI 순서, CLI 설치·다운로드를 담았다. 실제 코드 캡처 97개가 빠져 있으므로 초안이다. 최신 목차·카운터·CLI 대표 원고를 다시 빌드했다.
- 최종 배포는 실제 코드 캡처, 전체 페이지 시각 검수, PDF 상대 링크 및 ZIP 재검증 이후다. 패키징 도구는 누락 캡처 또는 PDF/TeX 해시와 연결된 전체 검수 기록이 없으면 배포를 중단한다.
