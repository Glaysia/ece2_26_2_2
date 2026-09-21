# LAB3-24 · 문자 LCD 제어

설계 top은 `lab3_character_lcd`, 기능 TB는 `tb_character_lcd`다. 8비트 HD44780 호환 인터페이스를 write-only로 사용한다.

- 전원 안정 대기 후 `38,38,38,0C,06,01` 명령을 보낸다.
- 첫 줄 주소 `0x80`에 `FPGA LAB3`, 둘째 줄 주소 `0xC0`에 `LCD CONTROLLER`를 쓴다.
- 50 MHz에서 10 µs tick을 만들고 Enable setup/high/hold와 일반 명령·clear 대기 시간을 분리한다.
- `lcd_rw`는 항상 0이며 busy flag를 읽지 않는다.

TB는 시간을 줄인 뒤 Enable 하강 에지에서 초기화 명령과 두 줄 40바이트를 순서대로 검사한다. 실제 보드에서는 LCD 전원·대비와 문자가 안정적으로 표시되는지 확인한다.
