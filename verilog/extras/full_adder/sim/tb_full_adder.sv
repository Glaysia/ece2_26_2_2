`timescale 1ns/1ps
`default_nettype none

module tb_full_adder;
    reg a, b, carry_in;
    wire sum, carry_out;
    reg [1:0] expected;
    integer vector_index;

    full_adder dut (
        .a(a), .b(b), .carry_in(carry_in),
        .sum(sum), .carry_out(carry_out)
    );

    initial begin
        $dumpfile("full_adder.vcd");
        $dumpvars(0, tb_full_adder);
        // Each of the eight input vectors is held for 10 ns.
        for (vector_index = 0; vector_index < 8; vector_index = vector_index + 1) begin
            {a, b, carry_in} = vector_index[2:0];
            expected = {1'b0, a} + {1'b0, b} + {1'b0, carry_in};
            #1;
            if ({carry_out, sum} !== expected)
                $fatal(1, "FAIL: input=%b%b%b expected=%b actual=%b%b",
                       a, b, carry_in, expected, carry_out, sum);
            $display("PASS: input=%b%b%b carry_out=%b sum=%b",
                     a, b, carry_in, carry_out, sum);
            #9;
        end
        $display("PASS: all 8 full-adder input combinations");
        $finish;
    end
endmodule

`default_nettype wire
