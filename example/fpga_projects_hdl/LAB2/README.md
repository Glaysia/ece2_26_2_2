# LAB2 · 순차논리

2026-09-21 수업 / 자료 작성일 2026-09-10.

[전체 제작 기준](../../../daily_goal/GOAL0910_LAB2.md) · [실험 목록](circuits.json) · [18개 프로젝트](projects.json) · [통합 동작](docs/integrated.md) · [CLI 구현](docs/cli.md)

현재 8개 기능 코어·장비 연결·XDC, 레거시 비교 8개, 통합 2개의 소스를 작성했다. **18개 모두 새 임시 디렉터리에서 독립 시뮬레이션을 통과했다.** 통합 CLI는 Vivado 없이 S75 bit 생성·IDCODE·9,104프레임 읽기를 검증했다. 최신 9개 프로젝트의 Vivado batch 구현과 XSim, 18개 공개 서브모듈의 새 clone 검증도 통과했다. 개별 매뉴얼은 실제 코드 캡처·최종 PDF 검수가 남아 있는 초안이다.

- [8개 정상·변경·복구 24회](docs/core-simulation-validation.json)
- [장비 연결 8개와 버튼·배열 극성](docs/board-simulation-validation.json)
- [통합 2개, LCD 버스 포함 각 2,848개 검사](docs/integrated-simulation-validation.json)
- [18개 독립 디렉터리 실행](docs/18-project-simulation-validation.json)
- [정확한 S75 CLI bit 생성](docs/cli-validation.json)

`legacy/`는 원본을 `original/`에 보존하고, 실행 코드는 단일 클록으로 정리했다. 버튼 클록·blocking 경쟁·비동기 데이터 로드 등 원본과 현재 코드의 차이를 각 README에 설명한다. 실제 장치 기록과 촬영은 제작 PC에서 수행하지 않았다.

학생은 정답 예시 대신 같은 빈 템플릿을 회로마다 다른 폴더 이름으로 clone한다.

```powershell
git clone --branch v2.0.0 https://github.com/Glaysia/fpga-lab-template.git lab2_01_counter
cd lab2_01_counter
git switch -c main
code LAB1.code-workspace
```

`LAB1.code-workspace`와 `tools/lab1.py`는 v2.0.0 공통 템플릿의 파일명이다. LAB2에서도 한 프로젝트를 가리킨다. 추천 확장은 slang·VaporView·vscode-pdf이며, 시뮬레이션 작업은 `simulation.json`의 파일만 읽는다.

예시를 기능 시뮬레이션하려면 각 `vivado_2026_1/01_counter` 등의 디렉터리에서 `python tools/lab1.py simulate`를 실행한다. Icarus와 vvp가 PATH에 있어야 한다. VS Code에서는 Terminal → Run Task... → 02 Simulate와 동일하다.

제작 검증기는 수업 저장소 루트에서 다음과 같이 실행한다.

```powershell
python weekly-slides/tools/verify_lab2_cores.py
```

검증기는 임시 복사본에서 정상·고의 변경·복구를 실행한다. 원본 RTL을 수정하지 않는다. TB의 기대값은 유지하며 변경된 회로만 실패해야 한다. 현재 8개 회로, 총 24회가 예상대로 동작했다. 실제 GUI·Vivado·장치 검증을 의미하지 않는다.

## 공개 예시와 검증 근거

- [18개 공개 저장소·고정 커밋](docs/example-repositories.json)
- [새 clone 18개: 바이트 일치·시뮬레이션·Git 상태](docs/fresh-submodule-validation.json)
- [Vivado XSim 9개](docs/xsim-batch-validation.json)
- [Vivado 현행 소스·S75 bit·DRC 감사](docs/vivado-current-audit.json)
- [통합 코드 변경 검출과 복구](docs/integrated-modification-validation.json)
- [매뉴얼 원고와 배포 상태](../../../weekly-slides/weekly-slides/LAB2_FPGA_0921/README.md)

수업 저장소를 받은 뒤 `git submodule update --init --recursive`로 고정된 예시를 가져온다. 학생의 직접 작성 실습에는 위의 빈 템플릿 clone을 사용한다.

Vivado DRC 오류는 없지만 CFGBVS-1 경고가 남아 있다. 설정 뱅크 전압과 실제 장치 다운로드를 검증한 결과는 아니다. CLI에서도 nextpnr의 `set_false_path` 미지원과 실제 장치 미실행을 구분한다.
