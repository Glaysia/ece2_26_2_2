`timescale 10ns / 10ps

module testbench();

reg rst, x;
// 입력

wire [1:0] y;
// 출력

mealy u1(rst, x, y);

initial begin
    rst = 1; x = 0;
    #10 rst = 0;
end

always #5 x = ~x;

endmodule

