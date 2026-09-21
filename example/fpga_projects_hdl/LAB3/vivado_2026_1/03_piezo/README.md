# LAB3-21 · 피에조 단일 음

설계 top은 `lab3_piezo`, 기능 TB는 `tb_piezo`다. MAIN CLOCK F 50 MHz는 `clk_50mhz`, K4의 active-high reset은 `rst_p`이며 피에조 출력은 Y21이다.

기본 음은 294 Hz이며 `HALF_PERIOD = CLK_HZ / (2*TONE_HZ)`마다 출력을 반전한다. 원본처럼 1 MHz 입력을 가정하지 않고 실제 50 MHz에서 분주한다. TB는 상수를 줄여 연속 반전 사이가 정확히 다섯 클록인지 확인한다.

시뮬레이션은 디지털 출력 주기만 검증한다. 실제 음 높이와 음량은 보드의 피에조에서 확인한다.
