
module half_adder(
a, b,
s, c
);

input a, b;
output s, c;

reg s, c;

always @(a or b)
begin
	if (a==b) s = 0;
	else s = 1;
	
	if (a == 1 && b == 1) c = 1;
	else c = 0;
end

endmodule
