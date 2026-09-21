# LAB3-25 · PC–FPGA UART 에코

설계 top은 `lab3_uart_echo`, 기능 TB는 `tb_uart_echo`다. MAIN CLOCK F 50 MHz, 9600 baud, 8 data bits, no parity, 1 stop bit를 사용한다.

- PC TX는 보드 C6의 `uart_rxd`, FPGA TX는 F6의 `uart_txd`에 연결된다.
- 수신한 한 바이트를 그대로 송신하고 마지막 수신값을 LED[7:0]에 표시한다.
- RX는 입력 동기화와 start-bit 중앙 확인, 8비트 LSB-first 샘플링, stop-bit 확인을 수행한다.
- TB는 독립 직렬 자극과 디코더로 `0x41`, `0x5A`, LF `0x0A`를 검사한다.

터미널은 9600 8N1, local echo off로 설정한다. 문자를 한 번 보냈을 때 FPGA가 반환한 문자 하나만 보이는지 확인한다. 연속 스트리밍·FIFO·줄 편집은 이 기초 실험의 범위가 아니다.
