"""Record the completed CLI build and verify its S75 IDCODE and pin mapping."""
from pathlib import Path
import csv
import hashlib
import json
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'
PROJECT=LAB/'opensource_cli/09_integrated'

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    log=(ROOT/'tmp/lab2-cli-build.log').read_text(encoding='utf-8')
    bit=PROJECT/'build/cli/lab2_integrated.bit'
    data=bit.read_bytes()
    # Configuration register 12, one-word write, exact xc7s75 IDCODE.
    marker=bytes.fromhex('30018001037c8093')
    assert marker in data and bytes.fromhex('aa995566') in data
    assert 'Number of configuration frames: 9104' in log and '\nDONE\n' in log
    assert digest(bit)+'  build/cli/lab2_integrated.bit' in log
    assert 'LAB2_INTEGRATED_PASS modes=8' in log
    for required in ['synthesis.log','place-route.log','design.frames','bits.txt']:
        assert (PROJECT/'build/cli'/required).stat().st_size>0
    route=(PROJECT/'build/cli/place-route.log').read_text(encoding='utf-8')
    assert 'ERROR:' not in route
    prepared=subprocess.run(['wsl.exe','-d','Ubuntu-26.04','-u','uos','--','bash','-lc',
                             'cat ~/fpga-cli/lab1-s75/prepared.json'],capture_output=True,text=True,check=True)
    db=json.loads(prepared.stdout)
    assert db['part']=='xc7s75fgga484-1' and db['package_pins']==338
    assert db['database_commit']=='a3cc0736a90c697b7d4c40319f847a5b6988df62'
    helper=ROOT/'example/fpga_projects_hdl/LAB1/opensource_cli/integrated/tools'
    for name in ['prepare_s75.py','xc7s75fgga484-1-package-pins.csv']:
        shutil.copyfile(helper/name,PROJECT/'tools'/name)
    csvfile=PROJECT/'tools/xc7s75fgga484-1-package-pins.csv'
    assert digest(csvfile)==db['package_pins_sha256']
    pins={row['pin'] for row in csv.DictReader(csvfile.open(encoding='utf-8'))}
    mapping=json.loads((PROJECT/'evidence/board-pin-provenance.json').read_text(encoding='utf-8'))['pins']
    assert len(mapping)==47 and set(mapping.values())<=pins
    inputs=[PROJECT/p for p in json.loads((PROJECT/'simulation.json').read_text(encoding='utf-8'))['sources']]
    inputs += [PROJECT/'sim/tb_lab2_integrated.sv',PROJECT/'constraints/lab2_integrated.xdc',PROJECT/'synth.ys',PROJECT/'tools/build_cli.sh']
    input_hashes={p.relative_to(PROJECT).as_posix():digest(p) for p in inputs}
    assert input_hashes==json.loads((PROJECT/'build/cli/inputs.json').read_text(encoding='utf-8')), 'sources differ from build-start snapshot'
    record={'status':'PASS','part':'xc7s75fgga484-1','idcode':'0x037c8093','platform':'WSL Ubuntu-26.04 Linux x86-64',
            'flow':'Icarus -> Yosys -> nextpnr-xilinx -> fasm2frames -> xc7frames2bit -> bitread',
            'yosys':'0.63+173 (66306a8ca)','nextpnr':'68aeeb3','configuration_frames':9104,
            'bitread_frame_checksum_check':True,'database':db,
            'bitstream':{'file':bit.name,'bytes':len(data),'sha256':digest(bit)},
            'input_sha256':input_hashes,
            'package_pin_coverage':{'mapped':len(mapping),'all_in_338_pin_table':True},
            'constraint_note':'nextpnr ignores set_false_path; that asynchronous-input timing exception applies only to Vivado. This build does not certify CDC or board timing.',
            'physical_board_tested':False,'macos_execution_tested':False,'vivado_used_for_this_bitstream':False}
    evidence=PROJECT/'evidence/openxc7'; evidence.mkdir(exist_ok=True)
    for name in ['synthesis.log','place-route.log']:
        shutil.copyfile(PROJECT/'build/cli'/name,evidence/name)
    (evidence/'bitread.txt').write_text(log[log.index('Bitstream size:'):],encoding='utf-8')
    (evidence/'validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (LAB/'docs/cli-validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(record['status'],record['bitstream'])

if __name__=='__main__': main()
