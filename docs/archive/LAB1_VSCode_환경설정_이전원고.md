> 과거 기록 — 강의자료의 SSOT는 TeX다. 이 문서의 일정·도구·경로·완료 표시는 현재 기준으로 사용하지 않는다. 당시 내용을 보존하며 업데이트하지 않는다.
>
> [문서 분류와 현재 작업](../README.md) · [강의자료](../../weekly-slides/README.md)

# LAB1 · VS Code Verilog 환경설정 매뉴얼

전자전기컴퓨터설계실험Ⅱ · 이해리 · 2026. 09. 14.

이 매뉴얼에서는 전가산기 예제로 **코드 작성 → 오류 확인 → 시뮬레이션 → 파형 해석**까지 진행한다. Windows와 Vivado 2026.1을 기준으로 하며, Vivado 설치는 앞의 설치 매뉴얼에 따라 완료한다.

## 1. 무엇을 설치하며, 왜 필요한가?

VS Code에서 파일을 열 수 있는 것과 회로를 이해하며 작업할 수 있는 것은 다르다. 언어 서버는 모듈·신호·연결 관계를 분석하여 정의로 이동, 심벌 정보와 오류 진단을 제공한다. 여러 파일로 나뉜 회로를 읽고 수정할 때 필요한 기능이다.

| 도구 | 역할 | 이 실습의 확인 방법 |
|---|---|---|
| VS Code | 소스 편집, 터미널과 작업 실행 | 프로젝트 열기, `code --version` |
| Git | 예제 내려받기와 변경 이력 관리 | `git --version` |
| GitHub CLI (`gh`) | 터미널에서 GitHub 로그인·저장소 작업 | 사용하는 경우 `gh --version` |
| vscode-slang 확장 + slang-server | Verilog/SystemVerilog 분석 | Ctrl+클릭, 심벌 설명, 오류 진단 |
| Vivado XSim | HDL 컴파일과 시간에 따른 회로 시뮬레이션 | `xvlog`, `xelab`, `xsim` 실행 |
| VaporView 확장 | 생성된 VCD 파일을 파형으로 표시 | 입력·출력 신호의 80 ns 파형 확인 |

이 예제에서 “VS Code 시뮬레이션”은 **VS Code의 작업으로 Vivado XSim을 실행하고, VaporView에서 결과를 보는 과정**을 뜻한다. 언어 서버가 시뮬레이션을 수행하는 것은 아니다.

## 2. VS Code와 Git 설치

