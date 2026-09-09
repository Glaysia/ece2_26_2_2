
module adder_4bit(	a, b, s, cout);

input [3:0] a, b;

output [3:0] s;
output cout;

reg [3:0] s;
reg cout;


always @(a or b)
begin
	s = a + b;
	
	if ((a+b) > 5'b01111)	 cout = 1'b1;
	else   		             cout = 1'b0;
end

endmodule
