# LAB1 · VS Code 전가산기 예제

전자전기컴퓨터설계실험Ⅱ의 VS Code 환경설정 매뉴얼용 프로젝트다. **코드 진단 → 정의로 이동 → 시뮬레이션 → 파형 확인**을 하나의 작은 예제로 연습한다.

배포 태그: `lab1-full-adder-v1.0.0` · 대상 환경: Windows, VS Code, Vivado 2026.1.

## 1. 프로젝트 열기

이 폴더의 `example_full_adder_hdl.code-workspace`를 VS Code에서 연다. 또는 **파일 → 폴더 열기**로 `example_full_adder_hdl` 폴더 자체를 연다. 상위 `fpga_projects_hdl` 폴더를 열면 이 프로젝트의 `.vscode/tasks.json`이 적용되지 않는다.

저장소 루트에서 명령으로 열 때:

```powershell
code fpga_projects_hdl/example_full_adder_hdl/example_full_adder_hdl.code-workspace
```

GitHub에 업로드한 뒤에는 실제 저장소 주소로 clone하고 `git checkout lab1-full-adder-v1.0.0`으로 매뉴얼과 같은 버전을 연다. 태그 상태에서 직접 수정·커밋하려면 먼저 `git switch -c my-lab1`로 작업 브랜치를 만든다.

## 2. VS Code 확장과 언어 서버

`Ctrl+Shift+X`로 확장 화면을 열고 다음 ID를 검색하여 설치한다.

| 확장 ID | 역할 |
|---|---|
| `Hudson-River-Trading.vscode-slang` | Verilog/SystemVerilog 진단, 심벌 정보, 정의로 이동 |
| `lramseyer.vaporview` | 시뮬레이터가 만든 VCD 파형 표시 |

`src/full_adder.v`를 열고 언어 서버 설치 알림이 나오면 **Install slang-server**를 선택한다. 확장이 서버 바이너리를 다운로드한다. 이미 설치된 PC에는 안내가 나타나지 않을 수 있다. 자동 설치 방식에서는 `slang.path`를 직접 지정하거나 서버 바이너리를 PATH에 추가할 필요가 없다.

언어 서버는 코드 편집을 지원하고, 실제 시간에 따른 시뮬레이션은 Vivado XSim이 수행한다. 두 확장만 설치한 상태로 시뮬레이션 도구가 준비되었다고 판단하지 않는다.

설정 파일 `.slang/server.json`과 `sources.f`에 이 프로젝트의 세 소스를 등록했다. 다른 실험·주차의 모듈을 함께 불러오지 않는다.

## 3. 도구 경로와 버전 확인

Vivado 설치 매뉴얼에 따라 **자신의 Vivado 설치 폴더 아래 `bin` 디렉터리**를 사용자 PATH에 추가한다. 설치 경로를 다른 사람의 PC 경로로 그대로 복사하지 않는다. PATH 변경 후 VS Code를 완전히 종료하고 다시 실행한다.

새 PowerShell 터미널에서 실행한다.

```powershell
git --version
code --version
Get-Command xvlog.bat, xelab.bat, xsim.bat
xvlog -version
xelab -version
xsim -version
```

Git과 VS Code는 `--version`, Vivado 시뮬레이션 도구는 **`-version`**을 사용한다. Vivado 도구 세 개가 2026.1로 표시되는지 확인한다. `code`가 인식되지 않으면 VS Code 설치의 PATH 옵션을 확인하거나 GUI로 작업 영역을 연다.

`Ctrl+Shift+P` → **Tasks: Run Task** → **HDL: Check tools**로도 Vivado 도구 세 개를 확인할 수 있다. 명령이 인식되지 않으면 시뮬레이션 전에 경로 문제부터 해결한다.

PATH를 사용하지 않는 개별 실행은 다음과 같이 가능하다. `-VivadoBin`에는 본인의 설치 경로를 넣는다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/check-tools.ps1 -VivadoBin 'C:\AMDDesignTools\2026.1\Vivado\bin'
```

이 명령의 실행 정책 옵션은 해당 PowerShell 프로세스에만 적용되며 시스템의 영구 설정을 변경하지 않는다. 스크립트는 선택적으로 `VIVADO_BIN` 환경변수도 읽는다. 일반 실습에서는 사용자 PATH 설정을 사용한다.

## 4. 언어 서버 동작 확인

1. `src/full_adder.v`에서 `half_adder` 모듈 이름 위에 마우스를 올려 심벌 설명을 확인한다.
2. `Ctrl`을 누른 채 모듈 이름을 클릭하거나 `F12`를 눌러 `src/half_adder.v`의 정의로 이동한다.
3. 진단 확인용으로 `assign carry_out = ...;`의 마지막 세미콜론을 잠시 지우고 **Problems**(`Ctrl+Shift+M`) 또는 오류 밑줄을 확인한다.
4. `Ctrl+Z`로 복원하고 저장한다. 오류가 해소된 다음 시뮬레이션한다.

색상은 선택한 테마에 따라 다르다. 색상만 바뀐 것을 설치 완료 기준으로 삼지 않고, **정의로 이동과 오류 진단**까지 확인한다. 기능이 나타나지 않으면 서버 설치 완료 여부, 오른쪽 아래 언어 모드, 열린 프로젝트 폴더를 확인한다.

## 5. 회로와 예상 결과

`half_adder.v`는 XOR로 합, AND로 자리올림을 만든다. `full_adder.v`는 반가산기 두 개와 OR 연산을 연결한다.

```text
입력: a, b, carry_in
출력: sum, carry_out
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

