"""Create matching Vivado and CLI LAB2 integration examples from verified cores."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'
REFERENCE=ROOT/'example/fpga_projects_hdl/LAB1/vivado_2026_1/11_integrated'

def main():
    # Keep the established 1 kHz LCD timing; only the title table changes.
    lcd=(REFERENCE/'src/lcd_modes.v').read_text(encoding='utf-8')
    lcd=lcd.replace('module lcd_modes','module lcd_lab2_modes')
    start=lcd.index('  case(shown_mode)'); end=lcd.index('  endcase',start)
    names=['UP DOWN COUNTER ','CLOCK DIVIDER   ','REGISTER PAIR   ','SHIFT REGISTER  ',
           'PISO            ','MOORE FSM       ','MEALY FSM       ','8 DIGIT SCAN    ']
    assert all(len(s)==16 for s in names)
    table='  case(shown_mode)\n'+''.join(f'   {i}:name="{name}";\n' for i,name in enumerate(names))+'   default:name="RESET REQUIRED  ";\n'
    lcd=lcd[:start]+table+lcd[end:]
    lcd=lcd.replace('(shown_mode==9)?"1":"0"','"0"').replace('(shown_mode==9)?"0":("1"+shown_mode)','("1"+shown_mode)')
    (LAB/'common/lcd_lab2_modes.v').write_text('`timescale 1ns/1ps\n'+lcd,encoding='utf-8')
    pulse=(REFERENCE/'src/button_onepulse.v').read_text(encoding='utf-8')
    (LAB/'common/button_onepulse.v').write_text('`timescale 1ns/1ps\n'+pulse,encoding='utf-8')
    entries=json.loads((LAB/'circuits.json').read_text(encoding='utf-8'))
    sources=[LAB/e['path']/'src'/f"{e['top']}.v" for e in entries]
    sources += [LAB/'common'/name for name in ['input_frontend.v','button_onepulse.v','lcd_lab2_modes.v','lab2_integrated.v']]
    basepins=json.loads((LAB/entries[0]['path']/'evidence/board-pin-provenance.json').read_text(encoding='utf-8'))
    arraypins=json.loads((LAB/entries[7]['path']/'evidence/board-pin-provenance.json').read_text(encoding='utf-8'))['pins']
    pins={('mode_button' if k=='button' else k):v for k,v in basepins['pins'].items()}
    pins['step_button']='N4' # Original array select[0], same physical button SW3.
    pins.update({k:v for k,v in arraypins.items() if k.startswith('seg_')})
    refxdc=REFERENCE/'constraints/lab1_integrated.xdc'
    pins.update({port:pin for pin,port in re.findall(r'set_property PACKAGE_PIN (\S+) \[get_ports \{([^}]+)\}\]',refxdc.read_text(encoding='utf-8')) if port.startswith('lcd_')})
    assert len(pins)==len(set(pins.values()))
    xdc='# Combo II-DLD S75, 1 kHz main clock. See evidence/board-pin-provenance.json.\n'
    for port,pin in pins.items():
        xdc+=f'set_property PACKAGE_PIN {pin} [get_ports {{{port}}}]\nset_property IOSTANDARD LVCMOS33 [get_ports {{{port}}}]\n'
    xdc+='create_clock -name trainer_1khz -period 1000000.000 [get_ports clk]\n'
    xdc+='set_false_path -from [get_ports {rst mode_button step_button sw[*]}]\n'
    for edition in ['vivado_2026_1','opensource_cli']:
        project=LAB/edition/'09_integrated'
        for directory in ['src','sim','constraints','tools','evidence']:
            (project/directory).mkdir(parents=True,exist_ok=True)
        for source in sources: shutil.copyfile(source,project/'src'/source.name)
        for relative in ['LAB1.code-workspace','tools/lab1.py','.gitignore']:
            shutil.copyfile(LAB/entries[0]['path']/relative,project/relative)
        (project/'constraints/lab2_integrated.xdc').write_text(xdc,encoding='utf-8')
        (project/'simulation.json').write_text(json.dumps({'sources':['src/'+s.name for s in sources],
            'testbench':'sim/tb_lab2_integrated.sv','simulation_top':'tb_lab2_integrated'},indent=2)+'\n',encoding='utf-8')
        (project/'board.json').write_text(json.dumps({'top':'lab2_integrated','part':'xc7s75fgga484-1','main_clock_hz':1000,
            'constraints':'constraints/lab2_integrated.xdc'},indent=2)+'\n',encoding='utf-8')
        provenance={**basepins,'pins':pins,'derived_lcd_source':str((REFERENCE/'src/lcd_modes.v').relative_to(ROOT)).replace('\\','/'),
                    'derived_lcd_sha256':hashlib.sha256((REFERENCE/'src/lcd_modes.v').read_bytes()).hexdigest(),
                    'lcd_change':'mode names and mode numbers 01..08; original 1 kHz timing preserved',
                    'status':'constructed; integration simulation and implementation not yet validated'}
        (project/'evidence/board-pin-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Vivado and CLI integration sources prepared: 12 RTL files each;',len(pins),'pins')

if __name__=='__main__': main()
