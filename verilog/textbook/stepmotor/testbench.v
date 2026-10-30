`timescale 10ns / 10ps

module testbench();
// input
reg rst, clk;
// output
wire [3:0] stepmotor;
// Instantiate the U1
stepmotor u1(clk, rst, stepmotor);
// Specify input stimulus
initial begin
		rst = 1; clk = 0;

	#5 	rst = 0;
end

always #1 clk = ~clk;

endmodule

