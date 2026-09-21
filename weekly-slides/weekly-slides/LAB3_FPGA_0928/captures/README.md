# LAB3 실제 화면 캡처

`../required-captures.json`의 42개 ID에 맞추어 실제 VS Code·Vivado 창을 PNG로 저장한다.
파일명은 `<id>.png`이며, 예: `01_led_pwm-vscode-workspace.png`.

실험마다 다음 여섯 화면이 필요하다.

- vscode-workspace: Explorer와 RTL·TB·XDC 파일
- vscode-pass: Icarus PASS marker와 종료 시각
- vscode-wave: clk_50mhz·rst_p·핵심 입출력과 시간축
- vivado-sources: Design Sources·Simulation Sources·Constraints와 top
- xsim-pass: XSim PASS와 의미 있는 파형 구간
- vivado-bit: 구현 완료·최종 WNS·DRC·bitstream 생성 결과

화면을 합성하거나 다른 실험의 화면을 재사용하지 않는다. 계정·개인 파일 등 무관한 정보가 보이지 않게 대상 창을 캡처한다.

캡처 저장 후 `python tools/generate_lab3_docs.py`로 원고를 재생성한다.
PNG가 있는 위치는 실제 이미지로 바뀌고, 없는 위치는 기존 자리표시자를 유지한다.
XeLaTeX로 원고를 두 번 빌드하고 실제 PDF 화면을 검토한 후
`python tools/package_lab3.py`를 실행한다. 모든 캡처가 있어야 최종 검증과 ZIP 생성이 통과한다.

2026-09-21: 실제 VS Code·Vivado 창 42장 촬영과 화면 확인을 완료했다. 보드 프로그래밍·실물 관찰은 수행하지 않았다.
