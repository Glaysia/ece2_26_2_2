# LAB3-19 · PWM LED 밝기

학생은 `fpga-lab-template` v2.0.2를 `lab3_19_led_pwm`으로 clone한 뒤 이 예시의 RTL·TB·XDC를 교안에 따라 직접 작성한다.

```powershell
git clone --branch v2.0.2 https://github.com/Glaysia/fpga-lab-template.git lab3_19_led_pwm
cd lab3_19_led_pwm
git switch -c main
code FPGA.code-workspace
```

- 설계 top: `lab3_led_pwm`, 기능 TB: `tb_led_pwm`.
- MAIN CLOCK F 50 MHz는 `clk_50mhz`, K4의 active-high reset은 `rst_p`, N8은 밝기 단계 버튼이다.
- 버튼을 누를 때마다 duty가 0%부터 10% 간격으로 증가하고 100% 다음에는 0%로 돌아간다.
- LED 8개는 같은 PWM 신호를 출력한다. TB는 0%, 30%, 100%, 순환을 검사한다.
- 버튼은 2단 동기화와 20 ms 디바운스를 거치며 내부 클록으로 사용하지 않는다.

VS Code 시뮬레이션에서 PWM 한 주기의 HIGH 개수를 확인한다. 실제 밝기의 선형성은 사람의 시각과 LED 특성에 영향을 받으므로 보드에서 별도로 관찰한다.
