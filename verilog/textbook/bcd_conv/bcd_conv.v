
module bcd_conv(  one, ten,  bin);

input [3:0] one, ten;
output [6:0] bin;

wire [6:0] reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8;
wire [6:0] bin;

assign reg1 = (one[0]) ? 7'b0000001 : 7'b0000000;
assign reg2 = (one[1]) ? 7'b0000010 : 7'b0000000;
assign reg3 = (one[2]) ? 7'b0000100 : 7'b0000000;
assign reg4 = (one[3]) ? 7'b0001000 : 7'b0000000;
assign reg5 = (ten[0]) ? 7'b0001010 : 7'b0000000;
assign reg6 = (ten[1]) ? 7'b0010100 : 7'b0000000;
assign reg7 = (ten[2]) ? 7'b0101000 : 7'b0000000;
assign reg8 = (ten[3]) ? 7'b1010000 : 7'b0000000;

assign bin = reg1 + reg2 + reg3 + reg4 + reg5 + reg6 + reg7 + reg8;

endmodule
