`timescale 10ns / 100ps

module testbench();
// input
reg a, b;
// output
wire x, y, z;
// Instantiate the U1
logic_gate u1(a, b, x, y, z);
// Specify input stimulus
initial begin
	a = 0; b = 0;
	
	#20 a = 1;
	#20 a = 0; b = 1;
	#20 a = 1;
end

endmodule

