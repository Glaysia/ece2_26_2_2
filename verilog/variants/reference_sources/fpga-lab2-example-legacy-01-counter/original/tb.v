`timescale 10ns/100ps

module tb();

reg rst, updn, clk;

wire [3:0] q;

counter_dnup TB1(rst, updn, clk, q);

initial begin
    rst=1;updn=0;clk=0;
    #5 rst=0;
    #50 updn=1;
end

always #2 clk=~clk;
//1Mhz
endmodule
