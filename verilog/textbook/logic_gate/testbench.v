`timescale 10ns / 100ps

module testbench();
// input
reg a, b;
// output
wire x, y, z;
// Instantiate the U1
logic_gate(a, b, x, y, z);
// Specify input stimulus
initial begin
	a = 0; b = 0;
end

always begin
	#10 a = ~a;
	#20 b = ~b;
end

endmodule

