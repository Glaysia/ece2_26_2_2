`timescale 1ns/1ps
module tb_stepper;
    reg clk=0,rst=1,enable=0,direction=0;
    wire [3:0] stepmotor;
    integer checks=0;
    always #5 clk=~clk;
    lab3_stepper #(.CLK_HZ(8),.STEP_HZ(2)) dut
      (.clk(clk),.rst(rst),.enable(enable),.direction(direction),.stepmotor(stepmotor));
    task check_value(input [3:0] value);begin #1;if(stepmotor!==value)$fatal(1,"got=%b expected=%b",stepmotor,value);checks++;end endtask
    initial begin
      $dumpfile("wave.vcd");$dumpvars(0,tb_stepper);
      repeat(2)@(posedge clk);rst=0;check_value(4'b0011);
      enable=1;wait(dut.enable_sync);wait(dut.state==1);check_value(4'b0110);
      wait(dut.state==2);check_value(4'b1100);
      wait(dut.state==3);check_value(4'b1001);
      wait(dut.state==0);check_value(4'b0011);
      direction=1;wait(dut.direction_sync);wait(dut.state==3);check_value(4'b1001);
      wait(dut.state==2);check_value(4'b1100);
      enable=0;wait(!dut.enable_sync);repeat(12)@(posedge clk);check_value(4'b1100);
      $display("LAB3_STEPPER_PASS checks=%0d",checks);$finish;
    end
    initial begin #5000;$fatal(1,"timeout");end
endmodule
