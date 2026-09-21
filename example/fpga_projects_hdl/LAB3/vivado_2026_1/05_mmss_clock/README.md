# LAB3-23 · MM:SS 시계

설계 top은 `lab3_mmss_clock`, 기능 TB는 `tb_mmss_counter`다. MAIN CLOCK F 50 MHz와 K4 reset을 사용한다.

`mmss_counter`가 50 MHz를 1초 enable로 바꾸어 BCD 네 자리를 계수하고, top은 네 자리를 4 kHz로 스캔한다. 분과 초 사이의 decimal point를 켜서 `MM:SS`를 구분한다.

TB는 초당 두 클록으로 가속하여 `00:09→00:10`, `00:59→01:00`, `59:59→00:00`을 포함한 3,600초 전체 순환을 검사한다. 보드에서는 네 자리 순서, 공통단자 극성, 1초 정확도를 확인한다.
