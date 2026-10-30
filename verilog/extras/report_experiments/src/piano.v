`timescale 1ns/1ps
module lab5_piano #(parameter integer CLK_HZ = 1000000)(
    input wire clk, rst,
    input wire [7:0] key,
    output wire sound
);
    reg [31:0] half_period;
    // 원본처럼 key[7]부터 도레미파솔라시도. 무입력/동시 입력은 무음.
    always @* begin
        case (key)
            8'h80: half_period = (CLK_HZ + 262) / (2 * 262);
            8'h40: half_period = (CLK_HZ + 294) / (2 * 294);
            8'h20: half_period = (CLK_HZ + 330) / (2 * 330);
            8'h10: half_period = (CLK_HZ + 349) / (2 * 349);
            8'h08: half_period = (CLK_HZ + 392) / (2 * 392);
            8'h04: half_period = (CLK_HZ + 440) / (2 * 440);
            8'h02: half_period = (CLK_HZ + 494) / (2 * 494);
            8'h01: half_period = (CLK_HZ + 523) / (2 * 523);
            default: half_period = 0;
        endcase
    end
    lab5_tone tone(clk, rst, half_period != 0, half_period, sound);
endmodule
