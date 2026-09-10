# macOS ARM64 배포와 WSL 오픈소스 흐름

[전체 프로젝트](../README.md) · [CLI 통합](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/b7c6c1d8c16270797abe140cc0c44c9b1a78c0d2/README.md) · [통합 동작](integrated.md) · [Icarus 교차검사](cli-simulation-results.json)

작성일 2026-09-10. 제작자는 Mac이 없으므로 **공식 macOS ARM64 바이너리 배포를 확인하고 WSL Ubuntu-26.04의 Linux x86-64 바이너리로 실행**합니다. Mac에서 직접 실행·보드 기록을 검증했다는 뜻이 아닙니다.

**정확한 S75에서 오픈소스 합성·배치배선·bit 생성과 파일 체크섬 검사가 통과했습니다.** 아래는 빈 단일 프로젝트에서 학생이 직접 실행하는 순서입니다. 실제 보드 기록·사진·영상은 학생의 실험 후 검증 항목입니다.

## 선택한 도구

| 구성 요소 | 설치 릴리스 | 확인한 버전·역할 |
|---|---|---|
| APIO | 1.5.1 | 도구 패키지 설치 |
| OSS CAD Suite | 2026.08.19 | Icarus Verilog 14.0 개발 버전, Yosys 0.63+173 |
| openXC7 | 2026.08.20 | nextpnr-xilinx 68aeeb3, bbaexport·bbasm·fasm2frames·xc7frames2bit |
| Project X-Ray DB | a3cc0736a90c697b7d4c40319f847a5b6988df62 | PR 15 + 정확한 S75fgga484 핀 표 |

