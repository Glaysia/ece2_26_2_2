# 01_logic_gates — vivado_2026_1

[LAB1 홈](../../README.md) · [환경 준비](../../docs/setup.md) · [첫 회로 검증](VALIDATION.md)

[vivado_2026_1_01_logic_gates.code-workspace](vivado_2026_1_01_logic_gates.code-workspace)를 VS Code 새 창에서 엽니다.

공통 RTL과 자기검사 테스트벤치를 사용합니다.

1. Terminal → Run Task... → **01 Check tools**. 도구가 없으면 환경 준비 안내를 따릅니다.
2. 소스·테스트벤치를 읽고 저장합니다. **02 Simulate**로 4개 입력을 검사합니다.
3. **03 Open waveform** 또는 Explorer의 build/vscode/wave.vcd → Open With... → VaporView를 선택합니다.
4. Netlist에서 top과 신호를 추가하고 Zoom Fit, 시간 단위, 커서 값을 읽습니다.
5. 예상값·파형·로그를 비교하여 실험 전 레포트를 작성합니다.
6. Vivado GUI에서 File → Project → New...로 새 RTL 프로젝트를 만듭니다.
7. RTL·테스트벤치·XDC를 추가하고 top·part를 확인한 뒤 Run Behavioral Simulation으로 사전 결과와 비교합니다.
8. 핀을 실제 보드와 대조한 뒤 Run Synthesis → Run Implementation → Generate Bitstream을 직접 누릅니다.
9. 실제 보드 기록·사진·영상·GitHub 결과는 실험 후 레포트 절차에 따릅니다.

- [설계 소스](../../common/rtl/logic_gate.v) · [검증 테스트벤치](../../common/tb/tb_logic_gate_modern.sv) · [제약](../../common/constraints/logic_gate.xdc) · [프로젝트 설정](project.json)
- VS Code 로그/파형: build/vscode/. GUI 로그/파형: vivado/logic_gate.sim/sim_1/behav/xsim/.
- 보드 쓰기와 촬영은 자동 시뮬레이션 성공과 별개입니다.

[59쪽 실습 PDF](../../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/04.LAB1_01_LOGIC_GATES_VIVADO.pdf) · [생성된 비트스트림](release/logic_gate.bit) · [검증 로그·DRC·해시](VALIDATION.md)

학생용 시작점은 별도 [fpga-lab-template](https://github.com/Glaysia/fpga-lab-template)입니다. clone한 폴더 루트의 LAB1.code-workspace를 엽니다. 이 저장소에는 강의·검증용 첫 회로를 유지합니다.

[같은 회로의 레거시](../../legacy/01_logic_gates/README.md) · [통합 모드 01](../../docs/integrated.md#mode-01) · [Vivado XPR](vivado/logic_gate.xpr) · [재생성 Tcl](create_project.tcl) · [레포트 양식](../../docs/reports.md)
