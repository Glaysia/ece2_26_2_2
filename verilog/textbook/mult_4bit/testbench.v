`timescale 10ns / 100ps

module testbench();
// input
reg [3:0] a, b;
// output
wire [7:0] m;
// Instantiate the U1
mult_4bit u1(a, b, m);
// Specify input stimulus
initial begin
    	a = 4'b0000; b = 4'b0000;
    #20 a = 4'b1010; b = 4'b0111;
    #20 a = 4'b0110; b = 4'b0101;
    #20 a = 4'b0101; b = 4'b0101;
    #20 a = 4'b0010; b = 4'b1001;
end

endmodule

