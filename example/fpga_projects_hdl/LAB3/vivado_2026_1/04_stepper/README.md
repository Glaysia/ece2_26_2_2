# LAB3-22 · 스텝모터 위상 제어

설계 top은 `lab3_stepper`, 기능 TB는 `tb_stepper`다. MAIN CLOCK F 50 MHz는 `clk_50mhz`, K4의 active-high reset은 `rst_p`이며 N8 enable, N4 direction을 사용한다.

- 정방향: `0011 → 0110 → 1100 → 1001`.
- 역방향: 같은 상태를 반대 순서로 이동한다.
- enable이 0이면 현재 위상을 유지한다.
- 기본 step rate는 100 step/s이며 50 MHz 클록에서 clock-enable을 만든다.

TB는 한 단계당 네 클록으로 가속하여 정방향 한 바퀴, 역방향 두 단계, 정지 유지 조건을 검사한다. 시뮬레이션은 코일 구동 순서만 검증하며 회전 방향·토크·발열은 실제 장치에서 확인한다.
