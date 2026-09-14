# LAB2 매뉴얼 완성 계획 — 최신 Vivado 8 + 통합 Vivado 1 + 통합 CLI 1

작성일: 2026-09-13 / 수업일: 2026-09-21

## 1. 목표와 적용 범위

학생이 빈 템플릿을 복제하고 RTL·테스트벤치·XDC를 직접 작성하여 VS Code 시뮬레이션부터 FPGA 구현까지 따라갈 수 있는 **LAB2 매뉴얼 10개**를 완성한다. 이미 검토받은 [첫 카운터 매뉴얼](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_01_COUNTER_VIVADO.pdf)을 설명 밀도·화면 구성·GUI 안내의 기준으로 삼는다.

이 계획은 [기존 LAB2 계획](GOAL0910_LAB2.md)의 제작 범위와 남은 작업 기준을 대체한다. 앞으로 구버전 Vivado 교안은 제작하지 않는다. 기존 구버전 소스·교안·검증 기록은 참고 자료로 보존하고, 이번 제작·검수·배포 대상에서 제외한다. 기존 계획에 남은 GUI 조작 중단 문구도 현재 제작 지침으로 적용하지 않는다. 필요한 VS Code·Vivado 화면은 실제 GUI에서 조작하여 촬영한다.

2026-09-13 사용자 지시로 제작을 재개한다. **VS Code 사전 시뮬레이션은 Icarus Verilog(`iverilog`·`vvp`)를 유지한다.** 템플릿은 v2.0.1로 갱신하여 사용하고, Vivado GUI 단계에서는 XSim을 사용한다. 시뮬레이터를 임의로 교체하지 않는다. 아래 순서와 완료 기준으로 남은 매뉴얼을 제작한다.

## 2. 매뉴얼 10개와 파일 구성

교안 위치: [LAB2 교안 폴더](../weekly-slides/weekly-slides/LAB2_FPGA_0921/README.md). 아래 파일마다 같은 이름의 `.tex`와 `.pdf`를 유지한다. 기존 링크를 유지하도록 파일명은 바꾸지 않는다.

| 순서 | 내용 | PDF 파일명 | 학생 프로젝트 폴더 |
|---|---|---|---|
| 1 | 업/다운 카운터 | `05.LAB2_01_COUNTER_VIVADO.pdf` | `lab2_01_counter` |
| 2 | 클록 분주 | `05.LAB2_02_CLOCK_DIVIDER_VIVADO.pdf` | `lab2_02_clock_divider` |
| 3 | 레지스터: 데이터 저장과 이동 | `05.LAB2_03_REGISTER_VIVADO.pdf` | `lab2_03_register` |
| 4 | 시프트 레지스터 | `05.LAB2_04_SHIFT_REGISTER_VIVADO.pdf` | `lab2_04_shift_register` |
| 5 | PISO | `05.LAB2_05_PISO_VIVADO.pdf` | `lab2_05_piso` |
| 6 | Moore 상태 머신 | `05.LAB2_06_MOORE_VIVADO.pdf` | `lab2_06_moore` |
| 7 | Mealy 상태 머신 | `05.LAB2_07_MEALY_VIVADO.pdf` | `lab2_07_mealy` |
| 8 | 7세그먼트 자리 스캔 | `05.LAB2_08_SEGMENT_SCAN_VIVADO.pdf` | `lab2_08_segment_scan` |
| 9 | 8모드 버튼·LCD 통합: Vivado | `05.LAB2_08A_INTEGRATED_VIVADO.pdf` | `lab2_integrated` |
| 10 | 8모드 버튼·LCD 통합: 오픈소스 CLI | `05.LAB2_08B_INTEGRATED_CLI.pdf` | `lab2_integrated_cli` |

공통 예습 `05.LAB2_00_START.pdf`와 전체 목차 `05.LAB2_00_CONTENTS.pdf`는 보조 자료다. **매뉴얼은 10개, 배포 ZIP의 PDF는 보조 자료를 포함하여 12개**로 구성한다. 구버전 PDF와 제작 중간본은 이 ZIP에 넣지 않는다.

## 3. 현재 상태와 재사용 기준

- 카운터: 75쪽 완성본을 기준으로 사용한다. VS Code·Vivado 시뮬레이션의 36개 검사/356 ns 종료, 실제 GUI 비트스트림 생성까지 확인한 상태다. 실제 보드 기록·사진·영상은 별도 항목이다.
- 나머지 9개: 기존 소스, TeX 초안, 시뮬레이션·빌드 기록을 재사용하되 학생 절차와 캡처를 완성한다. 기존 일괄 빌드 성공만으로 GUI 매뉴얼 완성을 판정하지 않는다.
- [예시 프로젝트 목록](../example/fpga_projects_hdl/LAB2/projects.json)의 최신 Vivado 9개와 CLI 1개를 이번 대상으로 사용한다. 기존 구버전 8개 예시 저장소를 삭제하거나 서브모듈 구조를 바꾸는 작업은 포함하지 않는다.
- 카운터 전용 생성기 `weekly-slides/tools/lab2_counter_complete.py`의 승인된 내용을 보존한다. 공통 생성기를 수정할 때 첫 매뉴얼을 과거 초안으로 덮어쓰지 않도록 대상 선택을 분리한다.
- 과거의 18개 원고·전체 페이지 수·누락 캡처 수는 이력이다. 이번 10개 기준으로 목록과 미완료 수를 다시 산출한다.

## 4. 학생 프로젝트의 시작점

