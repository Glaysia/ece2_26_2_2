// Supplement: original borrow comparison a > b is corrected to a >= b.
// Original ZIP bytes remain in ../original/sub_4bit.v.

module sub_4bit(a, b, d, bor);

input [3:0] a, b;

output [3:0] d;
output bor;

reg [3:0] d;
reg bor;

always @(a or b)
begin
	d = a - b;
	
	if (a >= b)	bor = 1'b0;
	else		bor = 1'b1;
end

endmodule
