`timescale 10us/100ns

module tb();

reg rst, clk;

wire o_100, o_50, o_10, o_2;
freq_div u1(rst, clk, o_100,o_50, o_10, o_2);

initial begin
    rst=1;clk=0;
    #1000 rst=0;
end

always #500 clk=~clk;
//100Hz

endmodule
