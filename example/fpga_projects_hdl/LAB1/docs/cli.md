# macOS ARM64 배포와 WSL 오픈소스 흐름

[전체 프로젝트](../README.md) · [CLI 통합](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/2c1e00f7ca38de27f1b933e836de210fb7682ca0/README.md) · [통합 동작](integrated.md) · [실행 스크립트](../tools/openxc7_build.py) · [Icarus 교차검사](cli-simulation-results.json)

작성일 2026-09-10. 제작자는 Mac이 없으므로 **공식 macOS ARM64 바이너리 배포를 확인하고 WSL Ubuntu-26.04의 Linux x86-64 바이너리로 실행**합니다. Mac에서 직접 실행·보드 기록을 검증했다는 뜻이 아닙니다.

**현재 검증한 릴리스는 시뮬레이션·Yosys 합성까지 성공하고 S75 배치배선에서 실패합니다. CLI bit는 생성하지 못했습니다.** 아래 bit 단계는 실행 스크립트와 실패 재현 안내이며, 완성된 S75 빌드 배포로 취급하지 않습니다.

## 선택한 도구

| 구성 요소 | 설치 릴리스 | 확인한 버전·역할 |
|---|---|---|
| APIO | 1.5.1 | 도구 패키지 설치 |
| OSS CAD Suite | 2026.08.19 | Icarus Verilog 14.0 개발 버전, Yosys 0.63+173 |
| openXC7 | 2026.08.20 | nextpnr-xilinx 68aeeb3, bbaexport·bbasm·fasm2frames·xc7frames2bit |
| Project X-Ray DB | e8b8e8e46a91334f6232df84d36954323e15a1d1 | spartan7의 xc7s75fgga484-1 |

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

