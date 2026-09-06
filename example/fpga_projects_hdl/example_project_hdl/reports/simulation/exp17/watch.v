`timescale 1ns/1ps
module lab5_watch #(parameter integer CLK_HZ = 1000)(
    input wire clk, rst,
    output reg [3:0] min_tens, min_ones, sec_tens, sec_ones,
    output reg [7:0] seg_data, seg_com
);
    reg [31:0] count;
    reg [1:0] scan;
    reg [3:0] digit;
    // 한 클록만 사용한다. CLK_HZ번마다 1초를 증가시킨다.
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= 0; scan <= 0;
            min_tens <= 0; min_ones <= 0; sec_tens <= 0; sec_ones <= 0;
        end else begin
            scan <= scan + 1'b1;
            if (count == CLK_HZ - 1) begin
                count <= 0;
                if (sec_ones == 9) begin
                    sec_ones <= 0;
                    if (sec_tens == 5) begin
                        sec_tens <= 0;
                        if (min_ones == 9) begin
                            min_ones <= 0;
                            if (min_tens == 5) min_tens <= 0;
                            else min_tens <= min_tens + 1'b1;
                        end else min_ones <= min_ones + 1'b1;
                    end else sec_tens <= sec_tens + 1'b1;
                end else sec_ones <= sec_ones + 1'b1;
            end else count <= count + 1'b1;
        end
    end
    // 자리 선택은 active-low, 세그먼트는 {a,b,c,d,e,f,g,dp}, active-high.
    always @* begin
        case (scan)
            0: begin seg_com = 8'hf7; digit = min_tens; end
            1: begin seg_com = 8'hfb; digit = min_ones; end
            2: begin seg_com = 8'hfd; digit = sec_tens; end
            3: begin seg_com = 8'hfe; digit = sec_ones; end
            default: begin seg_com = 8'hff; digit = 0; end
        endcase
        case (digit)
            0: seg_data = 8'hfc;
            1: seg_data = 8'h60;
            2: seg_data = 8'hda;
            3: seg_data = 8'hf2;
            4: seg_data = 8'h66;
            5: seg_data = 8'hb6;
            6: seg_data = 8'hbe;
            7: seg_data = 8'he0;
            8: seg_data = 8'hfe;
            9: seg_data = 8'hf6;
            default: seg_data = 0;
        endcase
        if (rst) begin seg_com = 8'hff; seg_data = 0; end
    end
endmodule
