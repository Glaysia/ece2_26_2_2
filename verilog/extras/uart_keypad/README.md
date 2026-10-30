# UART·키패드 테스트

줄 단위 UART 반환, 키 입력 전송과 GPIO 모니터 소스.

[Verilog 목차](../../README.md) · [장치별 목차](../../../docs/devices.md)

## 소스

| 파일 | 구분 |
|---|---|
| [src/uart.v](src/uart.v) | 설계 |
| [src/uart_keypad_test.v](src/uart_keypad_test.v) | 설계 |
| [sim/tb_uart_9600.sv](sim/tb_uart_9600.sv) | 테스트벤치·모델 |
| [sim/tb_uart_keypad.sv](sim/tb_uart_keypad.sv) | 테스트벤치·모델 |
| [constraints/uart_keypad_test.xdc](constraints/uart_keypad_test.xdc) | 핀 제약 |

## 출처

기존 메인 저장소의 `example/uart_keypad_test`.
