# macOS ARM64 배포와 WSL 오픈소스 흐름

[전체 프로젝트](../README.md) · [CLI 통합](../opensource_cli/integrated/README.md) · [통합 동작](integrated.md) · [실행 스크립트](../tools/openxc7_build.py) · [Icarus 교차검사](cli-simulation-results.json)

작성일 2026-09-10. 제작자는 Mac이 없으므로 **공식 macOS ARM64 바이너리 배포를 확인하고 WSL Ubuntu-26.04의 Linux x86-64 바이너리로 실행**합니다. Mac에서 직접 실행·보드 기록을 검증했다는 뜻이 아닙니다.

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

템플릿을 clone한 뒤 `opensource_cli/integrated/opensource_cli_integrated.code-workspace`를 새 창으로 엽니다. Terminal → Run Task...에서 01 Check tools → 02 Simulate → 03 Open waveform을 수행합니다. CLI workspace에는 `--simulator iverilog`가 지정되어 있습니다.

같은 명령을 터미널에서 실행하려면 프로젝트 폴더에서 다음을 사용합니다.

```sh
python3 ../../tools/lab1.py simulate --project . --simulator iverilog
```

제작 WSL에서 통합 2,560개, 버튼·LCD·reset 검사가 통과했고 72430ns에 종료했습니다. 개별 최신 10개·레거시 10개도 Icarus로 교차검사하여 모두 통과했습니다. 원본 감산기의 잘못된 borrow는 자기검사에서 의도대로 실패하고 수정본은 256개를 통과했습니다.

## 합성부터 bit까지

프로젝트 폴더에서 실행합니다. 스크립트는 새 실행 디렉터리를 만들고 앞 단계가 실패하면 멈추며 오래된 bit를 결과로 사용하지 않습니다.

```sh
python3 ../../tools/openxc7_build.py --project .
```

내부 순서는 Yosys `synth_xilinx -family xc7` → nextpnr-xilinx `--chipdb`·`--xdc`·`--json`·`--fasm` → fasm2frames `--db-root`·`--part` → xc7frames2bit `--part_file`·`--part_name`입니다. 전체 실제 명령과 종료 코드는 `build/cli/result.json`, 단계별 로그는 그 파일의 `run` 디렉터리에 기록됩니다. 성공한 최종 파일은 `build/cli/lab1_integrated.bit`입니다.

다른 설치 경로를 사용하면 `OSS_CAD_ROOT`, `OPENXC7_ROOT`, `XRAY_DB_ROOT`, `OPENXC7_CHIPDB`를 지정합니다. XDC와 RTL은 Vivado 통합본과 같습니다. 합성 성공과 최종 bit 생성 성공을 구분하며 마지막 단계가 PASS인 실행만 배포합니다.

## 실제 실행 현황

Icarus 시뮬레이션은 통과했습니다. 정확한 S75 chipdb 생성과 bit 흐름의 최종 결과는 검증 완료 후 이 절에 기록합니다. 현재 이 문장만으로 bit 생성 성공을 주장하지 않습니다. 실제 보드 기록·사진·영상은 미수행이며 실험실 Vivado 환경에서 수행한 뒤 실험 후 레포트에 추가합니다.
