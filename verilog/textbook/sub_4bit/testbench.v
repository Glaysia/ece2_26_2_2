`timescale 10ns / 100ps

module testbench();
// input
reg [3:0] a, b;
// output
wire bor;
wire [3:0] d;
// Instantiate the U1
sub_4bit u1(a, b, d, bor);
// Specify input stimulus
initial begin
    	a = 4'b0000; b = 4'b0000;
    #10 a = 4'b1010; b = 4'b0111;
    #10 a = 4'b0110; b = 4'b0101;
    #10 a = 4'b0101; b = 4'b0101;
    #10 a = 4'b0010; b = 4'b1001;
end

endmodule