모든 매뉴얼은 **동일한 단일 프로젝트 빈 템플릿**에서 시작한다. 템플릿에 완성 회로나 여러 실험을 미리 넣지 않는다. 예시 정답 프로젝트는 수업 저장소의 서브모듈로 별도 제공한다.

```powershell
git clone --branch v2.0.1 https://github.com/Glaysia/fpga-lab-template.git lab2_01_counter
cd lab2_01_counter
git switch -c main
code LAB1.code-workspace
```

각 교안에서는 폴더명만 해당 실험 이름으로 바꾼다. 클론 명령에 태그를 반드시 명시한다. 공유 템플릿의 기존 워크스페이스 이름은 `LAB1.code-workspace`이며 LAB2에서도 사용하는 이유를 짧게 안내한다. 추천 확장 설치와 언어 서버 정상 동작까지 확인한다. 개인 PC의 절대 경로는 템플릿이나 예시 워크스페이스에 넣지 않는다.

학생은 PDF의 실제 코드 화면을 보고 RTL, 보드 연결 모듈, 테스트벤치, `simulation.json`, XDC를 직접 작성·저장한다. 저장소에서 소스를 찾아 복사할 수 있는 학생을 막는 장치는 만들지 않는다.

## 5. 개별 Vivado 매뉴얼의 공통 흐름

1. **실험 목표와 예상 동작:** 입력·출력·클록·리셋, 보드에서 관찰할 현상을 먼저 제시한다.
2. **템플릿 복제와 VS Code:** 새 창 열기, 폴더/워크스페이스 열기, 추천 확장, 탐색기, 파일 생성·저장, 터미널 위치를 버튼과 화면으로 안내한다.
3. **소스 작성:** 파일별 역할과 전체 코드를 보여준다. 동기화·디바운스·한 클록 펄스와 핵심 회로를 연결하여 설명한다. `ASYNC_REG`, nonblocking 대입, 리셋 우선순위처럼 처음 보는 문법은 해당 위치에서 풀이한다.
4. **VS Code 시뮬레이션:** 실행할 작업을 메뉴에서 선택하는 순서, 정상 로그, 파형 열기·확대·신호 추가를 보여준다. 기대 값과 실제 파형을 연결한다.
5. **변경 실험:** 회로별 의미 있는 조건 하나를 바꾸어 기대 결과를 먼저 적고, 기존 테스트가 차이를 검출하는지 확인한 뒤 원복하여 PASS를 재확인한다. 단순 문법 오류 유발은 변경 실험으로 대신하지 않는다.
6. **실험 전 레포트:** 회로 설명, 직접 작성한 파일, 테스트 조건, VS Code 로그·파형, 변경 전후 해석을 정리한다.
7. **Vivado GUI:** 새 프로젝트 → 부품 선택 → 작성한 RTL 등록 → 테스트벤치 등록 → XDC 등록 → design/simulation top 확인 → Behavioral Simulation 순서로 안내한다. 소스와 시뮬레이션 파일의 등록 위치를 구분한다.
8. **핀과 구현:** I/O Ports의 포트·핀·전압 규격, 클록 제약을 확인한 뒤 Run Synthesis → Run Implementation → Generate Bitstream을 직접 누른다. 각 대화상자의 선택과 성공 판정 화면을 담는다. Task 4·5·6 같은 자동화 작업으로 이 GUI 절차를 대체하지 않는다.
9. **장치와 실험 후 레포트:** Hardware Manager 연결·장치 확인·Program Device 절차, 입력별 관찰표, 사진·영상 촬영 항목, GitHub 업로드와 링크 제출을 안내한다.

다른 교안을 보지 않아도 시작할 수 있게 필수 조작은 각 매뉴얼에 포함한다. 공통 개념의 긴 설명만 공통 예습 자료로 연결한다.

## 6. 회로별 검증과 설명의 핵심

| 회로 | 반드시 검증하고 파형으로 설명할 동작 |
|---|---|
| 카운터 | 증가·감소·유지, 최댓값/최솟값 순환, 리셋과 입력 우선순위 |
| 클록 분주 | 분주 주기·듀티·첫 전환·리셋, clock enable 간격; 다른 순차회로의 클록과 enable 사용 구분 |
| 레지스터 | 독립 load와 데이터 전달, 동시 동작에서 이전 값이 전달되는 nonblocking 대입 의미 |
| 시프트 레지스터 | 이동 방향, 직렬 입력, 유지·리셋, 각 클록에서 비트 위치 변화 |
| PISO | 병렬 load 우선순위, MSB부터 출력, 4회 이동과 이후 zero fill |
| Moore | 상태 전이와 상태 기반 출력, 입력만 바뀌었을 때 출력이 유지되는 구간 |
| Mealy | 상태 전이와 상태·입력 기반 출력, 클록 사이 입력 변화에 대한 출력 반응 |
| 7세그먼트 | 8자리 선택, 한 자리만 활성화, blanking, 0–F 패턴, 리셋과 보드의 활성 극성 |

최종 소스와 테스트벤치가 정의한 동작을 기준으로 표·설명·파형을 대조한다. 공통 입력 처리도 실제 버튼의 비동기 입력과 바운스를 고려하여 검증한다. 과거 로그를 인용할 때는 최종 소스 해시가 일치하는지 확인한다.

## 7. 통합 Vivado 매뉴얼

