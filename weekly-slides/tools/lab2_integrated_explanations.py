"""Shared integrated Vivado/CLI explanations from the same checked-in design."""
from lab2_intro import paras,steps,table


def architecture(d):
    d.frame('두 버튼의 역할을 나눈다', table(['입력','역할'], [('B6 / clk','1 kHz 주 클록'),('K4 / rst','전체 초기화, 첫 모드로 복귀'),('N8 / mode_button','다음 모드 선택'),('N4 / step_button','선택한 회로 한 단계 실행'),('SW1–SW8','sw[7]–sw[0], 모드별 입력')])+paras('개별 교안의 한 단계 버튼 N8은 통합판에서 N4로 바뀐다. N8은 모드 선택에 사용한다. 스위치를 먼저 정하고 버튼을 누른 뒤 놓는다.'))
    d.frame('내부 번호와 LCD 번호 · 1–4', table(['mode','LCD 첫 줄','둘째 줄'], [('0','MODE 01','UP DOWN COUNTER'),('1','MODE 02','CLOCK DIVIDER'),('2','MODE 03','REGISTER PAIR'),('3','MODE 04','SHIFT REGISTER')])+paras('mode는 3비트로 0부터 시작한다. 학생에게 표시하는 LCD 번호는 1부터 시작한다. 두 번호를 레포트에서 구분한다.'))
    d.frame('내부 번호와 LCD 번호 · 5–8', table(['mode','LCD 첫 줄','둘째 줄'], [('4','MODE 05','PISO'),('5','MODE 06','MOORE FSM'),('6','MODE 07','MEALY FSM'),('7','MODE 08','8 DIGIT SCAN')])+paras('각 줄은 16칸이며 남는 칸은 공백으로 덮어쓴다. MODE 08에서 N8을 한 번 누르면 MODE 01로 돌아온다.'))
    d.frame('여덟 회로는 하나의 bit에 함께 들어간다', paras('여덟 코어를 인스턴스화하고 mode에 따라 enable과 LED 출력 선택을 바꾼다. 모드를 바꿀 때마다 bit를 다시 기록하는 구조가 아니다.', 'counter·register·shift·PISO·Moore·Mealy는 해당 모드의 step_press로 진행한다. 스캔은 mode=7에서 자동으로 진행한다.', '분주기는 주 클록으로 계속 동작하며 mode=1에서 출력을 관찰한다. 모든 저장소의 클록은 공통 clk다.'))
    d.frame('모드를 바꾸면 상태를 초기화한다', paras('circuit_reset = reset || mode_press다. 모드 변경 펄스가 들어온 상승 에지에는 여덟 코어가 초기화되고 mode가 다음 값으로 바뀐다.', '같은 에지에서 step_press도 1이어도 코어의 reset이 우선한다. 이전 모드의 마지막 상태를 다음 모드로 넘기지 않는다.', '카운터를 15로 만든 뒤 다른 모드를 돌아 다시 MODE 01에 오면 0이다. LCD 회로는 mode_press로 리셋하지 않고 새 표시값을 다음 갱신 주기에 반영한다.'))
    d.frame('LED 선택과 사용하지 않는 표시 장치', table(['MODE','LED[7:0]'], [('01','0000, count'),('02','000, tick, /1000, /50, /10, /2'),('03','stored, registered'),('04','0000, shifted'),('05','parallel, 000, serial_out'),('06','000000, moore_value'),('07','00000, mealy_state, mealy_value'),('08','00000, scan_index')]).replace('{1.55}', '{1.3}')+paras('스캔 모드 외에는 seg_data=00, seg_com=FF로 7세그먼트를 끈다. LCD는 모든 모드에서 현재 이름을 표시한다.'))
    d.frame('LCD 한 바이트의 네 단계', table(['phase','동작'], [('0','E=0에서 RS·DATA 준비'),('1','E=1, 데이터 유지'),('2','E=0으로 내려 전송'),('3','회복 시간을 둔 뒤 다음 바이트')])+paras('1 kHz에서 각 단계는 1 ms다. lcd_rw=0으로 쓰기만 한다. 초기 POWER_WAIT=50은 50클록 대기이며 TB에서도 이 클록 수는 유지한다.'))
    d.frame('LCD 갱신 중 모드가 바뀌면', paras('첫 줄 주소 80을 전송할 때 mode를 shown_mode에 저장한다. 번호와 둘째 줄 이름은 shown_mode로 계산한다.', '따라서 한 화면을 쓰는 동안 버튼을 눌러도 번호와 이름을 서로 다른 모드에서 가져오지 않는다. 다음 화면 갱신에서 최신 mode를 반영한다.', '초기화 명령 뒤에는 두 줄의 주소·문자를 반복 전송한다. LED 모드 변화와 LCD 글자 갱신이 완전히 같은 순간일 필요는 없다.'))
    d.frame('개별 회로 설명으로 이동', r'\href{05.LAB2_01_COUNTER_VIVADO.pdf}{카운터}\quad\href{05.LAB2_02_CLOCK_DIVIDER_VIVADO.pdf}{분주}\quad\href{05.LAB2_03_REGISTER_VIVADO.pdf}{레지스터}\quad\href{05.LAB2_04_SHIFT_REGISTER_VIVADO.pdf}{시프트}\par\vspace{0.35cm}\href{05.LAB2_05_PISO_VIVADO.pdf}{PISO}\quad\href{05.LAB2_06_MOORE_VIVADO.pdf}{Moore}\quad\href{05.LAB2_07_MEALY_VIVADO.pdf}{Mealy}\quad\href{05.LAB2_08_SEGMENT_SCAN_VIVADO.pdf}{7세그먼트}\par\vspace{0.35cm}'+paras('각 코어의 상태 표·TB·수정 실험을 먼저 읽는다. 통합판은 같은 코어를 연결하며 이후 전체 코드 화면을 직접 작성한다.'))