1. [VS Code Windows 설치 안내](https://code.visualstudio.com/docs/setup/windows)에서 설치 프로그램을 받아 설치한다. 개인 PC에서는 User Setup을 사용할 수 있다.
2. 설치 중 PATH에 추가하는 옵션을 확인한다. PATH는 터미널에서 실행 파일의 전체 경로를 입력하지 않고 명령을 찾도록 하는 설정이다.
3. [Git for Windows](https://git-scm.com/install/windows)를 설치한다. 명령줄과 다른 프로그램에서 Git을 사용할 수 있는 PATH 옵션을 선택한다.
4. 설치가 끝나면 VS Code와 기존 터미널을 닫고 다시 연다.
5. VS Code의 **Terminal → New Terminal**에서 PowerShell 터미널을 연다.

```powershell
git --version
code --version
Get-Command git, code | Select-Object Name, Source
```

**완료 기준:** 버전과 실행 파일 경로가 출력된다. `code --version`은 버전 외에 커밋·아키텍처 등이 여러 줄로 나올 수 있다.

GitHub CLI도 사용할 경우 [GitHub CLI](https://cli.github.com/)를 설치한 뒤 확인한다. `gh`는 Git과 별도 프로그램이며, 이 예제의 `git clone`과 시뮬레이션에는 필수가 아니다.

```powershell
gh --version
Get-Command gh | Select-Object Name, Source
gh auth login
gh auth status
```

로그인은 화면 안내에 따라 GitHub.com과 브라우저 인증을 선택한다. 자세한 절차는 [공식 로그인 안내](https://cli.github.com/manual/gh_auth_login)를 따른다. 버전 옵션은 `gh --version`이며 `gh --versions`가 아니다.

## 3. Vivado 도구의 PATH와 버전 확인

Vivado GUI가 열리더라도 VS Code 터미널에서 시뮬레이션 명령을 찾지 못할 수 있다. 다음 세 실행 파일이 있는 **본인 Vivado 설치 폴더의 `bin`**을 확인한다.

- `xvlog.bat`: Verilog/SystemVerilog 소스 컴파일
- `xelab.bat`: 최상위 테스트벤치와 하위 모듈을 연결하여 실행 모델 생성
- `xsim.bat`: 시뮬레이션 실행

Windows 검색 → **계정의 환경 변수 편집** → 사용자 변수 **Path → 편집 → 새로 만들기**에서 해당 `bin` 폴더를 추가한다. 기존 Path 항목은 유지한다. 예를 들어 설치 위치가 아래와 같다면 이 경로를 등록한다.

```text
C:\AMDDesignTools\2026.1\Vivado\bin
```

경로는 설치 위치에 따라 다르다. 파일 탐색기에서 실제로 세 `.bat` 파일이 있는지 확인한 뒤 등록한다. 실행 파일 자체가 아닌 폴더 경로를 넣는다.

VS Code를 완전히 종료하고 다시 실행한 뒤 새 PowerShell 터미널에서 확인한다.

```powershell
Get-Command xvlog.bat, xelab.bat, xsim.bat | Select-Object Name, Source
xvlog -version
xelab -version
xsim -version
```

**완료 기준:** 세 도구 모두 실행되고 2026.1 버전이 표시된다. Vivado 도구는 `--version`이 아니라 **`-version`**을 사용한다.

다른 버전이 실행되면 다음 명령으로 경로 순서를 확인하고 사용자 Path를 수정한다.

```powershell
Get-Command xvlog.bat, xelab.bat, xsim.bat -All | Select-Object Name, Source
```

이후 예제 스크립트가 별도로 지정된 `VIVADO_BIN`을 사용하는 경우도 있다. 설정된 값은 `$env:VIVADO_BIN`으로 확인한다. 일반 실습에서는 PATH를 기준으로 통일한다.

## 4. 전가산기 예제 받기

[수업 예제 저장소](https://github.com/Glaysia/ece2_26_2_2)를 내려받는다. 예제를 저장할 상위 폴더에서 다음 명령을 실행한다.

```powershell
git clone https://github.com/Glaysia/ece2_26_2_2.git
cd ece2_26_2_2/fpga_projects_hdl/example_full_adder_hdl
code example_full_adder_hdl.code-workspace
```

첫 줄은 저장소를 내려받고, 두 번째 줄은 전가산기 프로젝트 폴더로 이동하며, 마지막 줄은 VS Code 작업 영역을 연다.

GUI로 열 때는 **File → Open Workspace from File…**에서 `example_full_adder_hdl.code-workspace`를 선택한다. 또는 **File → Open Folder…**로 `example_full_adder_hdl` 폴더 자체를 연다.

**완료 기준:** VS Code 탐색기 최상위에 `src`, `sim`, `scripts`, `.vscode`, `.slang`, `sources.f`가 보인다. 상위 저장소나 `fpga_projects_hdl`만 열면 예제의 작업 설정이 적용되지 않을 수 있다. 작업 영역 신뢰 안내가 나오면 내려받은 수업 예제임을 확인하고 신뢰를 선택한다.

```text
example_full_adder_hdl/
├─ example_full_adder_hdl.code-workspace
├─ .vscode/                 확장 추천, 편집 설정, 실행 작업
├─ .slang/server.json       언어 서버 설정
├─ sources.f                분석할 HDL 소스 목록
├─ src/
│  ├─ half_adder.v          반가산기
│  └─ full_adder.v          전가산기
├─ sim/tb_full_adder.sv      테스트벤치
├─ scripts/                 도구 확인과 시뮬레이션 스크립트
└─ build/                   실행 후 생성되는 파형과 로그
```

## 5. 확장과 언어 서버 설치

### 5.1. 확장 두 개 설치

`Ctrl+Shift+X`로 Extensions 화면을 열고 아래 **확장 ID**를 검색하여 설치한다. 이름이 비슷한 다른 확장과 구분한다.

| 확장 ID | 용도 |
|---|---|
| `Hudson-River-Trading.vscode-slang` | Verilog/SystemVerilog 언어 지원 |
| `lramseyer.vaporview` | VCD 파형 보기 |

명령으로 설치할 수도 있다.

```powershell
code --install-extension Hudson-River-Trading.vscode-slang
code --install-extension lramseyer.vaporview
code --list-extensions --show-versions | Select-String 'slang|vaporview'
```

### 5.2. slang-server 설치 알림 확인

1. `src/full_adder.v`를 연다.
2. 언어 서버 다운로드 안내가 나타나면 **Install slang-server**를 선택한다. 표시 문구는 확장 버전에 따라 달라질 수 있다.
3. 다운로드와 초기 분석이 완료될 때까지 기다린다.
4. 필요하면 명령 팔레트(`Ctrl+Shift+P`)에서 **Developer: Reload Window**를 실행한다.

확장은 서버 바이너리의 자동 설치를 안내하고, 사용자가 허용하면 내려받아 관리한다. 이미 서버가 설치되어 있으면 알림이 다시 나타나지 않을 수 있다. [slang-server 공식 설치 안내](https://hudson-trading.github.io/slang-server/start/installing/)

**자동 설치 방식에서는 `slang-server`를 사용자 PATH에 추가할 필요가 없다.** `slang.path`도 직접 입력하지 않는다. 수동 설치를 선택할 때만 해당 실행 파일을 지정한다. 따라서 터미널에서 `slang-server` 명령을 찾지 못한다는 이유만으로 자동 설치가 실패했다고 판단하지 않는다. 다음 절의 편집 기능으로 확인한다.

## 6. 언어 서버가 제대로 동작하는지 확인

### 6.1. 색상과 심벌 정보

`src/full_adder.v`를 열고 모듈 이름, 키워드와 신호가 구분되는지 확인한다. 예제는 `editor.semanticHighlighting.enabled`를 켜 두었다. 실제 색은 VS Code 테마에 따라 다르며, 색상만으로 언어 서버 동작을 판정하지 않는다.

`half_adder` 모듈 이름이나 포트 위에 마우스를 올려 심벌 정보를 확인한다.

### 6.2. Ctrl+클릭으로 다른 파일의 정의로 이동

전가산기는 반가산기 두 개를 연결한다. 다음 코드의 **`half_adder`** 위에서 `Ctrl+클릭` 또는 `F12`를 누른다.

```verilog
half_adder u_first (
    .a(a),
    .b(b),
    .sum(first_sum),
    .carry(first_carry)
);
```

**완료 기준:** `src/half_adder.v`의 `module half_adder` 정의로 이동한다. `Alt+왼쪽 화살표`로 이전 위치에 돌아온다.

### 6.3. 오류 진단 확인 후 복원

1. `full_adder.v`의 아래 문장에서 마지막 세미콜론을 잠시 지운다.
2. 저장하고 오류 밑줄 또는 **Problems**(`Ctrl+Shift+M`)의 진단을 확인한다.
3. `Ctrl+Z`로 복원하고 다시 저장한다.
4. 문법 오류가 사라진 다음 시뮬레이션으로 넘어간다.

```verilog
assign carry_out = first_carry | second_carry;
```

오류 위치는 누락된 기호 다음 줄에 표시될 수도 있다. 경고는 문법 오류와 구분해서 읽는다. 경고가 있다는 사실만으로 동작 실패를 뜻하지는 않지만, 무엇을 지적하는지 확인한다.

프로젝트의 `.slang/server.json`은 `sources.f`를 사용하고, `sources.f`에는 반가산기·전가산기·테스트벤치가 등록되어 있다. 파일을 추가하는 실험에서는 분석 대상 목록도 함께 확인한다. [프로젝트 설정 안내](https://hudson-trading.github.io/slang-server/start/config/)

## 7. 시뮬레이션 전에 예상 결과 정하기

입력 `a`, `b`, `carry_in`은 각각 1비트이며 출력은 `sum`, `carry_out`이다. 두 출력으로 입력 세 개의 합을 표현한다.

```text
{carry_out, sum} = a + b + carry_in
```

| a | b | carry_in | carry_out | sum |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 |

`sim/tb_full_adder.sv`는 입력 `000`부터 `111`까지 각각 10 ns 동안 유지하고, 입력 변경 1 ns 뒤 예상값과 출력을 비교한다. 전체 시뮬레이션은 80 ns이다. 이 회로는 조합회로이므로 클록 입력이 없다. 검사 전의 1 ns 대기는 실제 FPGA의 전파 지연 측정값이 아니다.

## 8. VS Code에서 시뮬레이션 실행

1. 모든 소스 파일을 저장한다.
2. `Ctrl+Shift+P` → **Tasks: Run Task** → **HDL: Check tools**를 실행한다.
3. Vivado 도구 세 개의 경로와 버전을 확인한다.
4. `Ctrl+Shift+B`로 기본 작업 **HDL: Simulate full adder**를 실행한다. 또는 Tasks: Run Task에서 해당 작업을 선택한다.
5. 터미널에서 아래 성공 문구를 확인한다.

```text
PASS: all 8 full-adder input combinations
```

**완료 기준:** 8개 입력 검사가 통과하고 `build/full_adder.vcd`가 생성된다. 터미널의 `Waveform:`은 파형 위치, `Logs:`는 이번 실행의 로그 폴더를 알려 준다.

같은 작업을 프로젝트 폴더의 PowerShell 터미널에서 직접 실행할 수도 있다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/check-tools.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/simulate.ps1
```

`ExecutionPolicy Bypass`는 이 실행 프로세스에 적용하는 옵션이다. 시스템의 영구 실행 정책을 변경할 필요는 없다.

PATH 문제를 진단할 때는 자신의 실제 설치 경로를 명시할 수 있다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/simulate.ps1 -VivadoBin 'C:\AMDDesignTools\2026.1\Vivado\bin'
```

스크립트는 `xvlog → xelab → xsim` 순서로 실행한다. 중간 단계가 실패하면 다음 단계로 진행하지 않는다. `build/run-…/`의 `compile.txt`, `elaborate.txt`, `simulation.txt`에서 해당 실행의 원인을 확인한다.

## 9. VaporView에서 파형 확인

1. 탐색기에서 `build/full_adder.vcd`를 연다.
2. 텍스트로 열리면 파일을 우클릭하여 **Open With… → VaporView**를 선택한다.
3. VaporView의 Netlist에서 `tb_full_adder`를 펼친다.
4. `a`, `b`, `carry_in`, `sum`, `carry_out`을 더블클릭하거나 옆의 `+`로 파형에 추가한다.
5. 파형 창에 포커스를 두고 **Zoom to Fit**(`Ctrl+0`)으로 전체 구간을 표시한다.
6. 커서를 각 구간에 놓고 진리표와 비교한다.

| 시간 구간 | a, b, carry_in | 확인할 출력 |
|---|---|---|
| 0–10 ns | 000 | carry_out=0, sum=0 |
| 30–40 ns | 011 | carry_out=1, sum=0 |
| 70–80 ns | 111 | carry_out=1, sum=1 |

표의 세 구간을 먼저 찾은 다음 나머지 다섯 구간도 확인한다. 시간 단위가 ps이면 **10,000 ps = 10 ns**이다. [VaporView 공식 사용 안내](https://marketplace.visualstudio.com/items?itemName=lramseyer.vaporview)

코드를 수정하면 저장 → 시뮬레이션 재실행 → 파형 다시 열기 또는 새로고침 순서로 확인한다. 예제 스크립트는 실행 시작 시 이전 대표 VCD를 제거하고, 검사가 성공했을 때 새 결과를 복사한다. 실패 후에는 이미 열어 둔 파형을 새 결과로 해석하지 않는다.

## 10. 실험 전 보고서에 담기

이 전가산기 예제로 환경을 확인한 뒤, **LAB1에 배정된 전체 10개 실험**에 같은 검증 절차를 적용한다. 이 배포 프로젝트에는 전가산기 예제만 들어 있다.

각 실험에는 설계 내용과 핵심 코드, 시험 입력과 예상 결과, VS Code에서 확인한 파형과 해석을 담는다. 스크린샷에는 파일명·신호명·시간축·입출력 변화가 읽히도록 표시한다. 파형을 작게 축소해 한 장에 모두 넣기보다 필요한 구간을 나누고 설명을 붙인다.

전가산기 해석 예시:

> 30–40 ns 구간에서 a=0, b=1, carry_in=1이다. 세 입력의 합은 2이므로 carry_out=1, sum=0을 예상한다. 파형에서도 같은 값이 확인되어 이 입력 조건의 결과가 진리표와 일치한다.

수업 운영 기준은 OT TeX를 따른다. LAB1~LAB3은 실험 전 보고서에 해당 LAB의 전체 VS Code 시뮬레이션을 담는다. 당일에는 조교가 무작위로 고른 2개를 시연하고 출석부에 기록한다. 실험 후 보고서에는 전체 Vivado 시뮬레이션과 선정된 2개의 시연 사진을 담는다.

## 11. 문제가 생기면

| 증상 | 확인할 것과 조치 |
|---|---|
| `git`·`code`·`gh` 명령을 찾지 못함 | 해당 프로그램 설치와 PATH 확인. VS Code까지 종료한 뒤 재실행. `gh`는 사용 시 확인 |
| `xvlog` 등을 찾지 못함 | Vivado의 실제 `bin` 폴더와 `.bat` 파일 확인. PATH 수정 후 재실행 |
| 이전 Vivado 버전이 실행됨 | `Get-Command … -All`로 경로 순서 확인. `VIVADO_BIN`이 별도로 지정되어 있는지도 확인 |
| 언어 서버 설치 알림이 안 나옴 | 이미 설치되었는지 정의 이동으로 확인. 확장 활성화·프로젝트 신뢰·`.v` 파일 열기 상태 확인 |
| 서버 다운로드 실패 | 네트워크·프록시와 Output 패널의 slang 관련 로그 확인. 실패 메시지를 조교에게 전달 |
| Ctrl+클릭이 작동하지 않음 | 프로젝트 폴더, 언어 모드, 서버 설치, `sources.f` 확인. F12로도 확인 |
| 코드가 일반 텍스트로 보임 | 오른쪽 아래 언어 모드가 `.v`는 Verilog, `.sv`는 SystemVerilog인지 확인 |
| `HDL: Simulate full adder`가 없음 | `.code-workspace` 또는 `example_full_adder_hdl` 폴더 자체를 열었는지 확인 |
| 컴파일 실패 | `compile.txt`의 첫 오류부터 확인. 진단 연습에서 지운 세미콜론도 복원 |
| PASS가 없거나 출력 불일치 | `simulation.txt`의 실패 입력과 예상값·실제값 비교. 코드 수정 후 재실행 |
| VCD가 없거나 파형이 비어 있음 | 먼저 PASS 확인. 올바른 VCD를 열고 Netlist에서 신호 추가 후 Zoom to Fit |

## 12. 설치 완료 확인

- [ ] `git --version`, `code --version`과 실행 경로를 확인했다.
- [ ] GitHub CLI를 사용하는 경우 `gh --version`, `gh auth status`를 확인했다.
- [ ] `xvlog`, `xelab`, `xsim`이 모두 Vivado 2026.1로 실행된다.
- [ ] GitHub에서 받은 전가산기 프로젝트를 올바른 폴더로 열었다.
- [ ] 두 확장을 설치하고, 언어 서버의 정의 이동과 오류 진단을 확인했다.
- [ ] 의도적으로 만든 문법 오류를 복원했다.
- [ ] 8개 입력 검사 PASS와 80 ns 파형을 확인했다.
- [ ] 다섯 신호의 값을 진리표와 비교하고 설명할 수 있다.

<!-- 제작 메모: 학생 배포 시 이 주석은 화면에 표시되지 않는다.
실제 촬영 자료 삽입 순서: ① 확장 ID와 설치 화면 ② Install slang-server 알림(기존 촬영본) ③ Ctrl+클릭 전후 ④ 의도적 문법 오류와 복원 ⑤ 도구 경로·버전 ⑥ 작업 선택과 PASS ⑦ 다섯 신호의 전체 파형.
기존 촬영 파일과 연결할 때 실제 파일을 확인하고 링크한다. 임시 이미지나 존재하지 않는 경로를 넣지 않는다.
-->
