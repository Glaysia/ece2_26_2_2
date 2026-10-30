`timescale 10ns / 100ps

module testbench();

// input
reg a;
// output
wire z;

// Instantiate the U1
not_gate u1( a, z);

// Specify input stimulus
initial begin
	a = 0;
end

always begin
	#10 a = ~a;
end

endmodule
