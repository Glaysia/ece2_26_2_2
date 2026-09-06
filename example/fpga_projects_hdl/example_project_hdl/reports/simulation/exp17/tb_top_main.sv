`timescale 1ns/1ps
module tb_top_main;
    reg clk = 0;
    reg rst = 1;
    reg up = 1;
    reg [7:0] key = 8'h80;
    wire [3:0] q, phase, min_tens, min_ones, sec_tens, sec_ones;
    wire o_100, o_50, o_10, o_2, sound;
    wire [7:0] seg_data, seg_com;

    // 실험 번호를 덮어쓰지 않고 top_main에서 선택한 회로를 실행한다.
    top_main dut(
        .clk(clk), .rst(rst), .up(up), .key(key),
        .q(q), .phase(phase),
        .o_100(o_100), .o_50(o_50), .o_10(o_10), .o_2(o_2),
        .sound(sound),
        .min_tens(min_tens), .min_ones(min_ones),
        .sec_tens(sec_tens), .sec_ones(sec_ones),
        .seg_data(seg_data), .seg_com(seg_com));

    // 빠른 논리 관찰용 10ns 클록. 보드의 실제 시간축과 다르다.
    always #5 clk = ~clk;

    initial begin
        $dumpfile("top_main.vcd");
        $dumpvars(0, tb_top_main);
        repeat (2) @(negedge clk);
        rst = 0;
        repeat (5000) @(negedge clk);
        up = 0;
        key = 8'h40;
        repeat (5000) @(negedge clk);
        key = 0;
        repeat (100) @(negedge clk);
        $finish;
    end
endmodule
