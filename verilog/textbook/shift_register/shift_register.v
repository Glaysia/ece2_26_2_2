
module shift_register(	i, clk, o);

input i, clk;
output [3:0] o;

reg [3:0] o;

always @(posedge clk)
begin
	o[3] <= i;
	o[2] <= o[3];
	o[1] <= o[2];
	o[0] <= o[1];
end

endmodule
	