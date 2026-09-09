# 10 modes with button and LCD

[전체 프로젝트](../../README.md) · [설치](../../docs/setup.md) · [회로별 규칙](../../docs/circuits.md) · [강의 PDF](https://github.com/Glaysia/ece2_26_2_2/blob/daily/0910/weekly-slides/weekly-slides/LAB1_FPGA_0914/04.LAB1_22_INTEGRATED_CLI.pdf) · [실험 전·후 레포트](../../docs/reports.md)

## VS Code에서 먼저 실행

1. 별도 [템플릿](https://github.com/Glaysia/fpga-lab-template)을 clone합니다.
2. VS Code의 File → New Window → Open Workspace from File...에서 `opensource_cli_integrated.code-workspace`를 엽니다.
3. Explorer에서 RTL과 `tb_lab1_integrated.sv`를 열고 예상 결과를 적습니다. File → Save All.
4. Terminal → Run Task... → **01 Check tools**, **02 Simulate** 순서로 실행합니다.
5. `LAB1_PASS lab1_integrated cases=2560`와 정상 종료를 확인합니다.
6. **03 Open waveform** → VaporView → `tb_lab1_integrated` 신호 추가 → Zoom to Fit → 커서 값을 예상값과 비교합니다.
7. `build/vscode/simulation.log`, `wave.vcd`, 자신의 화면 캡처와 해석을 실험 전 레포트에 남깁니다.

## 프로젝트 입력

- FPGA: `xc7s75fgga484-1`
- 설계 top: `lab1_integrated` / 시뮬레이션 top: `tb_lab1_integrated`
- [자기검사 TB](../../common/tb/tb_lab1_integrated.sv) / [핀 제약](../../common/constraints/lab1_integrated.xdc) / [파일 목록](sources.f)
- [logic_gate.v](../../common/rtl/logic_gate.v)
- [half_adder.v](../../common/rtl/half_adder.v)
- [full_adder.v](../../common/rtl/full_adder.v)
- [adder_4bit.v](../../common/rtl/adder_4bit.v)
- [sub_4bit.v](../../common/rtl/sub_4bit.v)
- [compare_4.v](../../common/rtl/compare_4.v)
- [mux_4x1.v](../../common/rtl/mux_4x1.v)
- [demux_1x8.v](../../common/rtl/demux_1x8.v)
- [encoder8x3.v](../../common/rtl/encoder8x3.v)
- [decoder3x8.v](../../common/rtl/decoder3x8.v)
- [seg_decoder.v](../../common/rtl/seg_decoder.v)
- [button_onepulse.v](../../common/rtl/button_onepulse.v)
- [lcd_modes.v](../../common/rtl/lcd_modes.v)
- [lab1_integrated.v](../../common/rtl/lab1_integrated.v)

Icarus Verilog로 사전 시뮬레이션하고 openXC7 흐름으로 빌드합니다. [CLI 설치·검증](../../docs/cli.md)을 따릅니다. Mac 실행 결과와 WSL 결과를 혼동하지 않습니다.

## CLI 구현과 보드 실험

사전 레포트를 마친 뒤 [CLI 안내](../../docs/cli.md)에 따라 정확한 S75 chipdb를 준비하고 `python3 ../../tools/openxc7_build.py --project .`를 실행합니다. Yosys 합성 → nextpnr 배치배선 → 프레임 변환 → bit 생성의 각 로그를 확인합니다. 생성 결과와 SHA-256은 `build/cli/result.json`에 기록됩니다.

실험실 보드 기록은 Vivado Hardware Manager의 Open target → Auto Connect → 장치 확인 → Program Device에서 수행하고 자신의 사진·영상을 실험 후 레포트에 연결합니다.

## 제작 검증

[실행 결과와 소스 SHA-256](evidence/validation.json): VS Code 단계 **PASS**, Vivado 시뮬레이션 **NOT_RUN**, Vivado bit 생성 **NOT_RUN**. 이는 제작 환경의 실행 기록이며 자신의 실행 증빙을 대신하지 않습니다. CLI 프로젝트는 [별도 검증](../../docs/cli.md)을 봅니다.

실제 보드 기록·사진·영상은 **미수행**입니다. 생성된 bit만으로 보드 실험 완료를 주장하지 않습니다.
