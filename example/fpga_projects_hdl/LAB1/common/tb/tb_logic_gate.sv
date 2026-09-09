`timescale 10ns/100ps
module tb_logic_gate;
    reg a, b;
    wire x, y, z;
    integer checked = 0;
    logic_gate dut (.a(a), .b(b), .x(x), .y(y), .z(z));

    task check(input [2:0] expected);
        begin
            if ({x, y, z} !== expected)
                $fatal(1, "FAIL: a=%b b=%b xyz=%b expected=%b",
                       a, b, {x, y, z}, expected);
            checked = checked + 1;
            $display("PASS: t=%0t a=%b b=%b x=%b y=%b z=%b",
                     $time, a, b, x, y, z);
        end
    endtask

    initial begin
        $timeformat(-9, 0, " ns", 0);
        $dumpfile("logic_gate.vcd");
        $dumpvars(0, tb_logic_gate);
        // Same stimulus order and 200 ns intervals as the legacy manual.
        a = 0; b = 0; #20; check(3'b000);
        a = 1; b = 0; #20; check(3'b011);
        a = 0; b = 1; #20; check(3'b011);
        a = 1; b = 1; #20; check(3'b110);
        if (checked != 4) $fatal(1, "FAIL: incomplete test");
        $display("PASS: all 4 logic-gate input combinations");
        $finish;
    end
endmodule