8개 회로를 버튼으로 순환 선택하고 LCD에 현재 모드 이름을 표시한다. 모드별 입력 버튼·스위치, LED·7세그먼트 출력, 리셋과 모드 진입 시 상태를 한 표에 정리한다.

빈 템플릿에서 공통 입력 처리 → 각 회로 → 모드 선택 → LCD 구동 → 통합 top → 테스트벤치 → XDC 순서로 작성한다. 각 단계의 연결 구조와 중간 시뮬레이션 결과를 제시하여 완성 코드를 한꺼번에 입력하는 데 그치지 않게 한다.

검증은 8개 모드의 기능, 마지막 모드에서 첫 모드로 순환, 버튼 한 번에 한 번만 전환, LCD 명령·문자 전송, 모드 변경 직후 출력·상태 초기화를 포함한다. LCD는 내부 문자열 변수만 확인하지 않고 외부 버스에 전달되는 바이트와 제어 신호를 확인한다. 이후 개별 매뉴얼과 동일한 Vivado GUI 경로로 시뮬레이션·구현·bit 생성·보드 기록을 설명한다.

## 8. 통합 CLI 매뉴얼

Vivado 없이 템플릿 복제 → 소스 작성 → VS Code 시뮬레이션 → Yosys 합성 → nextpnr-xilinx 배치·배선 → FASM/frames 변환 → `.bit` 생성 → openFPGALoader 기록까지 완결한다. [기존 CLI 실행 기록과 안내](../example/fpga_projects_hdl/LAB2/docs/cli.md)를 출발점으로 최종 소스에서 재현한다.

- 설치 환경, 도구 버전과 고정 다운로드 위치, FPGA 부품·패키지 DB 준비를 적는다. 환경 준비용 파일과 학생이 작성하는 회로 파일을 구분한다.
- 각 명령의 실행 위치·입력 파일·생성 파일·성공 로그를 화면과 함께 설명한다. 비트스트림의 대상 부품·IDCODE·프레임 읽기 결과를 확인한다.
- openFPGALoader 설치, 케이블 목록·장치 탐지, 실제 케이블 지정, SRAM 기록과 보드 관찰을 포함한다. WSL 사용 시 USB 전달 절차도 포함한다.
- 현재 실행 근거가 있는 WSL/Linux 경로를 우선 완성한다. macOS ARM64는 해당 환경에서 실제로 확인한 범위만 실행 완료로 표시한다.
- Vivado 통합과 동일한 8모드 기능을 검증한다. 도구별 제약 지원 차이와 실제 경고는 해당 결과를 해석하는 위치에서 설명한다.

## 9. 편집·촬영 기준

- 슬라이드는 4:3, 기존 첫 매뉴얼의 서체·색·레이아웃을 따른다. 날짜는 수업일을 작성일처럼 쓰지 않고 실제 작성일을 기입한다.
- 소스는 언어 서버가 정상 동작하는 실제 VS Code 화면을 사용한다. 학생용 설명에 테마 이름은 넣지 않는다.
- 긴 테스트벤치와 XDC는 첫 줄부터 마지막 줄까지 분할 촬영한다. 행 번호와 파일명이 보이고, 잘린 줄·누락 구간·오류 밑줄이 없는지 확인한다.
- 코드 이미지는 유지하며 선택 가능한 코드나 OCR 텍스트를 겹쳐 넣지 않는다. 명령어는 검정 배경·흰 글씨·작은 글꼴을 사용하되 PDF에서 읽을 수 있게 한다.
- GUI는 클릭 대상과 결과를 순서대로 보여준다. 합성·시뮬레이션 성공 화면을 다른 프로젝트의 화면으로 대신하지 않는다.
- 불필요한 원본 페이지 번호나 레거시 표기는 학생 본문에서 제외한다. 출처가 필요한 내용은 제작 기록에 남긴다.
- 새 캡처 PNG는 기존 ignore 정책을 유지한다. TeX·PDF·캡처 행 범위 및 소스 해시·검증 기록을 관리하며, 이미 추적 중인 이미지는 일괄 삭제하지 않는다.

## 10. 제작 순서

1. **대상 정리:** 생성·빌드·검수·패키징 도구에 이번 10개와 보조 PDF 2개의 명시적 목록을 적용한다. 목차·README·캡처 목록에서 현재 제작 대상과 구버전 이력을 구분한다.
2. **기준 고정:** 카운터 완성본을 보존하고 위 기준과의 차이만 점검한다. 변경 실험 등 빠진 항목은 필요한 만큼 보완한다.
3. **개별 7개:** 클록 분주부터 시작하여 레지스터 → 시프트 → PISO → Moore → Mealy → 7세그먼트 순서로 진행한다. 회로마다 소스 검증·실제 캡처·GUI bit 생성·PDF 검수를 끝낸 뒤 다음 회로로 넘어간다.
4. **통합 2개:** Vivado 통합을 먼저 완성하고 동일 기능의 CLI 통합을 작성한다. CLI의 bit 생성과 openFPGALoader 절차를 생략하지 않는다.
5. **공통 자료 정리:** 공통 예습과 목차를 10개 구성으로 맞추고, 예시 저장소·보고서 제출 경로·PDF 사이 링크를 연결한다.
6. **최종 배포 검수:** 모든 페이지 렌더 검수, 링크 검사, 새 폴더에 ZIP 압축 해제 후 재검증을 수행한다. 검수한 PDF와 TeX의 해시를 기록한다.

## 11. 완료 판정과 제출물

