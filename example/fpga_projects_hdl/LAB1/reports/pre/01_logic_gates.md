# 실험 전 레포트 예시: AND·OR·XOR

작성일 2026-09-10. 이 문서는 제작자의 실제 실행을 해석한 예시입니다. 학생은 자신의 실행 로그·화면으로 작성합니다.

## 목적과 예상값

두 입력 `a,b`에 대해 `x=a AND b`, `y=a OR b`, `z=a XOR b`를 비교합니다. 포트는 모두 1비트이고 top은 `logic_gate`입니다. AND는 둘 다 1인 경우, OR는 하나 이상 1인 경우, XOR는 서로 다른 경우에 1입니다.

| a | b | x | y | z |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

## 환경과 입력 파일

Windows, Git 2.55.0, VS Code 1.136.1, XSim 2026.1을 사용했습니다. 공개 템플릿의 커밋 `740aef5`를 공백이 있는 별도 폴더에 새로 clone했습니다. `LAB1.code-workspace`는 `vivado_2026_1/01_logic_gates`를 PROJECT, `common`을 COMMON으로 연결합니다.

[RTL](../../common/rtl/logic_gate.v), [TB](../../common/tb/tb_logic_gate_modern.sv), [XDC](../../common/constraints/logic_gate.xdc)를 사용했습니다. TB top은 `tb_logic_gate_modern`이며 `{a,b}`를 00→01→10→11 순서로 10ns씩 유지합니다. 각 조합에서 세 출력을 독립적인 기대값과 비교하고 오류면 `$fatal`로 중단합니다. 네 검사가 끝난 경우에만 PASS를 출력하고 40ns에 종료합니다.

## 실행과 관찰

VS Code 새 창에서 workspace를 열고 slang-server와 VaporView를 활성화했습니다. 저장 후 Terminal → Run Task...의 Check tools, Simulate를 실행하고 Open waveform으로 VCD를 열었습니다. `a,b,x,y,z`를 추가하고 Zoom to Fit와 ns 단위를 선택했습니다.

실제 [VS Code 작업 실행 로그](../../vivado_2026_1/01_logic_gates/evidence/template-clone-vscode.log)에서 `LAB1_PASS logic_gate cases=4`와 40ns 종료를 확인했습니다. [강의 PDF](https://github.com/Glaysia/ece2_26_2_2/blob/daily/0910/weekly-slides/weekly-slides/LAB1_FPGA_0914/04.LAB1_01_LOGIC_GATES_VIVADO.pdf)의 VS Code 화면은 해당 실행에서 캡처했습니다.

| 구간(ns) | ab | xyz | 해석 |
|---|---|---|---|
| 0–10 | 00 | 000 | 세 게이트 모두 0 |
| 10–20 | 01 | 011 | 한 입력만 1: OR·XOR만 1 |
| 20–30 | 10 | 011 | 입력을 서로 바꿔도 같은 출력 |
| 30–40 | 11 | 110 | OR와 XOR의 차이가 드러남 |

전환 순간 대신 구간 중간에서 커서를 읽었습니다. 파형만 눈으로 맞아 보이는 것에 더해 자동 비교 네 건과 정상 종료를 함께 확인했습니다.

## 보드 실험 계획

KEY1(a)=K4, KEY2(b)=N8, LED1(x)=L4, LED2(y)=M4, LED3(z)=M2, LVCMOS33입니다. Vivado에서 같은 TB를 실행한 다음 bit를 생성하고 네 입력 조합을 실제로 확인합니다. 특히 11에서 LED1·2가 켜지고 LED3가 꺼지는 장면을 사진·영상에 담을 계획입니다. 이 문서 단계의 보드 관찰은 아직 수행하지 않았습니다.
