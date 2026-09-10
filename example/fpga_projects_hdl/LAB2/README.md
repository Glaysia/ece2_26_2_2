# LAB2 · 순차논리

2026-09-21 수업 / 자료 작성일 2026-09-10.

[전체 제작 기준](../../../daily_goal/GOAL0910_LAB2.md) · [실험 목록](circuits.json) · [기능 검증 기록](docs/core-simulation-validation.json)

현재는 **8개 기능 코어와 독립 자기검사 TB를 제작한 단계**다. 장비 핀 wrapper·XDC, 통합 2개, 레거시 8개, 공개 서브모듈, 개별 매뉴얼은 작업 중이다. 이 디렉터리를 하드웨어까지 완성한 배포판으로 사용하지 않는다.

학생은 정답 예시 대신 같은 빈 템플릿을 회로마다 다른 폴더 이름으로 clone한다.

```powershell
git clone --branch v2.0.0 https://github.com/Glaysia/fpga-lab-template.git lab2_01_counter
cd lab2_01_counter
git switch -c main
code LAB1.code-workspace
```

`LAB1.code-workspace`와 `tools/lab1.py`는 v2.0.0 공통 템플릿의 파일명이다. LAB2에서도 한 프로젝트를 가리킨다. 추천 확장은 slang·VaporView·vscode-pdf이며, 시뮬레이션 작업은 `simulation.json`의 파일만 읽는다.

제작 중인 예시를 기능 시뮬레이션하려면 각 `vivado_2026_1/01_counter` 등의 디렉터리에서 `python tools/lab1.py simulate`를 실행한다. Icarus와 vvp가 PATH에 있어야 한다. VS Code에서는 Terminal → Run Task... → 02 Simulate와 동일하다.

제작 검증기는 수업 저장소 루트에서 다음과 같이 실행한다.

```powershell
python weekly-slides/tools/verify_lab2_cores.py
```

검증기는 임시 복사본에서 정상·고의 변경·복구를 실행한다. 원본 RTL을 수정하지 않는다. TB의 기대값은 유지하며 변경된 회로만 실패해야 한다. 현재 8개 회로, 총 24회가 예상대로 동작했다. 실제 GUI·Vivado·장치 검증을 의미하지 않는다.
