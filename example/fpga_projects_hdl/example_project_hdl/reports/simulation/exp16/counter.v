`timescale 1ns/1ps
module lab5_counter(input wire clk, rst, up, output reg [3:0] q);
    // up=1: 증가, up=0: 감소. 4비트 범위를 넘으면 순환한다.
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else if (up) q <= q + 1'b1;
        else q <= q - 1'b1;
    end
endmodule
