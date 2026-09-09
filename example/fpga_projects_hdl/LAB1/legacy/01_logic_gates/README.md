# 01 논리 게이트 — 레거시 실습의 VS Code 사전 시뮬레이션

[LAB1](../../README.md) · [제작 목표](../../../../../daily_goal/GOAL0910.md) · [실습 PDF](../../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/04.LAB1_01_LOGIC_GATES_LEGACY.pdf)

1. VS Code에서 **File → New Window → File → Open Workspace from File...**를 선택하고 [legacy_01_logic_gates.code-workspace](legacy_01_logic_gates.code-workspace)를 연다.
2. 탐색기의 `COMMON/rtl/logic_gate.v`와 `COMMON/tb/tb_logic_gate.sv`를 확인한다.
3. **Terminal → Run Build Task...** 또는 **Ctrl+Shift+B**로 `LAB1 01: Simulate logic gates`를 실행한다.
4. 마지막 `PASS: all 4 logic-gate input combinations`를 확인한다. 로그는 `01_LOGIC_GATES/build/vscode/simulation.log`에도 저장된다.
5. `01_LOGIC_GATES/build/vscode/logic_gate.vcd`를 VaporView로 열어 a, b, x, y, z의 파형을 진리표와 비교한다.
6. 예상값, 테스트 조건, 실제 로그·파형, 비교·해석을 실험 전 레포트에 기록한 뒤 Vivado GUI 단계로 넘어간다.

VS Code는 편집기이며 실제 시뮬레이터는 설치된 Vivado의 XSim이다. **Vivado GUI를 열거나 `.xpr`를 만들 필요는 없지만 Vivado 시뮬레이션 도구 설치는 필요하다.** `xvlog`, `xelab`, `xsim`이 PATH에 있어야 한다. 별도 설치 경로는 `VIVADO_BIN` 환경 변수나 스크립트의 `-VivadoBin` 인자로 지정한다. 환경 변수를 변경했다면 VS Code를 다시 실행한다.

필수 확장: `hudson-river-trading.vscode-slang`, `lramseyer.vaporview`. [환경설정 매뉴얼](../../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/02.vscode_verilog_환경설정_매뉴얼.pdf)을 참고한다. 워크스페이스 신뢰 여부는 학생이 저장소 출처를 확인하여 결정한다.

| 구간(ns) | a | b | x(AND) | y(OR) | z(XOR) |
|---|---|---|---|---|---|
| 0–200 | 0 | 0 | 0 | 0 | 0 |
| 200–400 | 1 | 0 | 0 | 1 | 1 |
| 400–600 | 0 | 1 | 0 | 1 | 1 |
| 600–800 | 1 | 1 | 1 | 1 | 0 |

원문 테스트벤치와 같은 `10ns/100ps`, `#20` 및 입력 순서를 유지하면서 자동 검사, VCD 저장, 800ns 종료를 추가했다. 진리표의 출력과 다르면 실패한다. 실행할 때 새 작업 폴더를 만들고 이전 공개 파형을 지워 오래된 결과와 혼동하지 않게 한다. `build/`는 로컬 실행 산출물이다.

현재 범위는 사전 시뮬레이션과 안내다. 레거시 Vivado `.xpr`·보드 프로그래밍 검증의 완료를 뜻하지 않는다.

검증(2026-09-10): XSim 2026.1에서 네 조합 PASS·800ns 종료·VCD 생성, 공백이 포함된 다른 경로에서 재실행을 확인했다. 임시 사본에서 AND를 OR로 바꾸자 실패가 검출되고 이전 공개 파형이 남지 않는 것도 확인했다. UI에서는 새 창·workspace·확장·작업 선택 목록·로그 파일·VaporView의 실제 파형을 확인했다. 작업 스크립트 실행은 별도 명령 실행 도구로 검증했다.