조합회로라서 설계에 클록이 없다. 테스트벤치는 입력 000부터 111까지 각각 10 ns 동안 유지하고, 입력 변경 1 ns 후 출력과 예상값을 비교한다. 총 실행 시간은 80 ns다. 이 대기 시간은 RTL 시뮬레이션의 검사 시점이며 실제 회로의 전파 지연을 측정한 값이 아니다.

## 6. 시뮬레이션과 파형

1. 소스를 모두 저장한다.
2. `Ctrl+Shift+B` → **HDL: Simulate full adder**를 실행한다.
3. 터미널에서 `PASS: all 8 full-adder input combinations`를 확인한다.
4. 탐색기에서 `build/full_adder.vcd`를 연다. 텍스트로 열리면 파일을 우클릭하여 **Open With… → VaporView**를 선택한다.
5. Netlist에서 `tb_full_adder`의 `a`, `b`, `carry_in`, `sum`, `carry_out`을 파형에 추가한다.
6. **Zoom to Fit**으로 전체 구간을 보고 진리표와 비교한다. 0–10 ns는 000, 10–20 ns는 001, 마지막 70–80 ns는 111 입력이다.

파형의 표시 단위가 ps라면 10,000 ps가 10 ns다. 코드를 수정한 뒤에는 다시 시뮬레이션하고 새 파형을 다시 열거나 reload한다.

`build/run-…/`에 컴파일·elaboration·실행 로그가 남는다. 매 실행은 새 폴더를 사용하고, 성공한 경우에만 `build/full_adder.vcd`를 갱신한다. 실패 시 이전 실행의 VCD를 새 결과로 오해하지 않도록 대표 VCD는 먼저 제거한다.

터미널에서 직접 실행할 때:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/simulate.ps1
```

## 7. 폴더 구성과 완료 기준

```text
example_full_adder_hdl/
├─ example_full_adder_hdl.code-workspace
├─ .vscode/                  권장 확장·편집 설정·실행 작업
├─ .slang/server.json        언어 서버 프로젝트 설정
├─ sources.f                HDL 소스 목록
├─ src/half_adder.v          반가산기
├─ src/full_adder.v          전가산기
├─ sim/tb_full_adder.sv      8개 입력 자동 검사
├─ scripts/                 도구 확인·시뮬레이션 실행
└─ build/                   생성 결과, Git 제외
```

- 언어 서버가 심벌 설명·정의로 이동·오류 진단을 제공한다.
- Vivado 시뮬레이션 도구 세 개가 실행된다.
- 테스트벤치의 8개 검사가 통과하고 80 ns 파형이 생성된다.
- 생성된 파형에서 입력·출력을 진리표와 대조할 수 있다.

이 배포본은 VS Code와 RTL 시뮬레이션을 위한 예제다. 특정 보드의 XDC·비트스트림·보드 동작 검증은 포함하지 않는다. `slang-server` 실행 파일, Vivado 바이너리와 생성 파형은 저장소에 포함하지 않는다.

## 배포 전 확인 기록

2026-09-07, Windows PowerShell과 Vivado XSim 2026.1에서 실행했다.

- `xvlog`, `xelab`, `xsim`의 버전 확인과 컴파일·실행 성공.
- 8개 입력 조합의 자동 검사 통과, 80 ns에 정상 종료.
- 생성된 VCD의 입력·출력값을 별도로 읽어 진리표와 일치함을 확인.
- 임시 복사본에 잘못된 회로를 넣었을 때 실행 실패를 반환하고 이전 대표 VCD가 제거됨을 확인.

위 기록은 명령줄 실행 검증이다. VS Code의 자동 설치 알림·정의 이동·파형 뷰어 화면은 매뉴얼 촬영 시 별도로 확인한다.

## 참고

- [slang-server 공식 설치 안내](https://hudson-trading.github.io/slang-server/start/installing/)
- [slang-server 프로젝트 설정](https://hudson-trading.github.io/slang-server/start/config/)
- [VaporView 확장](https://marketplace.visualstudio.com/items?itemName=lramseyer.vaporview)

회로 소스의 출발점은 수업 저장소의 `legacy_all_hdl/src/combinational` 예제이며, 이 배포본에서는 전가산기에 필요한 두 모듈만 사용한다.
