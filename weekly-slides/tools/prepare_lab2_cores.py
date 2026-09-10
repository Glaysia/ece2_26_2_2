"""Scaffold independent LAB2 simulation lessons; never modifies the template repo."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'example/fpga_projects_hdl/LAB2'
TEMPLATE = ROOT / 'example/fpga_projects_hdl/LAB1/vivado_2026_1/01_logic_gates'

LESSONS = [
    ('01_counter', 'counter4', '업/다운 카운터', 16, '''
reg enable=0, down=0;
wire [3:0] value;
counter4 dut(clk,rst,enable,down,value);
integer i;
initial begin
    step; check(value===0,"reset"); rst=0;
    enable=1;
    for(i=1;i<=16;i=i+1) begin
        step; check(value===(i%16),"up including 15 to 0");
    end
    down=1;
    for(i=15;i>=0;i=i-1) begin
        step; check(value===i,"down including 0 to 15");
    end
    enable=0; step; check(value===0,"hold");
    enable=1; step; check(value===15,"down wrap");
    rst=1; step; check(value===0,"reset beats enable");
    finish;
end
'''),
    ('02_clock_divider', 'clock_divider', '클록 분주', 17, '''
wire divided, tick, div2, tick2;
clock_divider #(.DIVISOR(10)) dut(clk,rst,divided,tick);
clock_divider #(.DIVISOR(2)) minimum(clk,rst,div2,tick2);
integer i, pulses=0;
always @(posedge clk) if (!rst && tick) pulses = pulses+1;
initial begin
    step; check({divided,tick,div2,tick2}===4'b0000,"reset");
    rst=0;
    for(i=1;i<=30;i=i+1) begin
        step;
        check(divided===(i%10>=5),"divide 10 duty and phase");
        check(tick===(i%10==9),"tick before consuming edge");
        check(div2===(i%2==1),"minimum divisor duty");
        check(tick2===(i%2==1),"minimum tick");
    end
    check(pulses===3,"three consumed enables in 30 clocks");
    repeat(7) step;
    rst=1; #1; check(tick===0,"reset masks tick before edge");
    step; check(divided===0,"reset mid period");
    rst=0;
    repeat(4) begin step; check(divided===0,"restart low half"); end
    step; check(divided===1,"restart first transition");
    finish;
end
'''),
    ('03_register', 'register_pair', '레지스터: 데이터 저장과 이동', 26, '''
reg load=0, transfer=0;
reg [3:0] data_in=0;
wire [3:0] stored,value;
register_pair dut(clk,rst,load,transfer,data_in,stored,value);
initial begin
    step; check({stored,value}===8'h00,"reset"); rst=0;
    data_in=4'ha; load=1; step;
    check({stored,value}===8'ha0,"load does not transfer");
    load=0; data_in=4'h3; transfer=1; step;
    check({stored,value}===8'haa,"transfer stored not live input");
    load=1; step;
    check({stored,value}===8'h3a,"simultaneous uses old stored");
    step; check({stored,value}===8'h33,"next edge transfers new stored");
    load=0; transfer=0; data_in=4'hf; step;
    check({stored,value}===8'h33,"both hold");
    rst=1; load=1; transfer=1; step;
    check({stored,value}===8'h00,"reset beats both controls");
    finish;
end
'''),
    ('04_shift_register', 'shift_register4', '시프트 레지스터', 27, '''
reg enable=0, serial_in=0;
wire [3:0] value;
shift_register4 dut(clk,rst,enable,serial_in,value);
initial begin
    step; check(value===0,"reset"); rst=0; enable=1;
    serial_in=1; step; check(value===4'b1000,"input enters MSB");
    serial_in=0; step; check(value===4'b0100,"move toward LSB");
    enable=0; serial_in=1; step; check(value===4'b0100,"hold");
    enable=1; step; check(value===4'b1010,"retain old stage values");
    serial_in=0; step; check(value===4'b0101,"four bit history");
    repeat(4) step; check(value===0,"flush with four zeros");
    serial_in=1; rst=1; step; check(value===0,"reset priority");
    finish;
end
'''),
    ('05_piso', 'piso4', 'PISO', 28, '''
reg load=0, enable=0;
reg [3:0] data_in=0;
wire serial_out;
wire [3:0] value;
piso4 dut(clk,rst,load,enable,data_in,serial_out,value);
integer word, bit_number;
initial begin
    step; check(value===0,"reset"); rst=0;
    for(word=0;word<16;word=word+1) begin
        data_in=word; load=1; enable=1; step;
        check(value===word,"load beats shift");
        load=0; enable=0; step; check(value===word,"hold");
        enable=1;
        for(bit_number=3;bit_number>=0;bit_number=bit_number-1) begin
            check(serial_out===((word>>bit_number)&1),"MSB first before edge");
            step;
        end
        check(value===0,"four shifts zero fill");
    end
    rst=1; load=1; data_in=15; step;
    check(value===0,"reset beats load"); finish;
end
'''),
    ('06_moore', 'moore_cycle', 'Moore 상태 머신', 29, '''
reg enable=0, advance=0;
wire [1:0] value;
moore_cycle dut(clk,rst,enable,advance,value);
integer round;
initial begin
    step; check(value===0,"reset"); rst=0; enable=1;
    advance=1; #1; check(value===0,"input alone cannot change output");
    for(round=0;round<4;round=round+1) begin
        step; check(value===1,"S0 to S1");
        advance=0; step; check(value===1,"advance zero holds");
        advance=1; enable=0; step; check(value===1,"disabled holds");
        enable=1; step; check(value===2,"S1 to S2");
        step; check(value===0,"S2 to S0");
    end
    step; rst=1; step; check(value===0,"reset from nonzero"); finish;
end
'''),
    ('07_mealy', 'mealy_toggle', 'Mealy 상태 머신', 30, '''
reg enable=0, bit_in=0;
wire state;
wire [1:0] value;
mealy_toggle dut(clk,rst,enable,bit_in,state,value);
initial begin
    step; check({state,value}===3'b000,"reset input zero"); rst=0;
    bit_in=1; #1; check({state,value}===3'b010,"S0 input changes between clocks");
    step; check({state,value}===3'b010,"disabled state still has Mealy output");
    enable=1; step; check({state,value}===3'b101,"transition to S1");
    bit_in=0; #1; check({state,value}===3'b100,"S1 input zero immediately");
    step; check(state===1,"input zero holds S1");
    bit_in=1; #1; check(value===1,"S1 pre-edge value");
    step; check({state,value}===3'b010,"transition to S0");
    step; check(state===1,"toggle again");
    rst=1; step; check({state,value}===3'b010,"reset state with input one");
    bit_in=0; #1; check(value===0,"clear combinational output"); finish;
end
'''),
    ('08_segment_scan', 'segment_scan8', '7세그먼트 자리 스캔', 12, '''
reg enable=0;
reg [31:0] digits=32'h76543210;
wire [7:0] select,segments;
wire [2:0] index;
segment_scan8 dut(clk,rst,enable,digits,select,segments,index);
reg [7:0] expected[0:15];
integer bank, position, lap;
initial begin
    // Truth-table values, ordered 0..F with abcdefg and dp.
    expected[0]=8'hfc; expected[1]=8'h60; expected[2]=8'hda; expected[3]=8'hf2;
    expected[4]=8'h66; expected[5]=8'hb6; expected[6]=8'hbe; expected[7]=8'he0;
    expected[8]=8'hfe; expected[9]=8'hf6; expected[10]=8'hee; expected[11]=8'h3e;
    expected[12]=8'h9c; expected[13]=8'h7a; expected[14]=8'h9e; expected[15]=8'h8e;
    step; check(select===0 && index===0,"reset blanks digit zero"); rst=0;
    for(bank=0;bank<2;bank=bank+1) begin
        digits=bank ? 32'hfedcba98 : 32'h76543210;
        for(lap=0;lap<2;lap=lap+1) begin
            for(position=0;position<8;position=position+1) begin
                enable=1; step;
                check(index===position,"position order");
                check(select===(1<<position),"exactly intended digit active");
                check(segments===expected[bank*8+position],"hex truth table");
                enable=0; step;
                check(select===(1<<position),"enable zero holds active slot");
                enable=1; step;
                check(select===0,"blank interval between every digit");
                enable=0; step; check(select===0,"blank interval hold");
            end
        end
    end
    enable=1; step; rst=1; step;
    check(select===0 && index===0,"reset from active scan"); finish;
end
'''),
]

# Reused bench harness deliberately drives inputs after a sampled edge and
# checks after nonblocking assignments have committed, avoiding TB races.
HARNESS = '''`timescale 1ns/1ps
module tb_{top};
reg clk=0, rst=1;
integer checks=0;
always #5 clk=~clk;
task step; begin @(posedge clk); #1; end endtask
task check(input condition, input [8*100-1:0] description);
begin
    checks=checks+1;
    if (condition !== 1'b1) begin
        $display("LAB2_FAIL %0s time=%0t",description,$time);
        $fatal(1,"check failed");
    end
end
endtask
task finish;
begin
    $display("LAB2_PASS {top} checks=%0d",checks);
    $finish;
end
endtask
initial begin $dumpfile("wave.vcd"); $dumpvars(0,tb_{top}); end
initial begin #100000; $fatal(1,"watchdog timeout"); end
{body}
endmodule
'''

def main():
    manifest=[]
    for number,(folder,top,title,original,body) in enumerate(LESSONS,11):
        project=LAB/'vivado_2026_1'/folder
        (project/'sim').mkdir(parents=True,exist_ok=True)
        (project/'sim'/f'tb_{top}.sv').write_text(HARNESS.format(top=top,body=body.strip()),encoding='utf-8')
        config={'sources':[f'src/{top}.v'],'testbench':f'sim/tb_{top}.sv','simulation_top':f'tb_{top}'}
        (project/'simulation.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
        # Template files are inspected separately; keep their recommended extensions.
        for relative in ['LAB1.code-workspace','tools/lab1.py']:
            source=TEMPLATE/relative
            if not source.is_file():
                raise FileNotFoundError(f'Initialize the LAB1 example submodule first: {source}')
            destination=project/relative
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,destination)
        (project/'.gitignore').write_text('/build/\n/.runs/\n/wave.vcd\n*.vvp\n',encoding='utf-8')
        manifest.append({'education_number':number,'title':title,'original_experiment':original,
                         'path':f'vivado_2026_1/{folder}','top':top,'status':'core-simulation-draft'})
    (LAB/'circuits.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