매뉴얼별로 다음 항목을 각각 기록한다. 코드 검증, GUI 촬영, 문서 완성, 실제 장치 실험을 하나의 완료 표시로 뭉치지 않는다.

- [ ] 고정 태그의 빈 템플릿에서 시작하여 학생 절차대로 소스 작성·실행을 재현했다.
- [ ] RTL·TB·설정·XDC의 전체 코드 화면을 확보하고 최종 소스와 대조했다.
- [ ] 정상·변경·원복 시뮬레이션과 파형 해석을 검증했다.
- [ ] Vivado 대상은 실제 GUI 시뮬레이션·핀 확인·bit 생성 화면을 확보했다.
- [ ] CLI 대상은 Vivado 없이 bit를 생성·검사했고 openFPGALoader 절차를 수록했다.
- [ ] 실험 전/후 레포트의 내용·사진·영상·GitHub 제출 예시를 수록했다.
- [ ] 전 페이지를 확인하여 잘림·빈 화면·임시 표시·누락 캡처를 제거했다.
- [ ] 4:3 비율, 목차 버튼, PDF 간 상대 링크를 VS Code와 Chrome에서 확인했다.
- [ ] 실제 보드 기록·관찰·사진·영상의 수행 여부를 별도로 적었다. 안내만 작성한 단계는 실측 완료로 쓰지 않았다.

최종 산출물은 **매뉴얼 TeX/PDF 10쌍, 공통 예습·목차, PDF 12개 ZIP, 최신 예시 소스와 검증 기록, 매뉴얼별 완료표**다. 실제 장치 기록이 남으면 그 사실을 완료표에서 명시한다. 이후 학생은 VS Code 예습 결과를 실험 전 레포트에, Vivado/CLI 구현과 장치 사진·영상을 실험 후 레포트 및 GitHub에 제출한다.

예시 소스를 수정하면 해당 저장소의 커밋을 먼저 공개 저장소에서 접근 가능하게 만든 뒤 상위 저장소의 서브모듈 포인터를 갱신한다. 교안 링크는 학생이 GitHub에서 실제로 열 수 있는 버전과 연결한다.


## 제작 재개 기록 · 2026-09-13

- Icarus 유지, v2.0.0 유지. 템플릿 저장소는 변경하지 않았다.
- 생성·빌드·검수·패키징 대상을 10개 매뉴얼 + 보조 PDF 2개로 변경했다. 카운터 75쪽 원고는 바이트 단위로 보존했다.
- 클록 분주: 새 태그 clone에서 정상 129개 검사/436ns, 전환 조건 변경 시 16ns 실패, 원복 PASS를 확인했다. 변경·원복은 명령줄 검증이며, 정상 실행은 VS Code 작업과 Vivado XSim GUI에서도 각각 확인했다.
- 클록 분주 79쪽 PDF: RTL·TB·설정·XDC 전체 코드 화면, VS Code 작업·파형, Vivado 프로젝트 생성·파일 등록·TB top·XSim·핀 표·합성·구현·bit 생성·타이밍 화면을 수록했다. 전체 페이지 렌더와 85개 내부 링크를 검사했다. [PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_02_CLOCK_DIVIDER_VIVADO.pdf), [검증 기록](../output/evidence/lab2-divider-0913/pdf-review.json).
- bit 생성은 실제 GUI에서 완료했으며, TIMING-18·CFGBVS-1 경고를 본문에 명시했다. 물리 보드 기록·사진·영상 촬영은 수행하지 않았고 학생 실험 절차로 안내했다.
- 다음 제작 대상은 03 레지스터다. 남은 8개 매뉴얼의 실제 캡처·GUI/CLI 구현·PDF 검수와 전체 12개 ZIP 검수는 아직 완료되지 않았다.

## v2.0.1 적용 · 2026-09-13

사용자 지시로 v2.0.1을 먼저 공개한 뒤 LAB2 전체를 완성한다. 앞의 v2.0.0 유지 기록은 당시 이력이다. 현재 기준은 **v2.0.1 / Icarus 유지 / slang 확장·서버 0.3.0**이다.

- 템플릿 main과 v2.0.1을 푸시했다. 커밋 `86c15c556e2edf1564a203180690f7ec4ad056af`.
- GitHub의 태그를 새로 clone하여 빈 프로젝트 실패와 LAB2 10개 정상 시뮬레이션을 확인했다. [검증 기록](../output/evidence/template-v2.0.1/remote.json).
- 모든 최신 매뉴얼·공통 예습의 clone을 v2.0.1로 맞춘다. 기존 실제 촬영 기록의 v2.0.0 표시는 이력으로 보존하고, 새 버전 검증과 구분한다.
- 카운터도 버전·도구 안내에 필요한 수정과 PDF 재검수를 수행한다. 기존 교육 내용과 실제 증빙은 보존한다.
- 남은 실제 GUI/CLI 촬영·10개 매뉴얼과 보조 자료의 전 페이지 검수·12개 PDF ZIP은 계속 제작 중이다.

### 현재 이어서 할 작업

