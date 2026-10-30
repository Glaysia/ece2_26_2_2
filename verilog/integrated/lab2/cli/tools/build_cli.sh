#!/usr/bin/env bash
# Run from this project root after writing and simulating the RTL.
set -euo pipefail
export PATH="$HOME/.apio/packages/oss-cad-suite/bin:$HOME/.apio/packages/openxc7/bin:$PATH"
chip="$HOME/fpga-cli/lab1-s75/xc7s75fgga484-1.bin"
db="$HOME/fpga-cli/lab1-s75/prjxray-db/spartan7"
part=xc7s75fgga484-1
test -f "$chip"
test -f "$db/$part/part.yaml"
test -f simulation.json
test -f constraints/lab2_integrated.xdc
mkdir -p build/cli
python3 - <<'PY'
from pathlib import Path
import hashlib, json
config=json.loads(Path('simulation.json').read_text())
files=config['sources']+[config['testbench'],'constraints/lab2_integrated.xdc','synth.ys','tools/build_cli.sh']
hashes={name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in files}
Path('build/cli/inputs.json').write_text(json.dumps(hashes,indent=2)+'\n')
PY
python3 tools/lab1.py simulate
yosys -l build/cli/synthesis.log -s synth.ys
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
sha256sum build/cli/lab2_integrated.bit