공식 [openXC7 릴리스](https://github.com/FPGAwars/tools-openxc7/releases/tag/2026-08-20)에 `apio-openxc7-darwin-arm64-20260820.tgz`와 `apio-openxc7-linux-x86-64-20260820.tgz`가 있습니다. [OSS CAD Suite 릴리스](https://github.com/FPGAwars/tools-oss-cad-suite/releases/tag/2026-08-19)도 플랫폼별 바이너리를 제공합니다. [APIO](https://github.com/FPGAwars/apio)와 [openXC7 nextpnr](https://github.com/openXC7/nextpnr-xilinx)의 공식 흐름을 사용합니다.

## 설치

Mac에서는 Terminal, Windows에서는 WSL Ubuntu 터미널에서 실행합니다. WSL에서 VS Code를 사용할 때는 WSL 확장으로 Linux 폴더를 열고 확장을 WSL 쪽에 설치합니다. `python3-venv`가 없는 Ubuntu에는 먼저 해당 배포의 패키지 관리자로 설치합니다.

```sh
python3 -m venv ~/.local/share/fpga-apio
~/.local/share/fpga-apio/bin/pip install apio==1.5.1
~/.local/share/fpga-apio/bin/apio packages install
export PATH="$HOME/.apio/packages/openxc7/bin:$HOME/.apio/packages/oss-cad-suite/bin:$PATH"
iverilog -V
yosys -V
nextpnr-xilinx --version
```

APIO의 기본 패키지는 나중에 바뀔 수 있습니다. 이 자료의 실제 실행은 위 표 릴리스입니다. 동일 재현에는 공식 릴리스의 같은 날짜·운영체제·아키텍처 자산을 사용합니다. Linux와 macOS 바이너리를 서로 바꾸어 실행하지 않습니다. 패키지의 `lib`를 전역 `LD_LIBRARY_PATH`로 지정하면 호스트 glibc와 충돌할 수 있으므로 배포된 실행 래퍼를 사용합니다.

## 정확한 S75 chipdb 준비

실습 프로젝트는 앞에서 `fpga-lab-template`의 **v2.0.0**을 새 이름으로 clone한 폴더입니다. RTL 14개·TB·XDC는 PDF를 보고 직접 작성합니다. 아래 별도 폴더에는 도구 데이터만 설치합니다.

upstream DB의 S75가 S50 fabric과 불완전한 190핀 CSV를 사용하던 문제를 해결했습니다. [PR 15](https://github.com/openXC7/prjxray-db/pull/15)의 정확한 S75→S100 fabric 매핑을 커밋 `a3cc0736a90c697b7d4c40319f847a5b6988df62`로 고정하고, 실제 `xc7s75fgga484-1`에서 추출한 338개 I/O 핀을 적용합니다. FPGA 부품명·IDCODE·part.yaml은 S75 그대로입니다. 학생 PC에서는 Vivado를 실행하지 않습니다.

아래 도구 보조 파일은 예시 저장소의 고정 태그에서 받습니다. 회로 정답 코드를 학생 프로젝트에 채우지 않습니다. [준비 스크립트와 핀 표](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/tree/v2.0.1/tools)를 확인할 수 있습니다.

```sh
mkdir -p ~/fpga-cli/lab1-tools
cd ~/fpga-cli/lab1-tools
base=https://raw.githubusercontent.com/Glaysia/fpga-lab-example-opensource-cli-integrated/v2.0.1/tools
curl --fail --location "$base/prepare_s75.py" -o prepare_s75.py
curl --fail --location "$base/xc7s75fgga484-1-package-pins.csv" -o xc7s75fgga484-1-package-pins.csv
python3 prepare_s75.py
```

`~/fpga-cli/lab1-s75/prepared.json`의 part·338핀·커밋·chipdb 해시를 확인합니다. exporter와 bbasm은 메모리와 시간이 필요합니다. 실패하면 같은 폴더의 export.log·bbasm.log를 확인합니다. 이미 다른 DB가 있는 폴더를 덮어쓰지 않도록 준비 도구가 커밋을 검사합니다.

## 학생 프로젝트에서 직접 실행

VS Code의 해당 실습 폴더로 돌아와 Terminal → New Terminal을 엽니다. 아래는 Bash/Zsh/WSL 명령이며 Windows PowerShell용 문법이 아닙니다. 프로젝트 루트에는 simulation.json과 src·sim·constraints가 있어야 합니다.

```sh
python3 tools/lab1.py simulate
export PATH="$HOME/.apio/packages/oss-cad-suite/bin:$HOME/.apio/packages/openxc7/bin:$PATH"
mkdir -p build/cli
```

2,560개 검사 PASS·버튼·LCD 검사를 먼저 확인합니다. Explorer에서 프로젝트 루트 우클릭 → New File → **synth.ys**를 만들고 직접 입력합니다. TB는 합성에 포함하지 않습니다.

```text
read_verilog src/*.v
synth_xilinx -family xc7 -top lab1_integrated
write_json build/cli/design.json
stat
```

터미널에서 순서대로 실행합니다. 각 명령의 종료 코드가 0인지 확인하고 오류가 나면 그 단계에서 로그를 읽습니다. 이전 결과를 새 실행의 결과로 사용하지 않습니다.

```sh
yosys -l build/cli/synthesis.log -s synth.ys
chip="$HOME/fpga-cli/lab1-s75/xc7s75fgga484-1.bin"
db="$HOME/fpga-cli/lab1-s75/prjxray-db/spartan7"
part=xc7s75fgga484-1
nextpnr-xilinx --chipdb "$chip" \
  --xdc constraints/lab1_integrated.xdc \
  --json build/cli/design.json --fasm build/cli/design.fasm \
  --freq 0.001 --log build/cli/place-route.log
fasm2frames --db-root "$db" --part "$part" \
  build/cli/design.fasm build/cli/design.frames
xc7frames2bit --part_file "$db/$part/part.yaml" \
  --part_name "$part" --frm_file build/cli/design.frames \
  --output_file build/cli/lab1_integrated.bit
bitread --part_file "$db/$part/part.yaml" -C -z -y \
  -o build/cli/bits.txt build/cli/lab1_integrated.bit
```

`--freq 0.001`은 수업 보드의 1kHz 클록을 MHz로 표현한 값입니다. XDC의 B6·1,000,000ns와 일치합니다. bitread는 생성한 파일을 다시 읽고 프레임 체크섬을 확인합니다. 정확한 S75의 구성 프레임은 9,104개입니다. 파일 생성·체크섬 검사는 실제 보드 동작 검사를 대신하지 않습니다.

## 확인한 결과와 근거

2026-09-10 WSL Linux x86-64에서 현재 단일 프로젝트의 소스로 Yosys·nextpnr·fasm2frames·xc7frames2bit가 모두 종료 코드 0으로 완료됐습니다. 생성 bit는 3,686,916바이트이고, bitread의 체크섬 검사와 9,104프레임 읽기가 통과했습니다. [실행 기록](cli-pr15-evidence/validation.json), [비트스트림 읽기](cli-pr15-evidence/bitread.txt), [DB 보정의 출처](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/v2.0.1/evidence/openxc7/database-provenance.json)를 확인합니다. 이 수치는 기록한 실행 결과이며 소스·도구·배치 결과에 따라 bit 해시가 달라질 수 있습니다.

기존 DB에서 K4/B6가 빠져 실패했던 [이전 실행](cli-direct-evidence/validation.json)은 원인 비교를 위해 보존합니다. 현재 성공 절차에 예전 S50 chipdb를 섞지 않습니다. upstream PR의 검증 범위와 실제 보드 미검증 상태도 구분합니다.

## openFPGALoader 설치와 보드 기록

macOS:

```sh
brew install openfpgaloader
```

Windows MSYS2 UCRT64:

```sh
pacman -S mingw-w64-ucrt-x86_64-openFPGALoader
```

Linux는 해당 배포 패키지 또는 [공식 설치 안내](https://trabucayre.github.io/openFPGALoader/guide/install.html)를 따릅니다. 도구를 실행하는 OS에 USB JTAG 장치가 연결되어야 합니다. WSL·VM은 USB 전달 여부도 확인합니다.

```sh
openFPGALoader --help
openFPGALoader --list-cables
openFPGALoader --list-boards
```

보드 전원과 USB JTAG 케이블을 연결하고 실제 케이블 식별자를 확인합니다. 아래 MY_CABLE을 그 값으로 바꿉니다. 보드가 목록에 없다고 다른 FPGA 보드의 이름을 임의로 고르지 않습니다.

```sh
openFPGALoader -c MY_CABLE build/cli/lab1_integrated.bit
```

기본 명령은 SRAM 기록입니다. Flash에 쓰는 `-f`는 이 실습 명령에 넣지 않습니다. 자신의 새 bit 경로·생성 시각·해시를 확인하고, 터미널의 장치 인식·기록·종료 로그를 보관합니다. 장치가 없으면 실제 프로그래밍 성공으로 기록하지 않습니다.

## 실험 후 레포트

KEY1 reset, KEY2의 짧은 누름·긴 누름, 10→01 순환과 LCD 두 줄의 모드 번호·회로 이름을 확인합니다. 모드마다 DIP를 바꿔 LED·7세그먼트 출력을 예상값과 비교합니다. 도구 버전·명령·RTL/TB/XDC 커밋·DB/bit 해시·각 단계 로그·보드 전체 사진·10모드 영상을 GitHub에 연결합니다. VS Code의 실험 전 결과와 CLI 구현 결과·실측 결과를 비교해 차이를 설명합니다.
