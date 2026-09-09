
module logic_gate(
 a, b, x, y, z
);

input a,b;
output x,y,z;

wire x, y, z;

// and gate
assign x = a & b;
// or gate
assign y = a | b;
// xor gate
assign z = a ^ b;

endmodule
