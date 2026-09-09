
module compare_4(  a, b,  o);

input [3:0] a, b;
output [2:0] o;

wire [2:0] o;

assign o[2] = ( a > b ) ? 1'b1 : 1'b0;
assign o[1] = ( a == b ) ? 1'b1 : 1'b0;
assign o[0] = ( a < b ) ? 1'b1 : 1'b0;

endmodule
