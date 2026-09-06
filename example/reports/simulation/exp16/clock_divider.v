`timescale 1ns/1ps
module lab5_clock_divider(
    input wire clk, rst,
    output wire o_100,
    output reg o_50, o_10, o_2
);
    // 입력 100Hz 기준. 출력은 관찰용이며 다른 회로의 클록으로 쓰지 않는다.
    reg [2:0] count_10;
    reg [4:0] count_2;
    assign o_100 = rst ? 1'b0 : clk;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            o_50 <= 0; o_10 <= 0; o_2 <= 0;
            count_10 <= 0; count_2 <= 0;
        end else begin
            o_50 <= ~o_50;
            if (count_10 == 4) begin
                count_10 <= 0;
                o_10 <= ~o_10;
            end else count_10 <= count_10 + 1'b1;
            if (count_2 == 24) begin
                count_2 <= 0;
                o_2 <= ~o_2;
            end else count_2 <= count_2 + 1'b1;
        end
    end
endmodule