APIO openXC7 패키지에 포함된 S50 chipdb는 수업의 S75와 다릅니다. S75의 Project X-Ray 데이터베이스는 [공식 저장소](https://github.com/openXC7/prjxray-db)에 있습니다. Linux 제작 환경에서 다음 명령으로 같은 부품을 내보냅니다.

```sh
mkdir -p ~/fpga-cli
cd ~/fpga-cli
git clone --depth 1 --filter=blob:none --sparse https://github.com/openXC7/prjxray-db.git
git -C prjxray-db sparse-checkout set spartan7
git -C prjxray-db rev-parse HEAD
python3 ~/.apio/packages/openxc7/share/nextpnr/python/bbaexport.py \
  --xray "$HOME/fpga-cli/prjxray-db/spartan7" \
  --device xc7s75fgga484-1 \
  --bba "$HOME/fpga-cli/xc7s75fgga484-1.bba"
bbasm --l ~/fpga-cli/xc7s75fgga484-1.bba ~/fpga-cli/xc7s75fgga484-1.bin
```

데이터베이스 커밋이 위 표와 다르면 결과도 별도 실행으로 기록합니다.

## VS Code 사전 시뮬레이션

`git clone https://github.com/Glaysia/fpga-lab-template.git lab1_integrated_cli`로 빈 프로젝트를 만듭니다. 새 창에서 그 폴더의 `LAB1.code-workspace`를 엽니다. [공통 작성 순서](student-workflow.md)에 따라 RTL은 `src`, TB는 `sim`, XDC는 `constraints`에 직접 작성하고 `simulation.json`에 RTL 목록·TB·TB top을 등록합니다. Terminal → Run Task...에서 01 Check tools → 02 Simulate → 03 Open waveform을 수행합니다. 모든 새 템플릿은 Icarus를 사용합니다.

같은 명령을 터미널에서 실행하려면 프로젝트 폴더에서 다음을 사용합니다.

```sh
python3 tools/lab1.py simulate
```

제작 WSL에서 통합 2,560개, 버튼·LCD·reset 검사가 통과했고 72430ns에 종료했습니다. 개별 최신 10개·레거시 10개도 Icarus로 교차검사하여 모두 통과했습니다. 원본 감산기의 잘못된 borrow는 자기검사에서 의도대로 실패하고 수정본은 256개를 통과했습니다.

## 합성부터 bit까지

아래는 기존 강사용 프로젝트에서 실행한 이력 명령입니다. 빈 v2.0.0 템플릿에 `openxc7_build.py`가 들어 있다는 뜻이 아닙니다. 새 학생용 교안의 직접 실행 명령과 S75 DB 해결 작업은 개편 중입니다. 기존 스크립트는 새 실행 디렉터리를 만들고 앞 단계가 실패하면 멈추며 오래된 bit를 결과로 사용하지 않습니다.

```sh
python3 ../../tools/openxc7_build.py --project .
```

내부 순서는 Yosys `synth_xilinx -family xc7` → nextpnr-xilinx `--chipdb`·`--xdc`·`--json`·`--fasm` → fasm2frames `--db-root`·`--part` → xc7frames2bit `--part_file`·`--part_name`입니다. 전체 실제 명령과 종료 코드는 `build/cli/result.json`, 단계별 로그는 그 파일의 `run` 디렉터리에 기록됩니다. 성공한 최종 파일은 `build/cli/lab1_integrated.bit`입니다.

다른 설치 경로를 사용하면 `OSS_CAD_ROOT`, `OPENXC7_ROOT`, `XRAY_DB_ROOT`, `OPENXC7_CHIPDB`를 지정합니다. XDC와 RTL은 Vivado 통합본과 같습니다. 합성 성공과 최종 bit 생성 성공을 구분하며 마지막 단계가 PASS인 실행만 배포합니다.

## 실제 실행 현황

| 대상 | Icarus | Yosys 합성 | nextpnr 배치배선 | 프레임·bit |
|---|---|---|---|---|
| 논리 게이트 지원 확인 | 4개 통과 | 성공 | K4 핀 없음으로 실패 | 미실행 |
| 통합 10모드 | 2,560개 통과 | 성공 | B6 핀 없음으로 실패 | 미실행 |

`bbaexport.py`와 `bbasm`은 실행을 마쳤지만, 생성한 chipdb로 배치배선할 때 `device does not have a pin named 'K4'` 또는 `'B6'` 오류가 납니다. [데이터베이스 대조 결과](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/2c1e00f7ca38de27f1b933e836de210fb7682ca0/evidence/historical-course/s75-database-audit.json)에 필수 핀 38개 중 누락 28개와 파일 해시를 기록했습니다.

해당 커밋의 `xc7s75/tilegrid.json`은 `xc7s50/tilegrid.json`과 바이트 단위로 같습니다. 두 SHA-256은 `478cd2342474f7114c138109ae836d2cd4a6fe5bafb487fafdb04afe3de05623`입니다. S75 패키지 CSV에는 핀 190개만 있고 필요한 K4·B6가 없습니다. 같은 부품의 Vivado 공식 데이터에서 K4는 bank 35의 `IOB_X1Y129`, B6는 bank 36의 `IOB_X1Y174`로 확인했습니다. 단순한 XDC 철자 문제로 처리할 수 없습니다.

이 파일의 [추가 커밋](https://github.com/openXC7/prjxray-db/commit/e107361263e9a3f1340ce54bc1c3e625da438c5b)은 S75 자료를 APIO 패키지에서 가져왔다고 설명합니다. 현재 검증한 데이터의 부족을 다른 부품 핀으로 바꾸어 우회하지 않았습니다. 실패 실행의 [결과](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/2c1e00f7ca38de27f1b933e836de210fb7682ca0/evidence/historical-course/cli-result.json), [합성 로그](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/2c1e00f7ca38de27f1b933e836de210fb7682ca0/evidence/historical-course/cli-synthesis.txt), [배치배선 로그](https://github.com/Glaysia/fpga-lab-example-opensource-cli-integrated/blob/2c1e00f7ca38de27f1b933e836de210fb7682ca0/evidence/historical-course/cli-place-route.txt)를 보관합니다.

대안으로 [F4PGA 기본 플랫폼](https://f4pga.readthedocs.io/en/latest/f4pga/Usage.html)을 확인했지만 공개 안내의 기본 구성은 Artix-7 계열이며 이 S75 보드의 대체 완성 흐름을 확인하지 못했습니다. 새 대상 지원에는 [Project X-Ray의 부품 추가 절차](https://f4pga.readthedocs.io/projects/prjxray/en/latest/db_dev_process/newpart.html)에 따라 실제 S75의 tilegrid·tileconn·패키지 핀·프레임 주소를 생성·검증하는 작업이 필요합니다. 도구 전체가 어떤 환경에서도 지원하지 않는다고 단정하는 것은 아니며, 여기서 선택·실행한 릴리스의 한계입니다.

따라서 CLI 통합 bit 목표는 **미완료**입니다. 정확한 S75 DB·도구 문제를 해결하여 오픈소스 경로로 bit를 생성하는 작업이 남아 있습니다. CLI 실습의 완료 조건을 Vivado 생성 bit로 대체하지 않습니다. 실제 보드 기록·사진·영상도 미수행이며 실제 결과를 얻은 뒤 실험 후 레포트에 추가합니다.

## openFPGALoader로 기록하기

bit가 생성되면 기록 도구는 **openFPGALoader**를 사용합니다. [공식 첫 실행 안내](https://trabucayre.github.io/openFPGALoader/guide/first-steps.html)에 따라 macOS는 `brew install openfpgaloader`, Windows MSYS2 UCRT64는 `pacman -S mingw-w64-ucrt-x86_64-openFPGALoader`로 설치합니다. Linux는 해당 배포판 패키지 또는 공식 설치 절차를 사용합니다.

1. `openFPGALoader --help`로 실행 파일과 옵션을 확인합니다.
2. 보드 전원과 USB JTAG를 연결합니다. VM/WSL은 도구가 실행되는 환경에 USB가 전달되어야 합니다.
3. `openFPGALoader --list-cables`와 `openFPGALoader --list-boards`로 실제 케이블·보드에 해당하는 식별자를 확인합니다. 보드가 없다고 임의의 다른 보드를 지정하지 않습니다.
4. 다음 명령의 `MY_CABLE`을 실제 확인한 케이블 식별자로 바꾸고 자신이 생성한 bit를 SRAM에 기록합니다.

```sh
openFPGALoader -c MY_CABLE build/cli/lab1_integrated.bit
```

기본 기록은 SRAM이며 전원을 끄면 사라집니다. Flash 기록은 별도 `-f` 옵션으로 수행하는 작업입니다. 이 실습의 SRAM 명령에는 넣지 않습니다. 실제 케이블·장치·기록 결과가 아직 확인되지 않았으므로 위 명령 예를 성공 로그로 취급하지 않습니다.

`evidence/cli`에는 합성·배치배선·bit 생성 근거, `evidence/programming`에는 장치·케이블·기록 로그를 보관합니다. 기록한 bit 해시와 소스 커밋을 연결하고 10개 모드·버튼·LCD 동작 사진과 영상을 `reports/post`에서 링크합니다. 실험 후 레포트는 CLI 도구 버전·DB·명령·bit·실측을 설명하며 XSim이나 Hardware Manager 실행을 요구하지 않습니다.
