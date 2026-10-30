# DAC

매뉴얼에 제공된 설계 모듈과 테스트벤치를 파일로 분리했다.

[Verilog 목차](../../README.md) · [장치별 목차](../../../docs/devices.md)

## 소스

| 파일 | 구분 |
|---|---|
| [src/dac.v](src/dac.v) | 설계 |
| [src/dac_parallel8.v](src/dac_parallel8.v) | 설계 |
| [src/ramp8.v](src/ramp8.v) | 설계 |
| [sim/tb.sv](sim/tb.sv) | 테스트벤치·모델 |

이 자료에 별도 핀 제약 파일은 포함되어 있지 않다.

## 출처

`ece2_474/docs/FPGA_additional.md`의 `DAC` 항목. 코드블록 내용은 유지했다.

[원문 매뉴얼](../../../c/stm32/docs/FPGA_additional.md)
