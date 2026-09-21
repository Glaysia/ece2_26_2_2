# LAB3 · 주변장치와 UART

2026-09-28 수업용 최신 Vivado 2026.1 예제다. 공식 실험은 PWM LED, RGB PWM, 피에조, 스텝모터, MM:SS 시계, 문자 LCD, UART 에코의 7개다.

모든 예제는 Combo II-DLD의 MAIN CLOCK F 50 MHz와 `xc7s75fgga484-1`을 기준으로 한다. 최상위 포트는 주파수와 극성이 드러나도록 `clk_50mhz`, active-high `rst_p`로 통일한다. 주파수를 parameter로 받는 공용 하위 모듈의 클록 포트는 `clk`를 사용한다. 레거시 소스의 기능과 핀을 참고하되, 버튼 클록·fabric clock·blocking 순차 대입을 제거하고 단일 클록과 clock-enable 구조로 다시 작성한다.

`common/`은 검증 기준 원본이다. `vivado_2026_1/`의 각 폴더는 학생이 빈 템플릿에서 직접 작성할 때 비교할 수 있는 독립 완성 예시로 구성한다.

| 폴더 | 설계 top | 기능 TB |
|---|---|---|
| `01_led_pwm` | `lab3_led_pwm` | `tb_led_pwm` |
| `02_rgb_pwm` | `lab3_rgb_pwm` | `tb_rgb_pwm` |
| `03_piezo` | `lab3_piezo` | `tb_piezo` |
| `04_stepper` | `lab3_stepper` | `tb_stepper` |
| `05_mmss_clock` | `lab3_mmss_clock` | `tb_mmss_counter` |
| `06_character_lcd` | `lab3_character_lcd` | `tb_character_lcd` |
| `07_uart_echo` | `lab3_uart_echo` | `tb_uart_echo` |

학생 시작 템플릿은 `fpga-lab-template` v2.0.2다. VS Code에서는 Icarus, Vivado GUI에서는 XSim을 사용한다. 실제 장치의 밝기·음향·회전·LCD 표시는 보드에서 따로 확인한다.

7개 모두 Icarus와 XSim 기능 시뮬레이션, Vivado 2026.1 합성·구현·DRC·timing·bitstream 생성을 통과했다. 수치와 PASS marker는 [validation-summary.json](validation-summary.json)에 기록했다. 화면 캡처와 실제 보드 관찰은 다음 단계다.
