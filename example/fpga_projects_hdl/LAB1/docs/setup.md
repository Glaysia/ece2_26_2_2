# LAB1 준비 — 첫 회로 검토본
[LAB1 홈](../README.md) · [첫 회로](../vivado_2026_1/01_logic_gates/README.md)

## 1. 설치와 버전
Windows용 Git, Python 3, VS Code, Vivado 2026.1을 설치합니다. Python 설치에서는 Add python.exe to PATH를 선택합니다.
VS Code에는 slang-server와 VaporView를 설치합니다. Nord는 화면 테마이며 회로 동작에는 영향을 주지 않습니다.

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

## 2. 고정 템플릿 clone
이번 검토본은 공개 저장소의 daily/0910 브랜치입니다. 큰 과거 교안까지 받지 않도록 sparse clone합니다.
```powershell
git clone --depth 1 --filter=blob:none --sparse --branch daily/0910 https://github.com/Glaysia/ece2_26_2_2.git lab1
cd lab1
git sparse-checkout set example/fpga_projects_hdl/LAB1
code -n example/fpga_projects_hdl/LAB1/template/LAB1.code-workspace
```
메뉴로 열려면 File → New Window → File → Open Workspace from File... → 위 LAB1.code-workspace를 선택합니다.
PROJECT와 COMMON 폴더가 보이면 올바른 창입니다. 템플릿은 첫 회로 프로젝트를 가리키며 별도의 23번째 프로젝트가 아닙니다.

## 3. 작업 메뉴
Terminal → Run Task...에서 01 Check tools, 02 Simulate, 03 Open waveform 순서로 실행합니다.
04 Create Vivado project는 준비된 소스·테스트벤치·제약을 .xpr에 등록합니다.
05 Vivado simulation은 Vivado 프로젝트의 시뮬레이션, 06 Build bitstream은 합성·배치배선·비트스트림 생성입니다.
기본 Run Build Task(Ctrl+Shift+B)는 02 Simulate입니다.

VCD가 글자로 열리면 파일 탭을 오른쪽 클릭 → Reopen Editor With... → VaporView.
Netlist에서 tb_logic_gate를 펼쳐 a,b,x,y,z를 추가하고 Zoom to Fit를 누릅니다.
첫 회로는 00→01→10→11, 각 10ns, 총 40ns를 검사합니다.
최신 검토본의 결과와 기존 레거시 교안의 200ns 간격은 구분하세요.
