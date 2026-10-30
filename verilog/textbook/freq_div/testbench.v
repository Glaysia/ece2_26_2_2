`timescale 10ns / 10ps

module testbench();
// input
reg rst, clk;
// output
wire o_100, o_50, o_10, o_2;
// Instantiate the U1
freq_div u1(rst, clk, o_100, o_50, o_10, o_2);
// Specify input stimulus
initial begin
		rst = 1; clk = 0;

	#5 	rst = 0;
end

always #1 clk = ~clk;

endmodule

