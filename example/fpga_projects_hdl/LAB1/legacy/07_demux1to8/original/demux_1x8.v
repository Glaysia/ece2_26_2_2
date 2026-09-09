
module demux_1x8(i, s, o);

input i;
input [2:0] s;

output [7:0] o;

wire [7:0] o;

assign o[7] = (s == 3'b000) ? i : 1'b0;
assign o[6] = (s == 3'b001) ? i : 1'b0;
assign o[5] = (s == 3'b010) ? i : 1'b0;
assign o[4] = (s == 3'b011) ? i : 1'b0;
assign o[3] = (s == 3'b100) ? i : 1'b0;
assign o[2] = (s == 3'b101) ? i : 1'b0;
assign o[1] = (s == 3'b110) ? i : 1'b0;
assign o[0] = (s == 3'b111) ? i : 1'b0;

endmodule
