`timescale 1ns/1ps
module tb_board;
    reg clk=0, rst=0, button=0;
    reg [7:0] sw=0;
    wire [7:0] led;
    wire [7:0] seg_data,seg_com;
    lab2_segment_scan #(.STABLE_CYCLES(3)) dut(clk,rst,button,sw,led,seg_data,seg_com);
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
 
        $display("LAB2_BOARD_PASS lab2_segment_scan checks=%0d",checks);
        $finish;
    end
endmodule
