# MM:SS 시계

LAB3 주변장치·UART 새 제공 실습.

[Verilog 목차](../../README.md) · [장치별 목차](../../../docs/devices.md)

## 소스

| 파일 | 구분 |
|---|---|
| [src/lab3_mmss_clock.v](src/lab3_mmss_clock.v) | 설계 |
| [src/mmss_counter.v](src/mmss_counter.v) | 설계 |
| [src/sevenseg_decode.v](src/sevenseg_decode.v) | 설계 |
| [sim/tb_mmss_counter.sv](sim/tb_mmss_counter.sv) | 테스트벤치·모델 |
| [constraints/lab3_mmss_clock.xdc](constraints/lab3_mmss_clock.xdc) | 핀 제약 |

## 출처

기존 메인 저장소의 `example/fpga_projects_hdl/LAB3/vivado_2026_1/05_mmss_clock`.
