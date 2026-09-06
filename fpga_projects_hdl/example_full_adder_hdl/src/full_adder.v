`timescale 1ns/1ps
`default_nettype none

// 전가산기: 반가산기 두 개를 연결한다.
module full_adder (
    input wire a,
    input wire b,
    input wire carry_in,
    output wire sum,
    output wire carry_out
);
    wire first_sum, first_carry, second_carry;

    half_adder u_first (
        .a(a),
        .b(b),
        .sum(first_sum),
        .carry(first_carry)
    );

    half_adder u_second (
        .a(first_sum),
        .b(carry_in),
        .sum(sum),
        .carry(second_carry)
    );

    assign carry_out = first_carry | second_carry;
endmodule

`default_nettype wire
