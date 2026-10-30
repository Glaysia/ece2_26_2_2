
module not_gate(
a, z
);

input a;
output z;

reg z;

always @(a)
if (a) z = 1'b0;
else   z = 1'b1;

endmodule
