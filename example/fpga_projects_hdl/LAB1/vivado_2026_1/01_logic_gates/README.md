# 01_logic_gates — vivado_2026_1

[LAB1 홈](../../README.md) · [환경 준비](../../docs/setup.md) · [첫 회로 검증](VALIDATION.md)

[vivado_2026_1_01_logic_gates.code-workspace](vivado_2026_1_01_logic_gates.code-workspace)를 VS Code 새 창에서 엽니다.

공통 RTL과 자기검사 테스트벤치를 사용합니다.

1. Terminal → Run Task... → **01 Check tools**. 도구가 없으면 환경 준비 안내를 따릅니다.
2. 소스·테스트벤치를 읽고 저장합니다. **02 Simulate**로 4개 입력을 검사합니다.
3. **03 Open waveform** 또는 Explorer의 build/vscode/wave.vcd → Open With... → VaporView를 선택합니다.
4. Netlist에서 top과 신호를 추가하고 Zoom Fit, 시간 단위, 커서 값을 읽습니다.
5. 예상값·파형·로그를 비교하여 실험 전 레포트를 작성합니다.
6. **04 Create Vivado project** → 생성된 vivado/logic_gate.xpr를 엽니다.
7. **05 Vivado simulation** 결과를 사전 결과와 비교합니다.
8. 핀을 실제 보드와 대조한 뒤 **06 Build bitstream**으로 합성·구현합니다.
9. 실제 보드 기록·사진·영상·GitHub 결과는 실험 후 레포트 절차에 따릅니다.

- [설계 소스](../../common/rtl/logic_gate.v) · [검증 테스트벤치](../../common/tb/tb_logic_gate_modern.sv) · [제약](../../common/constraints/logic_gate.xdc) · [프로젝트 설정](project.json)
- 로그/파형: build/vscode/, build/vivado-sim/. 도구·검사 결과는 result.json에 기록됩니다.
- 보드 쓰기와 촬영은 자동 시뮬레이션 성공과 별개입니다.
