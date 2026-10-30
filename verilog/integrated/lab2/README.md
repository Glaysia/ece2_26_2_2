# LAB2 통합 실습

모드를 바꾸며 개별 회로를 선택하는 통합 소스.

[Verilog 목차](../../README.md) · [장치별 목차](../../../docs/devices.md)

## 소스

| 파일 | 구분 |
|---|---|
| [src/button_onepulse.v](src/button_onepulse.v) | 설계 |
| [src/clock_divider.v](src/clock_divider.v) | 설계 |
| [src/counter4.v](src/counter4.v) | 설계 |
| [src/input_frontend.v](src/input_frontend.v) | 설계 |
| [src/lab2_integrated.v](src/lab2_integrated.v) | 설계 |
| [src/lcd_lab2_modes.v](src/lcd_lab2_modes.v) | 설계 |
| [src/mealy_toggle.v](src/mealy_toggle.v) | 설계 |
| [src/moore_cycle.v](src/moore_cycle.v) | 설계 |
| [src/piso4.v](src/piso4.v) | 설계 |
| [src/register_pair.v](src/register_pair.v) | 설계 |
| [src/segment_scan8.v](src/segment_scan8.v) | 설계 |
| [src/shift_register4.v](src/shift_register4.v) | 설계 |
| [sim/tb_lab2_integrated.sv](sim/tb_lab2_integrated.sv) | 테스트벤치·모델 |
| [constraints/lab2_integrated.xdc](constraints/lab2_integrated.xdc) | 핀 제약 |

## 출처

기존 저장소 `fpga-lab2-example-vivado-09-integrated`, 커밋 `21b9d222cbda622747a69bc4c7990079d47c0f94`.
