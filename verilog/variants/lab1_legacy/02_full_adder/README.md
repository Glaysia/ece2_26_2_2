# 전가산기 · Legacy 비교판

구형 구현과 비교하기 위한 제공 소스. 교안 ZIP 원본과도 구분한다.

[Verilog 목차](../../../README.md) · [장치별 목차](../../../../docs/devices.md)

## 소스

| 파일 | 구분 |
|---|---|
| [src/full_adder.v](src/full_adder.v) | 설계 |
| [src/half_adder.v](src/half_adder.v) | 설계 |
| [sim/tb_full_adder.sv](sim/tb_full_adder.sv) | 테스트벤치·모델 |
| [constraints/full_adder.xdc](constraints/full_adder.xdc) | 핀 제약 |

## 출처

기존 저장소 `fpga-lab-example-legacy-02-full-adder`, 커밋 `0fe260d299847628fd01626c76ae87150f601ca1`.