- v2.0.1 템플릿 푸시와 원격 재검증 완료. main `86c15c5`, annotated tag `f4f61f4`.
- 최신 10개 TeX와 공통 예습에 v2.0.1 적용. 카운터 76쪽·분주 80쪽·레지스터 79쪽·공통 예습 27쪽과 목차를 tmp/lab2-build에 재빌드했다. 기존 배포 PDF를 아직 교체하지 않았으며 새 버전 전 페이지 재검수는 미완료다.
- 레지스터 새 안내(7쪽), 공통 템플릿 설명(4·5쪽), 신호 목록의 마지막 행 잘림 수정(39쪽)을 렌더 확인했다. 이전 78쪽 렌더와 나머지 페이지의 최종 대조 및 pdf-review.json 기록이 남아 있다.
- 시프트: 실제 VS Code Ctrl+Shift+B로 8 PASS/106ns 확인, VaporView 5신호의 0–106ns 화면 확보. 10개 실제 GUI PNG와 코드 6구간 증빙을 저장했다. 입력 전처리·XDC는 소스 해시 일치 시 기존 실제 캡처를 재사용한다. Vivado GUI 프로젝트 생성·XSim·핀 확인·bit 생성과 상세 원고 작성이 다음 작업이다.
- 시프트 학생 폴더는 기존 v2.0.0 clone 이력이며 실행기는 v2.0.1과 동일하다. 새 v2.0.1 원격 clone의 동일 소스 10개 실행 증빙은 별도 template-v2.0.1/remote.json에 있다. 새 태그에서 직접 시작하는 이후 GUI 검증은 별도 학생 폴더로 기록한다.
- 전체 완성·12 PDF ZIP·최종 커밋 및 푸시는 아직 남아 있다.

### PDF 반영 기록

- 분주 v2.0.1: 80쪽, 내부 링크 86개, PDF SHA256 `89c4e97c6a0638a30ab0ac05974bcc230b31ad6f487e86071c38991cbc20730b`. 이전 검수본 대비 변경 본문 3·7·37쪽을 직접 확인하고 나머지 본문은 렌더 픽셀로 동일함을 확인했다.
- 레지스터 v2.0.1: 79쪽, 내부 링크 85개, PDF SHA256 `4c4588007adbc9bcfa042660008fcc1b05af61bdc102a03a0c8f8643485113eb`. 변경 본문 3·4·5·7·39쪽과 전체 페이지 하단을 확인했다. RTL·TB·설정·bit 해시도 다시 대조했다.
- 두 PDF를 교안 폴더와 output/pdf에 반영했다. final-visual-review.json은 검수한 정확한 PDF·TeX 해시만 인증한다. 생성기는 해시가 바뀌면 검수 필요 상태로 돌아간다.
- 실제 VS Code/Chrome 링크 클릭 최종 확인, 카운터·공통 자료의 v2.0.1 재검수, 남은 7개 매뉴얼 제작, 12개 ZIP은 아직 남아 있다.

### 시프트 원고 보완 · 2026-09-13

- 시프트 전용 생성기 `weekly-slides/tools/lab2_shift_manual.py`를 추가했다. v2.0.1 clone부터 RTL·TB·XDC 전체 실제 코드 화면, 8개 검사 기대값, VS Code 작업·VaporView 선택·5신호 파형, 방향 반전 실패·원복, 보드 입력 순서와 레포트까지 60쪽으로 구성했다.
- PDF 전 페이지를 렌더 확인하고 파형 편집기 메뉴를 확대했다. 내부 링크 66개와 목차 목적지 2쪽, 4:3, 입력 소스 해시를 확인했다. [초안 검수 기록](../output/evidence/lab2-shift-0913/pdf-draft-review.json).
- 교안 폴더와 output/pdf의 시프트 PDF를 위 초안으로 교체했다. SHA256 `fe15789d8d135d283958095865b0bc250f90fa23b5d56f09c9616c3fbb577b86`. 43쪽에 미완료 상태를 표시했으며 최종 배포 인증에는 넣지 않았다.
- Vivado 새 프로젝트 메뉴 이후 캡처가 `CreateForMonitor 0x80070057`로 실패했다. 창 목록 갱신·재선택 후에도 실패하여 GUI 입력을 중단했다. 시프트 프로젝트의 XSim·핀·합성·구현·bit 실제 GUI 검증과 촬영은 아직 남아 있다. 화면 복구 여부는 다음 GUI 작업 전에 다시 확인한다.
- 전체 목차의 고정 쪽수 `공통 예습 26쪽`을 `공통 예습`으로 고쳐 문서 증감 시 낡은 숫자가 남지 않도록 했다. 목차 PDF 재빌드·검수는 남아 있다.

### 카운터·공통 예습 v2.0.1 PDF 반영

- 카운터 76쪽: 기존 75쪽 검수 PDF와 렌더를 대조했다. 변경된 3쪽과 추가 76쪽을 직접 확인했고 나머지 74쪽은 페이지 전체 픽셀이 동일하다. 내부 링크 82개·목차 목적지 2쪽·소스·bit·로그·GUI 캡처 해시를 확인했다. [검수 기록](../output/evidence/lab2-counter-first/pdf-review.json).
- DRC 보고서는 Git 체크아웃으로 LF→CRLF가 된 것만 달랐다. LF로 정규화한 해시는 기존 증빙과 정확히 일치한다. 원 증빙은 유지하고 현재 바이트 해시와 정규화 비교 결과를 새 검수 기록에 명시했다.
- 공통 예습 27쪽: 전체 페이지를 직접 렌더 확인했다. 내부 링크 31개·목차 목적지 2쪽을 확인했다. [검수 기록](../output/evidence/lab2-intro-0913/pdf-review.json).
- 두 PDF를 교안 폴더와 output/pdf에 반영하고 정확한 PDF·TeX 해시를 final-visual-review.json에 등록했다. 카운터·분주·레지스터의 v2.0.1 PDF와 공통 예습이 반영된 상태다.
- 전체 목차 PDF는 재빌드했지만 배포 반영·최종 검수는 아직이다. 실제 뷰어 링크 클릭·시프트 이후 7개 매뉴얼·최종 ZIP·커밋·푸시는 남아 있다.
- 이 진행 회차에서도 현재 Vivado 창을 다시 선택하여 캡처를 두 번 시도했으나 `CreateForMonitor 0x80070057`이 재현됐다. GUI 입력은 수행하지 않았다. 화면 문제와 독립적인 원고·PDF 작업은 계속할 수 있다.

