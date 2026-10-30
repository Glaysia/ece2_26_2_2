`timescale 1ns/1ps
module lab5_stepper(input wire clk, rst, output reg [3:0] phase);
    // 원본의 2상 여자 순서. 실제 모터에는 별도의 구동 회로가 필요하다.
    reg [1:0] state;
    always @(posedge clk or posedge rst) begin
        if (rst) state <= 0;
        else state <= state + 1'b1;
    end
    always @* begin
        case (state)
            0: phase = 4'b0011;
            1: phase = 4'b0110;
            2: phase = 4'b1100;
            3: phase = 4'b1001;
            default: phase = 4'b0000;
        endcase
    end
endmodule
