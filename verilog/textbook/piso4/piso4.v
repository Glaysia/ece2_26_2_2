
module piso4(
	shldn, clk, d, q
);

input clk, shldn;
input [3:0] d;
output q;

reg [3:0] tmp;

always @(posedge shldn or posedge clk)
	
	if (shldn) 	tmp = d;
	else 			tmp = {tmp[2:0], 1'b0};

assign q = tmp[3];

endmodule

		