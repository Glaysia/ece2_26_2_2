`timescale 10ns / 100ps

module count_4_tb();

reg rst, clk;
wire [3:0] q;

count_4 u1( rst, clk, q );

initial begin
    clk = 0; rst = 1;
    #10 rst = 0;
end

always begin
    #5 clk = ~clk;
end

endmodule

