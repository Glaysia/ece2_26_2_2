`timescale 10ns / 100ps

module testbench();
// input
reg a, b, c;
// output
wire d, bor;
// Instantiate the U1
full_sub u1(a, b, c, d, bor);
// Specify input stimulus
initial begin
    	a = 0; b = 0; c=0;
    #10 a = 1; b = 0; c=0;
    #10 a = 0; b = 1; c=0;
    #10 a = 1; b = 1; c=0;
    #10 a = 0; b = 0; c=1;
    #10 a = 1; b = 0; c=1;
    #10 a = 0; b = 1; c=1;
    #10 a = 1; b = 1; c=1;
    #10 a = 0; b = 0; c=0;
end

endmodule

