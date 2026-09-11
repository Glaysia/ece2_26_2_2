"""Add S75 board connections to independent LAB2 lessons; preserve core TBs."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'
LAB1=ROOT/'example/fpga_projects_hdl/LAB1/vivado_2026_1/11_integrated'
OLD_ARRAY=ROOT/'legacy/notebook/cpp/verilog/W4/12_seg_decoder_array'

BODIES={
    'counter4': ('''wire [3:0] value;
    counter4 core(clk, reset, press, switches[0], value);
    assign led = {4'b0000, value};''',
                 'SW8(sw[0]): 0 증가/1 감소. 버튼 한 번당 한 단계. LED[3:0]에 값.'),
    'clock_divider': ('''wire divided, tick, div2, div10, div50;
    clock_divider #(.DIVISOR(2)) ratio2(.clk(clk), .rst(reset), .divided(div2), .tick());
    clock_divider #(.DIVISOR(10)) ratio10(.clk(clk), .rst(reset), .divided(div10), .tick());
    clock_divider #(.DIVISOR(50)) ratio50(.clk(clk), .rst(reset), .divided(div50), .tick());
    clock_divider #(.DIVISOR(DIVISOR)) core(clk, reset, divided, tick);
    assign led = {3'b000, tick, divided, div50, div10, div2};''',
                      '1 kHz 주 클록에서 LED[0:2]는 각각 /2=500 Hz, /10=100 Hz, /50=20 Hz. LED[3]은 /1000=1 Hz 관찰 기준. LED[4]의 tick은 1 ms 펄스이므로 파형에서 확인.'),
    'register_pair': ('''wire [3:0] stored, value;
    register_pair core(clk, reset, press && switches[0],
                       press && switches[1], switches[7:4], stored, value);
    assign led = {stored, value};''',
                      'SW1..4(sw[7:4]): 데이터. SW8(sw[0]): load, SW7(sw[1]): transfer 허용. 버튼으로 실행. LED[7:4]=stored, LED[3:0]=value.'),
    'shift_register4': ('''wire [3:0] value;
    shift_register4 core(clk, reset, press, switches[7], value);
    assign led = {4'b0000, value};''',
                        'SW1(sw[7]): 직렬 입력. 버튼 한 번당 bit 3에서 bit 0 방향으로 한 단계 이동. LED[3:0]에 값.'),
    'piso4': ('''wire serial_out;
    wire [3:0] value;
    piso4 core(clk, reset, press && switches[0], press && !switches[0],
               switches[7:4], serial_out, value);
    assign led = {value, 3'b000, serial_out};''',
              'SW1..4(sw[7:4]): 병렬 데이터. SW8(sw[0])=1에서 버튼: load, 0에서 버튼: shift. LED[7:4]=저장값, LED[0]=직렬 출력.'),
    'moore_cycle': ('''wire [1:0] value;
    moore_cycle core(clk, reset, press, switches[7], value);
    assign led = {6'b000000, value};''',
                    'SW1(sw[7]): advance. 1에서 버튼을 누르면 00→01→10→00. SW1만 바꾸면 상태 출력은 유지. LED[1:0]=상태.'),
    'mealy_toggle': ('''wire state;
    wire [1:0] value;
    mealy_toggle core(clk, reset, press, switches[7], state, value);
    assign led = {5'b00000, state, value};''',
                     'SW1(sw[7]): 입력. 1에서 버튼을 누르면 상태 전환. 버튼 없이 SW1을 바꿔도 동기화 지연 후 출력 변화. LED[2]=상태, LED[1:0]=출력.'),
    'segment_scan8': ('''wire [7:0] selected, segments;
    wire [2:0] index;
    wire [31:0] digits = {28'h7654321, switches[7:4]};
    segment_scan8 core(clk, reset, 1'b1, digits, selected, segments, index);
    // Legacy array selects are active-low; index 0 is COM[7].
    assign seg_com = ~{selected[0],selected[1],selected[2],selected[3],
                       selected[4],selected[5],selected[6],selected[7]};
    assign seg_data = segments;
    assign led = {5'b00000, index};''',
                       'SW1..4(sw[7:4]): 첫 자리 숫자. COM[7]부터 입력값,1,2,3,4,5,6,7 순서. 1 kHz에서 자리당 62.5 Hz, blanking 포함.')
}

def pinmap(path):
    return {port:pin for pin,port in re.findall(r'set_property PACKAGE_PIN (\S+) \[get_ports \{([^}]+)\}\]',path.read_text(encoding='utf-8'))}

def main():
    shared=LAB/'common/input_frontend.v'
    boardpins=pinmap(LAB1/'constraints/lab1_integrated.xdc')
    arraypins=pinmap(OLD_ARRAY/'pin.xdc')
    provenance={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [LAB1/'constraints/lab1_integrated.xdc',OLD_ARRAY/'pin.xdc',OLD_ARRAY/'seg_decoder_array.v']}
    manifest=json.loads((LAB/'circuits.json').read_text(encoding='utf-8'))
    for entry in manifest:
        project=LAB/entry['path']; core=entry['top']; board='lab2_'+project.name.split('_',1)[1]
        body,controls=BODIES[core]
        output_extra=',\n    output wire [7:0] seg_data, seg_com' if core=='segment_scan8' else ''
        params='parameter integer STABLE_CYCLES = 20'+(', DIVISOR = 1000' if core=='clock_divider' else '')
        rtl=f'''`timescale 1ns/1ps
// Combo II-DLD S75. Main clock B6 MUST be set to 1 kHz.
// K4: reset. N8: step button. DIPSW1..8 = sw[7]..sw[0].
module {board} #({params}) (
    input wire clk, rst, button,
    input wire [7:0] sw,
    output wire [7:0] led{output_extra}
);
    wire reset, press;
    wire [7:0] switches;
    input_frontend #(.STABLE_CYCLES(STABLE_CYCLES)) inputs(
        clk, rst, button, sw, reset, press, switches);
    {body}
endmodule
'''
        (project/'src'/f'{board}.v').write_text(rtl,encoding='utf-8')
        shutil.copyfile(shared,project/'src/input_frontend.v')
        pins={'clk':boardpins['clk'],'rst':boardpins['rst'],'button':boardpins['mode_button']}
        pins.update({f'{bus}[{i}]':boardpins[f'{bus}[{i}]'] for bus in ['sw','led'] for i in range(8)})
        if core=='segment_scan8':
            pins.update({f'{bus}[{i}]':arraypins[f'{bus}[{i}]'] for bus in ['seg_data','seg_com'] for i in range(8)})
        assert len(set(pins.values()))==len(pins)
        xdc='# Combo II-DLD S75 / xc7s75fgga484-1 / main clock 1 kHz.\n'
        xdc+='# Pin source and array polarity: evidence/board-pin-provenance.json.\n'
        for port,pin in pins.items():
            xdc+=f'set_property PACKAGE_PIN {pin} [get_ports {{{port}}}]\n'
            xdc+=f'set_property IOSTANDARD LVCMOS33 [get_ports {{{port}}}]\n'
        xdc+='create_clock -name trainer_1khz -period 1000000.000 [get_ports clk]\n'
        # Button, reset and switches are asynchronous external inputs; only the
        # synchronizer first stage is a CDC entry. Do not waive dedicated clock routing.
        xdc+='set_false_path -from [get_ports {rst button sw[*]}]\n'
        (project/'constraints').mkdir(exist_ok=True)
        (project/'constraints'/f'{board}.xdc').write_text(xdc,encoding='utf-8')
        (project/'evidence').mkdir(exist_ok=True)
        record={'part':'xc7s75fgga484-1','main_clock_hz':1000,'sources_sha256':provenance,'pins':pins,
                'array_polarity':{'seg_data':'active-high abcdefg,dp','seg_com':'active-low; logical index 0 -> COM[7]'},
                'status':'source mapping; hardware execution not performed'}
        (project/'evidence/board-pin-provenance.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        cfg=json.loads((project/'simulation.json').read_text(encoding='utf-8'))
        cfg['sources']=[f'src/{core}.v','src/input_frontend.v',f'src/{board}.v']
        (project/'simulation.json').write_text(json.dumps(cfg,indent=2)+'\n',encoding='utf-8')
        (project/'board.json').write_text(json.dumps({'part':'xc7s75fgga484-1','top':board,
                                                    'constraints':f'constraints/{board}.xdc','main_clock_hz':1000},indent=2)+'\n',encoding='utf-8')
        entry.update(board_top=board,constraints=f'constraints/{board}.xdc',controls=controls,status='board-connection-draft')
        readme=f'''# {entry['title']} · LAB2

학생용 시작점은 빈 템플릿 v2.0.0이다. 이 폴더는 강사용 완성 코드 예시를 제작 중인 작업본이다.

```powershell
git clone --branch v2.0.0 https://github.com/Glaysia/fpga-lab-template.git lab2_{project.name}
cd lab2_{project.name}
git switch -c main
code LAB1.code-workspace
```

기능 코어: `{core}` / Vivado 설계 top: `{board}` / 시뮬레이션 top: `{cfg['simulation_top']}`.

- `src/{core}.v`: 직접 학습하는 회로.
- `src/input_frontend.v`: 리셋 해제 동기화, 두 단계 입력 동기화, 20 ms 버튼 디바운스와 한 클록 펄스.
- `src/{board}.v`: 입력·출력을 코어와 보드 핀 이름에 연결.
- `{cfg['testbench']}`: 기능 코어의 자기검사. 보드 핀 검증과 구분한다.
- `constraints/{board}.xdc`: {len(pins)}개 포트, S75 핀과 LVCMOS33, 1 kHz 주 클록 제약.

장비 설정: 주 클록을 **1 kHz**로 설정하고 초기화 버튼 K4를 누른 뒤 놓는다. 버튼 N8은 클록이 아니라 입력이다. 스위치를 먼저 정하고 버튼을 누른다.

{controls}

입력 동기화 때문에 버튼과 DIP 입력은 즉시 반영되지 않는다. 버튼은 누름과 뗌 모두 충분한 안정 시간이 필요하다. 기계적 접점과 메타안정성의 실제 특성은 기능 시뮬레이션만으로 증명하지 않는다.

실행: Terminal → Run Task... → 02 Simulate. 보드 연결 검증 및 실제 장치 실행 상태는 상위 LAB2 검증 기록을 확인한다.
'''
        (project/'README.md').write_text(readme,encoding='utf-8')
    (LAB/'circuits.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('8 board wrappers and XDCs prepared')

if __name__=='__main__': main()
