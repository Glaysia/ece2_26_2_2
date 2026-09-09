# LAB1 준비와 22개 workspace
[LAB1 홈](../README.md) · [첫 회로](../vivado_2026_1/01_logic_gates/README.md)

## 1. 설치와 버전
Windows용 Git, Python 3, VS Code, Vivado 2026.1을 설치합니다. Python 설치에서는 Add python.exe to PATH를 선택합니다.
VS Code에는 slang-server와 VaporView를 설치합니다.

PowerShell에서 다음을 확인합니다.
```powershell
git --version
python --version
code --version
vivado -version
xvlog --version
xelab --version
xsim --version
```
명령을 찾지 못하면 해당 도구를 설치하고 VS Code를 완전히 닫았다 다시 엽니다.
Vivado 도구를 찾지 못하면 Vivado 설치의 bin 폴더를 PATH에 추가하거나 VIVADO_BIN 환경 변수로 지정합니다.
예: C:\AMDDesignTools\2026.1\Vivado\bin. 설치 경로는 PC마다 다릅니다.
버전 출력 여부도 확인합니다. Vivado의 -version은 정상 버전 출력에도 종료 코드 1을 반환할 수 있습니다.

## 2. 별도 템플릿 clone

공개 템플릿 저장소를 clone합니다. 강의자료 저장소와 독립적으로 실행됩니다.

```powershell
git clone https://github.com/Glaysia/fpga-lab-template.git
cd fpga-lab-template
code -n LAB1.code-workspace
```

File → New Window → File → Open Workspace from File...에서 루트의 LAB1.code-workspace를 선택합니다. PROJECT와 COMMON 폴더가 보이면 올바른 창입니다.

## 3. 작업 메뉴
Terminal → Run Task...에서 01 Check tools, 02 Simulate, 03 Open waveform 순서로 실행합니다.
Vivado 단계는 task로 실행하지 않습니다. Vivado GUI에서 새 프로젝트를 만들고 RTL·테스트벤치·XDC를 추가한 뒤 Run Behavioral Simulation → Run Synthesis → Run Implementation → Generate Bitstream을 직접 선택합니다. 자세한 화면별 안내는 강의자료 PDF를 따릅니다.
기본 Run Build Task(Ctrl+Shift+B)는 02 Simulate입니다.

VCD가 글자로 열리면 파일 탭을 오른쪽 클릭 → Reopen Editor With... → VaporView.
Netlist에서 tb_logic_gate_modern을 펼쳐 a,b,x,y,z를 추가하고 Zoom to Fit를 누릅니다.
첫 회로는 00→01→10→11, 각 10ns, 총 40ns를 검사합니다.
배포 자기검사 TB의 시간과 원본 교안 testbench의 시간은 구분하세요.

## 4. 다른 회로와 통합본

[전체 목록](../README.md)에서 회로를 고르고 해당 폴더의 `.code-workspace`를 엽니다. 최신은 `vivado_2026_1`, 레거시는 `legacy`, CLI 통합은 `opensource_cli/integrated`입니다. 프로젝트마다 실행 디렉터리와 TB가 달라지므로 파일 하나만 여는 대신 전용 workspace를 사용합니다. 통합본의 모드·DIP·LCD 연결은 [통합 안내](integrated.md)를 봅니다.

레거시 XPR은 Vivado 2020.1 원본 형식을 유지했습니다. 설치된 2026.1 XSim으로 먼저 RTL을 검사할 수 있지만 2020.1 GUI·합성 검증과 같지 않습니다. 새 버전에서 XPR을 열면 변환될 수 있으므로 원본은 `original/`에 보존했습니다.

CLI 사용자는 [macOS ARM64·WSL 설치](cli.md)를 따릅니다. 해당 workspace는 Icarus Verilog를 실행합니다. WSL에서 열었다면 Python·도구·확장도 WSL 환경을 사용해야 합니다.

## 5. 실행 문제에서 복귀

- 작업이 보이지 않음: File → Open Workspace from File...로 올바른 전용 workspace를 다시 선택합니다.
- 파일을 못 찾음: 전체 템플릿을 clone했는지 확인합니다. 프로젝트 폴더만 따로 옮기면 `../../common` 연결이 끊어집니다.
- 컴파일 오류: 실제 실행 폴더 `build/vscode/run-...`의 compile.log부터 확인합니다. elaborate.log와 simulation.log를 차례로 읽습니다.
- 파형이 오래된 것 같음: File → Save All, 02 Simulate를 다시 실행한 뒤 wave.vcd를 닫았다 엽니다. PASS와 검사 수·종료 시각을 확인합니다.
- 버전 명령 실패: 설치 경로와 PATH 또는 VIVADO_BIN을 확인하고 VS Code를 다시 실행합니다.

[실험 전·후 레포트](reports.md)에 자신의 오류·수정·재실행 기록까지 남깁니다.
