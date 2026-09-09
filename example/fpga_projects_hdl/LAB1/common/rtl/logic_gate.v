module logic_gate (
    input  wire a,
    input  wire b,
    output wire x,
    output wire y,
    output wire z
);
    assign x = a & b;  // AND
    assign y = a | b;  // OR
    assign z = a ^ b;  // XOR
endmodule
