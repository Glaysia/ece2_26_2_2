# LAB1 공통 실습 — 빈 프로젝트에서 직접 작성하기

작성일: 2026-09-10 · 수업: 2026-09-14

[전체 계획](../../../../daily_goal/GOAL0910_2.md) · [학생 템플릿 v2.0.0](https://github.com/Glaysia/fpga-lab-template/tree/v2.0.0) · [레포트 안내](reports.md)

22개 실습은 모두 같은 빈 템플릿에서 시작한다. 완성 예시는 참고 자료이며 학생 프로젝트의 시작 파일로 배포하지 않는다. 아래 첫 회로에서는 `lab1_01_logic_gates`라는 새 폴더를 만든다. 다음 회로는 폴더 이름만 바꿔 같은 명령으로 시작한다.

```sh
git clone https://github.com/Glaysia/fpga-lab-template.git lab1_01_logic_gates
```

수업 버전을 고정하려면 `git clone --branch v2.0.0 https://github.com/Glaysia/fpga-lab-template.git lab1_01_logic_gates`를 사용한다.

## 1. 새 창과 추천 확장

1. VS Code의 **File → New Window**를 누른다.
2. 새 창에서 **File → Open Workspace from File...**을 누른다.
3. 방금 clone한 폴더의 **LAB1.code-workspace**를 선택한다. 다른 회로에서도 이 파일명은 같다.
4. 왼쪽 Explorer에 **PROJECT** 하나가 표시되는지 확인한다. `src`, `sim`, `constraints`, `simulation.json`, `tools`가 이 폴더 안에 있다.
5. 왼쪽 **Extensions** 아이콘을 누르고 검색창에 **@recommended**를 입력한다.
6. **slang**, **VaporView**, **vscode-pdf**의 **Install**을 누른다. 각각 HDL 편집·진단, 파형 보기, 교안 보기에 사용한다.

확장은 시뮬레이터 설치와 별개다. Python 3.10 이상과 Git, Icarus Verilog의 `iverilog`·`vvp`를 설치하고 PATH에 등록한 다음 VS Code를 다시 연다. WSL 사용자는 WSL 확장을 설치하고 WSL 창에서 프로젝트와 실행 도구를 함께 사용한다.

## 2. RTL과 테스트벤치를 직접 작성

1. Explorer에서 **src** 왼쪽 화살표를 누른다. **design.v**를 우클릭해 **Rename**, `logic_gate.v`를 입력한다.
2. 파일을 두 번 눌러 열고 PDF 코드 이미지의 모듈 선언·입출력·AND/OR/XOR 동작을 입력한다. 파일명과 모듈명은 별개이며 설계 모듈명은 **logic_gate**다.
3. **sim → tb_design.v → Rename**으로 `tb_logic_gate_modern.sv`를 만든다.
4. PDF에 있는 테스트벤치 전체를 입력한다. TB 모듈명은 **tb_logic_gate_modern**이다. DUT 연결, 네 입력 조합, 예상값 검사, 파형 덤프와 종료까지 작성한다.
5. **simulation.json**을 두 번 눌러 열고 다음 값으로 수정한다. 이 파일은 HDL이 아니므로 아래 내용을 복사해도 된다.

```json
{
  "sources": ["src/logic_gate.v"],
  "testbench": "sim/tb_logic_gate_modern.sv",
  "simulation_top": "tb_logic_gate_modern"
}
```

6. **File → Save All**을 누른다. 여러 RTL을 사용하는 회로는 각각 `src`에 작성하고 `sources` 배열에 모두 등록한다. `simulation_top`에는 설계 top이 아니라 TB의 모듈명을 적는다.

## 3. 예상표 → 시뮬레이션 → 수정

실행 전에 입력 00, 01, 10, 11에 대한 AND·OR·XOR 결과를 예상표에 적는다.

1. **Terminal → Run Task... → 01 Check tools**를 선택한다. 아래 터미널에서 Python·Git·Icarus의 버전과 실행 경로를 확인한다.
2. 다시 **Terminal → Run Task... → 02 Simulate**를 선택한다.
3. 터미널의 실제 컴파일 명령에 자신이 작성한 RTL과 TB가 들어 있는지 확인한다.
4. 첫 회로 TB의 `LAB1_PASS logic_gate cases=4`와 정상 종료를 확인한다. 실행기의 `SIMULATED`는 새 파형 생성까지 끝났다는 뜻이며 정답 판정을 대신하지 않는다.
5. **03 Open waveform**을 선택한다. 텍스트로 열리면 탭 우클릭 → **Reopen Editor With... → VaporView**를 선택한다.
6. Netlist에서 TB를 펼치고 입력 `a`, `b`, 출력 `x`, `y`, `z`를 추가한다. **Zoom to Fit**으로 전체 구간을 보고 전환 경계에서 떨어진 지점의 값을 예상표와 비교한다.

결과는 `build/sim/wave.vcd`에 있다. 실행별 폴더 `build/sim/run-...`에는 `compile.log`와 `simulation.log`가 있고 최근 상태는 `build/sim/result.json`에 기록된다. 실패하면 첫 오류의 파일·줄로 돌아가 수정하고 저장한 다음 02를 다시 실행한다.

첫 회로에서는 XOR 연산자 `^`를 OR 연산자 `|`로 바꾸고 저장한 뒤 다시 시뮬레이션한다. 어떤 입력에서 예상값과 달라지는지 먼저 적고, TB가 실제로 그 차이를 검출하는지 확인한다. 원래 코드로 복구하고 다시 실행해 통과와 새 파형을 확인한다. 실패·수정·복구를 자신의 실험 전 레포트에 남긴다.

## 4. XDC를 직접 작성

1. **constraints → pins.xdc → Rename**으로 `logic_gate.xdc`를 만든다.
2. PDF의 핀 표와 실제 보드 자료를 대조하며 각 `PACKAGE_PIN`, `IOSTANDARD`, `get_ports`를 직접 입력한다.
3. 첫 회로의 포트·핀은 `a=K4`, `b=N8`, `x=L4`, `y=M4`, `z=M2`이고 I/O 표준은 LVCMOS33이다. 포트 철자·대소문자가 RTL과 일치하는지 확인한다.
4. **File → Save All**을 누른다. XDC는 기능 시뮬레이션에서 읽지 않으므로 파형 통과만으로 핀 배치까지 검증됐다고 판단하지 않는다.

## 5. 자신이 작성한 파일을 Vivado에 가져오기

실험 전 레포트를 정리한 뒤 Vivado GUI를 연다. **Create Project**에서 clone 폴더 안의 `vivado`를 프로젝트 위치로 지정하고 RTL Project, 정확한 part `xc7s75fgga484-1`을 선택한다.

| Add Sources의 선택 | 직접 선택할 파일 | 확인 사항 |
|---|---|---|
| Add or create design sources | `src/logic_gate.v` | Copy sources into project 해제 |
| Add or create simulation sources | `sim/tb_logic_gate_modern.sv` | sim_1, Include all design sources for simulation 체크 |
| Add or create constraints | `constraints/logic_gate.xdc` | Copy constraints files into project 해제 |

Design Sources의 top은 **logic_gate**, Simulation Sources의 top은 **tb_logic_gate_modern**이다. 잘못 지정되었으면 모듈 우클릭 → **Set as Top**으로 수정한다. **Run Simulation → Run Behavioral Simulation**으로 같은 파일을 다시 검증하고 입력·출력·시간·검사 수를 VS Code 결과와 비교한다. 이어서 GUI의 **Run Synthesis → Run Implementation → Generate Bitstream**을 각각 실행한다.

CLI 통합 실습은 이 Vivado 절을 수행하지 않는다. 직접 작성한 같은 파일로 Icarus → Yosys → nextpnr → 프레임·bit 변환 → openFPGALoader 순서를 수행한다. 자세한 장치 DB·명령·검증 상태는 [CLI 문서](cli.md)에서 구분한다.

## 6. 레포트와 증빙

실험 전 레포트에는 직접 작성한 RTL·TB·XDC 설명, 예상표, VS Code 실행·파형, 실패와 수정 과정을 넣는다. 실험 후 레포트에는 Vivado 또는 CLI 구현 결과, bit 생성·장치 기록, 보드 사진·조작 영상, 예상값과 실측 비교를 넣는다. 자신의 GitHub 저장소에서 레포트와 증빙을 서로 링크한다. 교안의 캡처는 자신의 실행 증빙으로 제출하지 않는다.