### 나머지 회로·통합 설명 보완

- PISO·Moore·Mealy·7세그먼트의 RTL·코어 TB·보드 모듈·보드 TB를 직접 읽고 전용 설명 생성기를 추가했다. 제어 우선순위·상태 표·검사 시각·파형 해석·변형 실패 원인·보드 조작 29쪽을 보완하고 모두 렌더 확인했다.
- 소스 해시를 기존 정상/변형/원복 실행 증빙과 대조했다. PISO 114개/976 ns/변형 실패 86 ns, Moore 23개/226 ns/46 ns, Mealy 11개/67 ns/7 ns, 스캔 194개/1306 ns/6 ns를 확인했다.
- 통합 Vivado·CLI 두 원고에 공통 설명 15쪽씩 추가했다. 두 버튼·내부 0–7과 LCD 01–08·회로 선택·동시 입력 리셋 우선·LCD 바이트 전송과 shown_mode·실제 LCD 버스 검사·모드별 검사·파형 분류·촬영 순서를 설명했다. 8개 개별 PDF 상대 링크도 넣었다.
- 통합 RTL·TB·LCD 소스 해시를 두 프로젝트의 실행 증빙과 대조했고 2848개/34326 ns 기준을 확인했다. 공유 설명 프레임이 두 원고에 동일하게 들어감을 확인하고 Vivado판의 15쪽을 렌더 검수했다. 링크와 본문 사이 간격도 고쳤다.
- 최신 임시 빌드는 PISO 53쪽, Moore 52쪽, Mealy 53쪽, 스캔 59쪽, 통합 Vivado 93쪽, 통합 CLI 89쪽이다. 빌드 오류·overfull·누락 글자는 없다. 이 여섯 PDF는 실제 캡처가 아직 부족하여 교안 폴더의 PDF를 교체하지 않았다.
- [설명 검수 기록](../output/evidence/lab2-explanations-0913/explanation-review.json). 이 기록은 추가 설명의 검수이며 전체 매뉴얼 완료 인증이 아니다.
- 남은 핵심 작업: GUI 캡처 복구 후 시프트 Vivado와 나머지 6개 실제 코드·파형·구현 촬영, 전체 PDF 검수, 뷰어 링크, 12 PDF ZIP, 최종 커밋·푸시. CLI 구현 증빙·명령 재현성도 최종 대조한다.

### CLI 고정 설치와 구현 증빙 재검증

- 통합 CLI 설치를 변동하는 APIO 기본값 대신 OSS CAD Suite 2026-08-19·openXC7 2026-08-20 고정 패키지 다운로드로 구체화했다. Linux x86-64/Apple Silicon darwin-arm64, 전용 설치 폴더, PATH와 버전 확인을 5쪽으로 설명한다.
- 두 플랫폼의 실제 릴리스 다운로드와 압축 최상위 구조를 확인했다. S75 준비 명령에는 새 openXC7 설치 경로를 `--tools`로 명시했다. 새 경로에서 전체 설치·합성을 재실행한 것은 아니다.
- 통합 CLI 임시 PDF는 93쪽이다. 2회 XeLaTeX 빌드에서 overfull·누락 글자가 없고, 수정한 80·81쪽 링크/본문 간격을 렌더 확인했다. 전체 실제 캡처와 최종 검수가 남아 있어 배포 PDF는 교체하지 않았다.
- 보관된 CLI bit의 해시 `820224a8b513782d64607b53ae2ced58ae25c51f563fd12d3bd560a979e3835e`와 현재 RTL·TB·XDC·빌드 입력을 대조했다. bitread를 재실행하여 9104 프레임·IDCODE 0x037c8093을 확인했다. 새 합성이나 실제 보드 기록을 했다는 뜻은 아니다. [재검증 기록](../output/evidence/lab2-cli-0913/revalidation.json).
- 현재 회차에서도 Vivado 창 목록 갱신 후 캡처, 창 재선택 후 재시도 모두 `CreateForMonitor 0x80070057`로 실패했다. GUI 입력은 하지 않았다. 실제 캡처 복구·남은 매뉴얼 전체 검수·ZIP·최종 커밋/푸시는 미완료다.

### 원격 화면 복구 후 GUI 재개

- 사용자 원격 접속 복구 안내 후 캡처가 성공했다. Vivado를 앞으로 가져온 뒤 실제 레지스터 완료 화면을 확인했다.
- GUI로 시프트 프로젝트 `tmp/lab2-students-0913/lab2_04_shift_register/vivado/lab2_shift_register.xpr`를 생성했다. RTL Project·소스 나중에 등록·xc7s75fgga484-1을 선택했다.
- 이름/경로·RTL 유형·부품·요약·빈 프로젝트 화면을 assets/shift-0913/vivado/02–06 PNG로 저장했다. 다음 작업은 RTL·TB·XDC GUI 등록과 XSim·구현 촬영이다.
- 직전 전체 PDF 재빌드는 사용자 중단 후 실행 중인 python/xelatex 프로세스가 없음을 확인했다. 구조 감사는 단일 PDF 빌드 결과만 남아 실패했으므로 전체 빌드 및 감사는 다시 필요하다.


