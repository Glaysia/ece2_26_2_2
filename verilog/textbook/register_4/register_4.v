
module register_4(sw_s, sw_l,i, o);

input sw_s, sw_l;
input [3:0] i;
output [3:0] o;

reg [3:0] o;
reg [3:0] reg_tmp;

always @(posedge sw_s)
	if (sw_s)	reg_tmp = i;

always @(posedge sw_l)
	if (sw_l)	o = reg_tmp;

endmodule

	
