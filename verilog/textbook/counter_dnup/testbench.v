`timescale 10ns / 100ps

module testbench();
// input
reg rst, updn, clk;
// output
wire [3:0] q;
// Instantiate the U1
counter_dnup u1(rst, updn, clk, q);
// Specify input stimulus
initial begin
		rst = 1; updn = 0; clk = 0;

	#5 	rst = 0;
	#50 updn = 1;	
	
end

always #2 clk = ~clk;

endmodule

