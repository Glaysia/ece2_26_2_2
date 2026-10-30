`timescale 10ns / 10ps

module testbench();
// input
reg i, clk;
// output
wire [3:0] o;
// Instantiate the U1
shift_register u1(i, clk, o);
// Specify input stimulus
initial begin
    i = 0; clk = 0;

    #10 i = 1;
    #30	i = 0;
    #20 i = 1;
    #30	i = 0;
end

always #5 clk = ~clk;
// 10MHz
endmodule

