`timescale 1ns/1ps
module lab5_tone(
    input wire clk, rst, enable,
    input wire [31:0] half_period,
    output reg sound
);
    // 출력 주파수 = 입력 클록 / (2 * half_period)
    reg [31:0] count;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= 0;
            sound <= 0;
        end else if (!enable || half_period == 0) begin
            count <= 0;
            sound <= 0;
        end else if (count >= half_period - 1) begin
            count <= 0;
            sound <= ~sound;
        end else count <= count + 1'b1;
    end
endmodule

module lab5_piezo #(parameter integer CLK_HZ = 1000000)(
    input wire clk, rst,
    output wire sound
);
    // 원본의 고정음 '레': 약 294Hz
    localparam integer HALF_PERIOD = (CLK_HZ + 294) / (2 * 294);
    lab5_tone tone(clk, rst, 1'b1, HALF_PERIOD, sound);
endmodule
