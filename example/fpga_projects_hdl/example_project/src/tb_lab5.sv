`timescale 1ns/1ps
module tb_lab5;
    reg clk = 0;
    reg rst = 1;
    reg up = 1;
    reg [7:0] key = 0;
    wire [3:0] q, phase, mt, mo, st, so;
    wire o100, o50, o10, o2, piezo, piano;
    wire [7:0] seg, common;
    integer i, expected, second, note, j;
    integer periods [0:7];
    lab5_counter counter(clk, rst, up, q);
    lab5_clock_divider divider(clk, rst, o100, o50, o10, o2);
    lab5_stepper motor(clk, rst, phase);
    lab5_piezo piezo_dut(clk, rst, piezo);
    lab5_piano piano_dut(clk, rst, key, piano);
    // 가상 1초를 4클록으로 줄여 시계의 자리올림을 빠르게 검사한다.
    lab5_watch #(.CLK_HZ(4)) watch_dut(clk, rst, mt, mo, st, so, seg, common);
    always #5 clk = ~clk;

    task tick;
        begin @(posedge clk); #1; end
    endtask
    task reset_all;
        begin
            @(negedge clk); rst = 1;
            tick;
            if (q !== 0 || phase !== 4'b0011 || piezo !== 0 || piano !== 0)
                $fatal(1, "reset mismatch");
            if ({mt,mo,st,so} !== 16'h0000) $fatal(1, "watch reset");
            @(negedge clk); rst = 0;
        end
    endtask

    initial begin
        $dumpfile("lab5.vcd");
        $dumpvars(0, tb_lab5);
        reset_all;
        for (i = 1; i <= 100; i = i + 1) begin
            tick;
            if (q !== (i % 16)) $fatal(1, "up counter: %0d", i);
            if (o50 !== (i % 2) || o10 !== ((i / 5) % 2) ||
                o2 !== ((i / 25) % 2)) $fatal(1, "divider: %0d", i);
            case (i % 4)
                0: expected = 3;
                1: expected = 6;
                2: expected = 12;
                3: expected = 9;
            endcase
            if (phase !== expected) $fatal(1, "stepper: %0d", i);
            @(negedge clk); #1;
            if (o100 !== 0) $fatal(1, "clock passthrough");
        end
        up = 0;
        expected = 4;
        repeat (20) begin
            tick;
            expected = (expected + 15) % 16;
            if (q !== expected) $fatal(1, "down counter");
        end
        $display("PASS counter, divider, stepper");

        reset_all;
        for (i = 1; i <= 6804; i = i + 1) begin
            tick;
            if (piezo !== ((i / 1701) % 2)) $fatal(1, "piezo period");
        end
        periods[0]=1908; periods[1]=1701; periods[2]=1515; periods[3]=1433;
        periods[4]=1276; periods[5]=1136; periods[6]=1012; periods[7]=956;
        for (note = 0; note < 8; note = note + 1) begin
            reset_all;
            key = 8'h80 >> note;
            for (j = 1; j <= periods[note]*2; j = j + 1) begin
                tick;
                if (piano !== ((j / periods[note]) % 2))
                    $fatal(1, "piano note %0d cycle %0d", note, j);
            end
            @(negedge clk); key = 0; tick;
            if (piano !== 0) $fatal(1, "key release");
        end
        @(negedge clk); key = 8'h81;
        repeat (2000) begin tick; if (piano !== 0) $fatal(1, "multiple keys"); end
        $display("PASS piezo, all eight piano notes, silence");

        reset_all;
        for (second = 1; second <= 3600; second = second + 1) begin
            repeat (4) tick;
            expected = second % 3600;
            if (mt !== (expected / 600) || mo !== ((expected / 60) % 10) ||
                st !== ((expected % 60) / 10) || so !== (expected % 10))
                $fatal(1, "watch second %0d", second);
        end
        if (seg !== 8'hfc) $fatal(1, "zero segment pattern");
        repeat (4) begin
            tick;
            if (common !== 8'hf7 && common !== 8'hfb &&
                common !== 8'hfd && common !== 8'hfe) $fatal(1, "scan select");
        end
        reset_all;
        $display("PASS watch 00:00 through 59:59 and rollover; reset");
        $display("ALL LAB5 CHECKS PASSED");
        $finish;
    end
    initial begin #2000000; $fatal(1, "timeout"); end
endmodule
