# LED PWM

LAB3 주변장치·UART 새 제공 실습.

[Verilog 목차](../../README.md) · [장치별 목차](../../../docs/devices.md)

## 소스

| 파일 | 구분 |
|---|---|
| [src/button_onepulse.v](src/button_onepulse.v) | 설계 |
| [src/lab3_led_pwm.v](src/lab3_led_pwm.v) | 설계 |
| [src/pwm_channel.v](src/pwm_channel.v) | 설계 |
| [sim/tb_led_pwm.sv](sim/tb_led_pwm.sv) | 테스트벤치·모델 |
| [constraints/lab3_led_pwm.xdc](constraints/lab3_led_pwm.xdc) | 핀 제약 |

## 출처

기존 메인 저장소의 `example/fpga_projects_hdl/LAB3/vivado_2026_1/01_led_pwm`.
