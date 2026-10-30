`timescale 10ns / 10ps

module testbench();
// input
reg rst, x;
// output
wire [1:0] y;
// Instantiate the U1
mealy u1(rst, x, y);
// Specify input stimulus
initial begin
		rst = 1; x = 0;
	#10 rst = 0;
end

always #5 x = ~x;

endmodule

