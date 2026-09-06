`timescale 1ns/1ps
`default_nettype none

// 반가산기: 두 입력을 더해 합과 자리올림을 만든다.
module half_adder (
    input wire a,
    input wire b,
    output wire sum,
    output wire carry
);
    assign sum = a ^ b;
    assign carry = a & b;
endmodule

`default_nettype wire