### 시프트 Vivado 검증 및 PDF 반영 · 2026-09-13

- 원격 접속 복구 후 실제 GUI에서 RTL 3개·TB·XDC 원본 참조, Simulation Top 설정, XSim 8개 검사/106 ns를 확인했다.
- 19개 핀을 대조하고 합성·구현·비트스트림 생성을 완료했다. WNS 999997.000 ns, WHS 0.122 ns, Setup·Hold 실패 0개. 실제 장치 기록은 수행하지 않았다.
- 실제 화면 26개를 보존하고 메뉴·핀 표를 확대하여 시프트 PDF 75쪽을 반영했다. 기존 VS Code 42쪽은 이전 검수본과 픽셀 동일, 새 GUI 페이지는 렌더 검수했다.
- [PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_04_SHIFT_REGISTER_VIVADO.pdf) · [검수](../output/evidence/lab2-shift-0913/pdf-review.json) · [실행 및 해시](../output/evidence/lab2-shift-0913/vivado-gui-validation.json)
- 남은 6개 매뉴얼의 실제 캡처·GUI 검증, 최종 뷰어 링크 검사·전체 ZIP·커밋/푸시는 계속 진행한다. 전체 목표는 미완료다.

### PISO 실제 VS Code 진행 · 2026-09-14

- 공개 v2.0.1을 새 학생 폴더 `tmp/lab2-students-0913/lab2_05_piso`에 clone하고 main 작업 브랜치를 만들었다.
- simulation.json·RTL·TB·XDC를 실제 VS Code에서 열고 캡처했다. 누락 코드 이미지 7개를 소스 해시와 행 범위 증거로 등록했다.
- 기본 시뮬레이션 작업을 GUI에서 실행하여 LAB2_PASS piso4 checks=114 / 976 ns 종료를 확인했다.
- 설치된 VaporView를 해당 워크스페이스에서 활성화하고 7개 신호, 전체 파형과 A 로드·유지·시프트 상세 파형을 촬영했다.
- [진행 기록](../output/evidence/lab2-piso-0913/capture-progress.json). 다음은 새 실제 캡처의 PDF 반영과 PISO Vivado GUI 검증이다. PISO PDF 전체 검수·완성은 아직 아니다.

### PISO Vivado 실제 구현 · 2026-09-14

- GUI로 PISO 프로젝트를 만들고 원본 RTL 3개·TB·XDC를 등록했다. 설계 Top은 lab2_piso, 시뮬레이션 Top은 tb_piso4다.
- XSim 114개 검사 PASS / 976 ns 종료와 전체·A 입력 상세 파형을 확인했다. 19개 핀을 XDC와 대조했다.
- 합성·구현·bit 생성을 모두 GUI에서 완료했다. bit는 3,687,012바이트, SHA256 `267957f0efe8db431790343d457425cc7987990e0e1dd43b481beb3a9048a988`이다. WNS 999997.500 ns, WHS 0.121 ns, Setup·Hold 실패 각각 0개다. 실제 보드 기록은 미실행이다.
- [실행·소스·캡처 해시 증빙](../output/evidence/lab2-piso-0913/vivado-gui-validation.json). 실제 Vivado 캡처 26개를 보존했고 PISO 전용 생성기에 구현 완료와 경고 해석을 반영했다.
- 68쪽 중간 빌드의 새 GUI 44–65쪽을 렌더 확인했다. 57쪽 로그가 작아 PASS와 종료 시각을 확대했다. 완료·타이밍 페이지를 추가한 최신 PDF 전체 검수와 배포 반영은 다음 단계다.
- 다른 5개 매뉴얼의 실제 캡처·GUI 검증, 모든 PDF 최종 검수·뷰어 링크·12개 ZIP·최종 커밋/푸시는 남아 있다.

### PISO PDF 전체 검수 완료 · 2026-09-14

- 실제 GUI 검증 화면을 반영한 74쪽 전체를 렌더 검수하고 교안 폴더와 output/pdf에 반영했다. RTL 오른쪽 끝, TB·XDC 분할, 확대된 XSim PASS 로그를 확인했다.
- [PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_05_PISO_VIVADO.pdf) · [해시 및 검수 기록](../output/evidence/lab2-piso-0913/pdf-review.json)
- Moore·Mealy·7세그먼트·통합 Vivado·통합 CLI, 최종 뷰어 링크 검사·전체 빌드·ZIP·커밋/푸시는 남아 있다. 전체 목표는 진행 중이다.

### Moore 실제 VS Code 실행·캡처 · 2026-09-14

- 공개 v2.0.1 새 clone을 `tmp/lab2-students-0913/lab2_06_moore`에 만들고 같은 원본 RTL·TB·XDC를 준비했다.
- 실제 VS Code Ctrl+Shift+B 실행: 23개 검사 PASS, 226000 ps 종료. [실행 결과](../output/evidence/lab2-moore-0914/vscode-gui-result.json).
- 설정·코어·보드 RTL·TB 전 행을 실제 화면으로 촬영해 필요한 코드 이미지 6개를 등록했다. XDC 앞뒤 및 VaporView 활성화·열기·신호 추가·전체 파형까지 원본 화면 13개를 보존했다.
- VS Code 설명 6쪽을 추가해 58쪽 초안을 빌드했다. 21–28, 33–40쪽을 직접 렌더 검수했고, PASS 로그가 작아 33쪽 캡처 확대를 수정하여 재빌드 중이다.
- Moore Vivado 실제 GUI 촬영·검증, 나머지 PDF 전체 검수는 미완료다. 최종 PDF/ZIP 배포 검수로 표시하지 않는다.
- 후속 확인: 58쪽 재빌드 완료. 확대 수정한 33쪽을 다시 렌더하여 PASS 23 로그의 가독성을 확인했다. 부분 검수 기록은 output/evidence/lab2-moore-0914/pdf-draft-review.json에 보존했다.

