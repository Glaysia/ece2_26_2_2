"""Exercise board wrappers with external switch/button signals and check XDC coverage."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'
CASES={
 'counter4': '''
    set_switches(0); push_button;
    check(led===8'h01,"one bounced press increments once");
    set_switches(1); push_button; check(led===0,"down to zero");
    push_button; check(led===15,"down wraps to 15");
    reset_board; check(led===0,"reset count from 15");
 ''',
 'clock_divider': '''
    for(i=1;i<=100;i=i+1) begin
        step;
        check(led[0]===(i%2==1),"divide by 2");
        check(led[1]===(i%10>=5),"divide by 10");
        check(led[2]===(i%50>=25),"divide by 50");
        check(led[3]===(i%10>=5),"accelerated slow reference phase and duty");
        check(led[4]===(i%10==9),"tick mapped to LED4");
        check(led[7:5]===0,"unused LEDs off");
    end
    reset_board; check(led===0,"divider reset restarts phase");
 ''',
 'register_pair': '''
    set_switches(8'ha1); push_button; check(led===8'ha0,"load stores DIP upper nibble");
    set_switches(8'h32); push_button; check(led===8'haa,"transfer excludes current DIP");
    set_switches(8'h33); push_button; check(led===8'h3a,"simultaneous transfers old stored");
    push_button; check(led===8'h33,"next press transfers new stored");
    reset_board; check(led===0,"both registers reset");
 ''',
 'shift_register4': '''
    set_switches(8'h80); push_button; check(led===8'h08,"MSB serial input");
    set_switches(0); push_button; check(led===8'h04,"right shift");
    set_switches(8'h80); push_button; check(led===8'h0a,"history preserved");
    set_switches(0); push_button; check(led===8'h05,"four sampled bits");
    reset_board; check(led===0,"shift register reset");
 ''',
 'piso4': '''
    set_switches(8'ha1); push_button; check(led===8'ha1,"load 1010, first serial bit 1");
    set_switches(8'ha0); push_button; check(led===8'h40,"shift to 0100, output 0");
    push_button; check(led===8'h81,"shift to 1000, output 1");
    push_button; check(led===8'h00,"shift to 0000, output 0");
    push_button; check(led===8'h00,"zero fill continues");
 ''',
 'moore_cycle': '''
    set_switches(8'h80); check(led===0,"switch alone cannot change Moore state");
    push_button; check(led===1,"Moore S0 to S1");
    set_switches(0); push_button; check(led===1,"advance zero holds");
    set_switches(8'h80); push_button; check(led===2,"Moore S1 to S2");
    push_button; check(led===0,"Moore S2 to S0");
 ''',
 'mealy_toggle': '''
    set_switches(8'h80); check(led===2,"switch changes Mealy output before button");
    push_button; check(led===5,"state S1 and output 01");
    set_switches(0); check(led===4,"input zero changes only output");
    push_button; check(led===4,"zero holds state S1");
    set_switches(8'h80); check(led===5,"S1 input one before transition");
    push_button; check(led===2,"back to S0");
 ''',
 'segment_scan8': '''
    set_switches(8'h90);
    for(i=0;i<64;i=i+1) begin
        step;
        check(led[7:3]===0,"index occupies only LED2..0");
        if(seg_com!==8'hff) begin
            check(seg_com===(8'hff ^ (8'h80>>led[2:0])),"active low reversed COM order");
            case(led[2:0])
                0:check(seg_data===8'hf6,"DIP9 displayed on COM7");
                1:check(seg_data===8'h60,"fixed digit1");
                2:check(seg_data===8'hda,"fixed digit2");
                3:check(seg_data===8'hf2,"fixed digit3");
                4:check(seg_data===8'h66,"fixed digit4");
                5:check(seg_data===8'hb6,"fixed digit5");
                6:check(seg_data===8'hbe,"fixed digit6");
                7:check(seg_data===8'he0,"fixed digit7");
            endcase
            active_slots=active_slots+1;
        end else blank_slots=blank_slots+1;
    end
    check(active_slots==32 && blank_slots==32,"half slots blank, four complete scans");
    reset_board; check(seg_com===8'hff,"reset disables all physical digits");
 '''
}

BENCH='''`timescale 1ns/1ps
module tb_board;
    reg clk=0, rst=0, button=0;
    reg [7:0] sw=0;
    wire [7:0] led;
    {extra_declaration}
    {top} #(.STABLE_CYCLES(3){extra_parameter}) dut(clk,rst,button,sw,led{extra_connection});
    always #5 clk=~clk;
    integer checks=0, presses=0, i, before_press, active_slots=0, blank_slots=0;
    always @(posedge clk) if(!dut.reset && dut.press) presses=presses+1;
    task step; begin @(posedge clk); #1; end endtask
    task check(input condition, input [8*100-1:0] description);
    begin
        checks=checks+1;
        if(condition!==1'b1) begin $display("LAB2_BOARD_FAIL %0s",description); $fatal(1,"check failed"); end
    end endtask
    task reset_board;
    begin
        rst=1; button=0; repeat(3) step;
        rst=0; step; check(dut.reset===1,"reset release first synchronizer stage");
        step; check(dut.reset===0,"reset release second synchronizer stage");
    end endtask
    task set_switches(input [7:0] value);
    begin sw=value; repeat(4) step; end endtask
    task push_button;
    begin
        before_press=presses;
        button=1; step; button=0; step;
        button=1; step; button=0; repeat(3) step;
        check(presses===before_press,"short bounce cannot trigger");
        button=1; repeat(12) step;
        check(presses===before_press+1,"held button yields one pulse");
        button=0; repeat(12) step;
        check(presses===before_press+1,"release does not trigger");
    end endtask
    initial begin $dumpfile("wave.vcd"); $dumpvars(0,tb_board); end
    initial begin #100000; $fatal(1,"watchdog"); end
    initial begin
        #2; reset_board;
        check(led===0,"reset LEDs");
        {case}
        $display("LAB2_BOARD_PASS {top} checks=%0d",checks);
        $finish;
    end
endmodule
'''

def main():
    env=os.environ.copy()
    if Path('C:/msys64/mingw64/bin/iverilog.exe').exists():
        env['PATH']='C:/msys64/mingw64/bin'+os.pathsep+env.get('PATH','')
    reports=[]
    for entry in json.loads((LAB/'circuits.json').read_text(encoding='utf-8')):
        project=LAB/entry['path']; top=entry['board_top']; core=entry['top']
        scan=core=='segment_scan8'
        text=BENCH.format(top=top,case=CASES[core],
                          extra_declaration='wire [7:0] seg_data,seg_com;' if scan else '',
                          extra_parameter=', .DIVISOR(10)' if core=='clock_divider' else '',
                          extra_connection=',seg_data,seg_com' if scan else '')
        bench=project/'sim/tb_board.sv'; bench.write_text(text,encoding='utf-8')
        config=json.loads((project/'simulation.json').read_text(encoding='utf-8'))
        (project/'simulation-board.json').write_text(json.dumps({**config,'testbench':'sim/tb_board.sv','simulation_top':'tb_board'},indent=2)+'\n',encoding='utf-8')
        xdc=(project/entry['constraints']).read_text(encoding='utf-8')
        pins=re.findall(r'set_property PACKAGE_PIN (\S+) \[get_ports \{([^}]+)\}\]',xdc)
        ports={p for _,p in pins}
        expected={'clk','rst','button'}|{f'{bus}[{i}]' for bus in (['sw','led','seg_data','seg_com'] if scan else ['sw','led']) for i in range(8)}
        assert ports==expected and len(pins)==len(ports) and len({p for p,_ in pins})==len(pins)
        standards=set(re.findall(r'set_property IOSTANDARD LVCMOS33 \[get_ports \{([^}]+)\}\]',xdc))
        assert standards==ports
        assert 'CLOCK_DEDICATED_ROUTE' not in xdc
        assert '-period 1000000.000' in xdc
        with tempfile.TemporaryDirectory(prefix='lab2-board-') as temporary:
            run=Path(temporary)
            compile=subprocess.run(['iverilog','-g2012','-Wall','-s','tb_board','-o',str(run/'sim.vvp'),
                                    *[str(project/p) for p in config['sources']],str(bench)],cwd=run,env=env,capture_output=True,text=True)
            assert compile.returncode==0,compile.stderr
            sim=subprocess.run(['vvp','-N',str(run/'sim.vvp')],cwd=run,env=env,capture_output=True,text=True,timeout=20)
            assert sim.returncode==0 and f'LAB2_BOARD_PASS {top}' in sim.stdout,(top,sim.stdout,sim.stderr)
            assert not compile.stderr,compile.stderr
            wave=(run/'wave.vcd').read_text(encoding='utf-8')
            reports.append({'path':entry['path'],'top':top,'pins':len(pins),'compile_log':compile.stderr,'simulation_log':sim.stdout,
                            'wave_without_date_sha256':hashlib.sha256(re.sub(r'\$date\b.*?\$end','',wave,flags=re.S).encode()).hexdigest(),
                            'inputs_sha256':{p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                             for p in [*(project/s for s in config['sources']),bench,project/entry['constraints']]}})
            print(sim.stdout.strip(),flush=True)
    report={'scope':'8 board wrapper functional simulations; XDC pin coverage and uniqueness; not Vivado or hardware execution',
            'result':'PASS','projects':reports}
    (LAB/'docs/board-simulation-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
