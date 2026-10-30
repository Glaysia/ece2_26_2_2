`timescale 1ns/1ps
module tb_board;
    reg clk=0, rst=0, button=0;
    reg [7:0] sw=0;
    wire [7:0] led;
    
    lab2_clock_divider #(.STABLE_CYCLES(3), .DIVISOR(10)) dut(clk,rst,button,sw,led);
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
 
        $display("LAB2_BOARD_PASS lab2_clock_divider checks=%0d",checks);
        $finish;
    end
endmodule