### Moore GUI 및 71쪽 PDF 검수 완료 · 2026-09-14

- GUI XSim PASS23/226 ns, 합성·구현·bit 생성 확인. 원본 RTL/TB/XDC 참조 및 canonical 소스 해시 일치를 검증했다. WNS 999997.250 ns, WHS 0.122 ns, setup/hold 실패 0.
- [PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_06_MOORE_VIVADO.pdf) · [검수 기록](../output/evidence/lab2-moore-0914/pdf-review.json) · [실행 기록](../output/evidence/lab2-moore-0914/vivado-gui-validation.json)
- Mealy는 원격 v2.0.1 신규 clone에서 VS Code GUI PASS11/67 ns까지 진행했다. 설정·코어 캡처 3개를 저장했으며 나머지 코드·파형·Vivado 검증은 남아 있다.
- Mealy·7세그먼트·통합 Vivado·통합 CLI 완성, 실제 뷰어 링크 검사·전체 빌드·ZIP·커밋/푸시가 남았다. 전체 목표는 진행 중이다.

### Mealy GUI 및 71쪽 PDF 검수 완료 · 2026-09-14

- 원격 연결 복구 후 GUI XSim PASS11/67 ns, 19개 핀, 합성·구현·bit 생성 확인. 원본 RTL/TB/XDC 참조와 canonical 소스 해시 일치를 검증했다. WNS 999997.750 ns, WHS 0.122 ns, setup/hold 실패 0.
- [PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_07_MEALY_VIVADO.pdf) · [검수 기록](../output/evidence/lab2-mealy-0914/pdf-review.json) · [실행 기록](../output/evidence/lab2-mealy-0914/vivado-gui-validation.json)
- 캡처 DPI를 맞추고 포인터가 코드에 겹친 화면을 실제 VS Code에서 다시 촬영했다. 71쪽 전체를 검토했다.
- 7세그먼트는 원격 v2.0.1 신규 clone에서 VS Code GUI PASS194/1306 ns를 확인했다. 코드·파형 캡처와 Vivado GUI 검증은 남았다.
- 7세그먼트·통합 Vivado·통합 CLI 완성, 실제 뷰어 링크 검사·전체 빌드·ZIP·커밋/푸시가 남았다. 전체 목표는 진행 중이다.

### 7세그먼트 GUI 및 82쪽 PDF 검수 완료 · 2026-09-14

- 공개 v2.0.1 신규 clone에서 VS Code 및 XSim PASS194/1306 ns. XSim 기본 1000 ns 뒤 Run All 필요. 35개 핀 확인, GUI 합성·구현·bit 생성 완료. WNS 999998.062 ns, WHS 0.119 ns, setup/hold 실패 0.
- [PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_08_SEGMENT_SCAN_VIVADO.pdf) · [검수 기록](../output/evidence/lab2-segment-0914/pdf-review.json) · [실행 기록](../output/evidence/lab2-segment-0914/vivado-gui-validation.json)
- 자동 스캔, blank 구간, COM 극성과 순서, SW1~4 변경을 설명하고 실제 GUI 캡처를 반영했다. 전체 82쪽 렌더 검수 완료.
- 통합 Vivado·통합 CLI 완성, 실제 뷰어 링크 검사·전체 빌드·ZIP·커밋/푸시가 남았다. 전체 목표는 진행 중이다.

### 통합 VS Code 캡처 및 CLI 108쪽 PDF 검수 완료 · 2026-09-14

- 전체 97개 고유 코드 이미지가 실제 VS Code 캡처로 등록되었다. 통합 RTL·TB·XDC 및 파형 캡처를 완료했다.
- 통합 VS Code 자기검사: modes=8, checks=2848, 종료 34326 ns. 전체 mode=0~7과 LCD MODE 05 데이터·Enable 파형을 실제 화면에서 확인하고 두 통합 교안에 공통 반영했다.
- [통합 CLI PDF](../weekly-slides/weekly-slides/LAB2_FPGA_0921/05.LAB2_08B_INTEGRATED_CLI.pdf) · [검수 기록](../output/evidence/lab2-cli-0914/pdf-review.json). 108쪽 전체 렌더 검수 및 내부 링크 113개·목차 목적지 2쪽 확인. 기존 CLI bit와 현재 소스 해시 일치 재확인.
- 통합 Vivado 새 프로젝트 GUI는 클릭 시 `foreground window did not report a process id`가 발생하여 창 재선택·활성화 후 1회 재시도했으나 같았다. 실제 통합 Vivado 생성·XSim·합성·구현·bit 검증은 아직 수행하지 않았다.
- 통합 Vivado 완성, CONTENTS 최종 검수, 12개 PDF 실제 뷰어 링크 클릭, 전체 빌드·ZIP·커밋/푸시가 남았다. 전체 목표는 계속 진행 중이다.
