
module encoder8x3(i, a);

input [7:0] i;
output [2:0] a;

reg [2:0] a;

always @(i)
begin

	if (i == 8'b0000_0000) a = 3'b000 ;
	else if (i == 8'b1000_0000) a = 3'b000;
	else if (i == 8'b0100_0000) a = 3'b001;
	else if (i == 8'b0010_0000) a = 3'b010;
	else if (i == 8'b0001_0000) a = 3'b011;
	else if (i == 8'b0000_1000) a = 3'b100;
	else if (i == 8'b0000_0100) a = 3'b101;
	else if (i == 8'b0000_0010) a = 3'b110;
	else if (i == 8'b0000_0001) a = 3'b111;
	else a=3'b000;

end

endmodule
