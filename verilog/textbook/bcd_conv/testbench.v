`timescale 10ns / 100ps

module testbench();
// input
reg [3:0] ten, one;
// output
wire [6:0] bin;
// Instantiate the U1
bcd_conv u1(one, ten, bin);
// Specify input stimulus
initial begin
    	ten = 0; one = 0;
    #10 ten = 0; one = 3;
    #10 ten = 2; one = 1;
    #10 ten = 1; one = 8;
    #10 ten = 6; one = 2;
    #10 ten = 4; one = 1;
    #10 ten = 0; one = 0;
	
end

endmodule

