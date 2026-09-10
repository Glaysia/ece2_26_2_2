# LAB2 오픈소스 CLI 구현

Vivado 없이 S75용 bit를 생성하는 흐름이다. 학생은 빈 템플릿 v2.0.0을 새 이름으로 clone한 뒤 RTL·TB·XDC를 직접 작성한다. 제작자는 WSL Ubuntu-26.04 Linux x86-64에서 실행했다. macOS ARM64에서 실행하거나 실제 장치에 기록했다는 의미는 아니다.

사용 도구: APIO 1.5.1, OSS CAD Suite 2026.08.19의 Yosys 0.63+173, openXC7 2026.08.20의 nextpnr-xilinx 68aeeb3. 설치·고정 릴리스 링크는 [기존 CLI 설치 안내](../../LAB1/docs/cli.md)를 참고한다. 공통 S75 DB 준비 도구는 동일하며 학습용 회로를 채우지 않는다.

```sh
export PATH="$HOME/.apio/packages/oss-cad-suite/bin:$PATH"
export PATH="$HOME/.apio/packages/openxc7/bin:$PATH"
python3 tools/prepare_s75.py
python3 tools/lab1.py simulate
mkdir -p build/cli
```

`prepare_s75.py`와 `xc7s75fgga484-1-package-pins.csv`는 예시의 tools 아래에 제공한다. 학생의 빈 템플릿에는 없으므로 PDF의 고정 태그 다운로드 절차로 두 파일만 받는다. 준비 결과는 `~/fpga-cli/lab1-s75/prepared.json`이며 LAB1과 공유하는 장비 데이터 이름이다.

`synth.ys`를 직접 작성한다.

```text
read_verilog src/*.v
synth_xilinx -family xc7 -top lab2_integrated
write_json build/cli/design.json
stat
```

프로젝트 루트 터미널에서 순서대로 실행한다. 각 명령이 실패하면 다음 단계로 가지 않는다.

```sh
yosys -l build/cli/synthesis.log -s synth.ys
chip="$HOME/fpga-cli/lab1-s75/xc7s75fgga484-1.bin"
db="$HOME/fpga-cli/lab1-s75/prjxray-db/spartan7"
part=xc7s75fgga484-1
nextpnr-xilinx --chipdb "$chip" \
  --xdc constraints/lab2_integrated.xdc \
  --json build/cli/design.json --fasm build/cli/design.fasm \
  --freq 0.001 --log build/cli/place-route.log
fasm2frames --db-root "$db" --part "$part" \
  build/cli/design.fasm build/cli/design.frames
xc7frames2bit --part_file "$db/$part/part.yaml" \
  --part_name "$part" --frm_file build/cli/design.frames \
  --output_file build/cli/lab2_integrated.bit
bitread --part_file "$db/$part/part.yaml" -C -z -y \
  -o build/cli/bits.txt build/cli/lab2_integrated.bit
```

`--freq 0.001` MHz는 장비의 1 kHz와 XDC의 1,000,000 ns에 대응한다. nextpnr는 `set_false_path`를 지원하지 않아 무시한다는 메시지를 낸다. 이 예외는 Vivado의 비동기 입력 분석에 적용되는 것이며 CLI 결과를 완전한 CDC·실제 장비 타이밍 검증으로 해석하지 않는다.

[실제 실행 기록](cli-validation.json)은 정확한 `xc7s75fgga484-1`, IDCODE `0x037c8093`, 3,686,926바이트의 bit와 9,104개 프레임 읽기 통과를 기록한다. 입력 소스·도구 데이터·bit 해시를 함께 보관했다.

openFPGALoader 설치 후 다음 순서로 실제 USB JTAG 장치를 확인한다. macOS는 `brew install openfpgaloader`, Linux는 배포 패키지 또는 [공식 설치 안내](https://trabucayre.github.io/openFPGALoader/guide/install.html)를 따른다. WSL에는 USB 장치 전달이 필요하다.

```sh
openFPGALoader --list-cables
openFPGALoader --detect
openFPGALoader -c MY_CABLE build/cli/lab2_integrated.bit
```

`MY_CABLE`을 실제 케이블 식별자로 바꾼다. 위 명령은 SRAM에 기록하며 Flash 옵션 `-f`를 쓰지 않는다. 기록 로그, K4 초기화, N8 모드 전환, N4 회로 실행과 LCD·LED·배열 출력을 사진·영상으로 남긴다. 연결 장치가 없으면 기록 성공으로 쓰지 않는다.
