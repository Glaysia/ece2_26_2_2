# LAB3-20 · RGB LED PWM

학생 시작점은 `fpga-lab-template` v2.0.2다. 설계 top은 `lab3_rgb_pwm`, 기능 TB는 `tb_rgb_pwm`이다.

- MAIN CLOCK F 50 MHz는 `clk_50mhz`, K4의 active-high reset은 `rst_p`다.
- N8·N4·N1 버튼이 각각 R·G·B duty를 0~100% 사이에서 10%씩 순환시킨다.
- 같은 색의 LED 4개는 동일한 PWM 신호를 받으며 세 색은 독립적으로 동작한다.
- 공통 `pwm_channel` 세 개와 버튼 원펄스 세 개를 인스턴스화한다.
- TB는 R=20%, G=50%, B=80%와 R만 한 단계 증가하는 조건을 자동검사한다.

파형에서는 세 PWM의 주기는 같고 HIGH 시간이 서로 다른지 확인한다. 보드에서는 세 색의 조합과 밝기를 관찰한다.
