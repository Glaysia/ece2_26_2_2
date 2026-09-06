`timescale 1us/1ns

module tb_toplevel;
  reg clk;
  reg rst;
  wire sum;
  wire cout;

  toplevel dut (
    .clk(clk),
    .rst(rst),
    .sum(sum),
    .cout(cout)
  );

  // 주기 25us인 클럭: 12.5us마다 0과 1을 반복
  always #12.5 clk = ~clk;

  initial begin
    $dumpfile("toplevel.vcd");
    $dumpvars(0, tb_toplevel);
    $monitor("time=%0t clk=%b rst=%b sum=%b cout=%b", $time, clk, rst, sum, cout);

    clk = 1'b0;
    rst = 1'b1;

    // 첫 번째 주기 동안 reset을 걸어 둠
    #25 rst = 1'b0;

    // 25us x 20주기 = 500us 후 시뮬레이션 종료
    #475;
    $finish;
  end
endmodule
