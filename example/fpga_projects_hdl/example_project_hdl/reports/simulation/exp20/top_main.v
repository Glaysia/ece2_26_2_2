`timescale 1ns/1ps
module top_main #(
    // 아래 EXPERIMENT 선언 중 하나만 주석 해제한다.
    parameter integer EXPERIMENT = 20,
    // parameter integer EXPERIMENT = 17,
    // parameter integer EXPERIMENT = 18,
    // parameter integer EXPERIMENT = 19,
    // parameter integer EXPERIMENT = 20,
    // parameter integer EXPERIMENT = 21,
    parameter integer TONE_CLK_HZ = 1000000,
    parameter integer WATCH_CLK_HZ = 1000
) (
    input wire clk, rst, up,
    input wire [7:0] key,
    output wire [3:0] q, phase,
    output wire o_100, o_50, o_10, o_2,
    output wire sound,
    output wire [3:0] min_tens, min_ones, sec_tens, sec_ones,
    output wire [7:0] seg_data, seg_com
);
    // clk의 실제 주파수와 XDC는 선택한 실험에 맞춰야 한다.
    // 선택하지 않은 회로는 생성하지 않고 출력만 고정한다.
    generate
        if (EXPERIMENT == 16) begin : counter
            lab5_counter circuit(.clk(clk), .rst(rst), .up(up), .q(q));
        end else begin : no_counter
            assign q = 4'b0000;
        end

        if (EXPERIMENT == 17) begin : divider
            lab5_clock_divider circuit(
                .clk(clk), .rst(rst), .o_100(o_100),
                .o_50(o_50), .o_10(o_10), .o_2(o_2));
        end else begin : no_divider
            assign {o_100, o_50, o_10, o_2} = 4'b0000;
        end

        if (EXPERIMENT == 18) begin : stepper
            lab5_stepper circuit(.clk(clk), .rst(rst), .phase(phase));
        end else begin : no_stepper
            assign phase = 4'b0000;
        end

        if (EXPERIMENT == 19) begin : piezo
            lab5_piezo #(.CLK_HZ(TONE_CLK_HZ)) circuit(
                .clk(clk), .rst(rst), .sound(sound));
        end else if (EXPERIMENT == 20) begin : piano
            lab5_piano #(.CLK_HZ(TONE_CLK_HZ)) circuit(
                .clk(clk), .rst(rst), .key(key), .sound(sound));
        end else begin : no_sound
            assign sound = 1'b0;
        end

        if (EXPERIMENT == 21) begin : watch
            lab5_watch #(.CLK_HZ(WATCH_CLK_HZ)) circuit(
                .clk(clk), .rst(rst),
                .min_tens(min_tens), .min_ones(min_ones),
                .sec_tens(sec_tens), .sec_ones(sec_ones),
                .seg_data(seg_data), .seg_com(seg_com));
        end else begin : no_watch
            assign {min_tens, min_ones, sec_tens, sec_ones} = 16'h0000;
            assign seg_data = 8'h00;
            assign seg_com = 8'hff;
        end
    endgenerate
endmodule