def testbench(d):
    d.frame('통합 TB에서 빠르게 만든 부분', paras('STABLE_CYCLES=3, DIVISOR=10으로 버튼과 분주 대기를 줄인다. TB 클록 주기는 10 ns다.', '실제 보드 기본값은 STABLE_CYCLES=20, DIVISOR=1000이며 클록은 1 kHz다. TB 수치를 XDC 주기나 실제 분주 속도로 옮기지 않는다.', '같은 코어 검사 외에 두 버튼·입력 동기화·모드 선택·LCD 버스·COM 극성까지 전체 연결을 검사한다.'))
    d.frame('LCD 이름 ROM을 읽어 정답으로 쓰지 않는다', paras('TB는 실제 lcd_data·lcd_rs·lcd_e 버스를 감시해 32칸 screen을 만든다. 명령 80과 C0으로 줄 주소를 바꾸고 데이터 바이트를 저장한다.', 'E 상승 때 write-only와 setup 시간을, E 하강 때 E 유지 시간을 검사한다. E가 높은 동안 DATA 또는 RS가 바뀌면 즉시 실패한다.', 'check_lcd는 300클록을 기다린 뒤 첫 줄 번호·공백과 둘째 줄 16문자를 별도 기대 문자열에 대조한다.'))
    d.frame('여덟 모드에서 검사하는 것', table(['모드','통합 검사'], [('01','증가·감소·0에서 15로 순환'),('02','30클록에 tick 3개, TB /10'),('03','동시 저장·전달 시 이전 값'),('04','입력 1,0에 LED 08,04'),('05','병렬 load와 MSB 직렬 출력'),('06','입력만 바꿔서는 상태 유지'),('07','버튼 없이 입력으로 출력 변경'),('08','COM 극성·입력 9·blank 비율')]))
    d.frame('동시 버튼과 실행 중 리셋', paras('버튼 입력에는 짧은 바운스와 길게 누름을 포함한다. next_mode는 한 동작에 모드가 정확히 한 번만 바뀌는지 검사한다.', 'MODE 08 → MODE 01 복귀 때 이전 카운터 값이 0으로 초기화되는지 확인한다. 이어 두 버튼을 동시에 눌러 코어 갱신보다 초기화가 우선하는지 확인한다.', '마지막 전체 리셋은 mode=0, LED=0, lcd_e=0, seg_com=FF를 검사한다. 기준 로그는 modes=8, checks=2848, 종료 34326 ns다.'))


def waveform(d):
    d.frame('통합 파형은 목적별로 나누어 본다', steps('제어 파형: clk·rst·mode_button·step_button·dut.mode·dut.mode_press·dut.step_press·dut.circuit_reset.', '회로 파형: sw·led와 현재 모드의 코어 저장값. 입력 변경, 버튼 펄스, 상태 갱신 순서를 확대한다.', 'LCD 파형: lcd_e·lcd_rs·lcd_rw·lcd_data. 번호와 이름을 전송하는 구간을 확인한다.', '스캔 파형: seg_com·seg_data·dut.scan_index. 선택 신호 FF가 blank 구간인지 확인한다.', '마지막 동시 버튼과 리셋 구간을 별도 화면으로 남기고 정상 로그와 함께 설명한다.'))


def board(d):
    d.frame('통합판 영상의 촬영 순서', steps('K4 초기화 후 LCD MODE 01과 카운터 동작을 촬영한다.', 'N8을 누르고 놓아 다음 이름으로 바뀌는 장면을 찍는다. 회로 한 단계는 N4로 실행한다.', '8개 모드마다 LCD 이름·스위치 입력·출력을 함께 보여 준다.', 'MODE 08의 여덟 자리와 MODE 01로 돌아갈 때 카운터 초기화를 보여 준다.', '실제로 기록한 bit의 경로·해시와 사진·영상 링크를 README 및 실험 후 레포트에 연결한다.'))
