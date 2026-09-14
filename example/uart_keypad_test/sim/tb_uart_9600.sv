`timescale 1ns/1ps
module tb_uart_9600;
 reg clk=0,rx=1;wire tx;wire [7:0] led;wire [15:0] gpio;
 always #10 clk=~clk;
 uart_keypad_test dut(clk,rx,12'b0,tx,led,gpio);
 localparam BIT_NS=104167;
 reg [7:0] expected[0:4];reg [7:0] octet;
 integer n,k;
 task send_byte(input [7:0] b);integer j;begin
  rx=0;#BIT_NS;
  for(j=0;j<8;j=j+1)begin rx=b[j];#BIT_NS;end
  rx=1;#BIT_NS;
 end endtask
 initial begin
  expected[0]="L";expected[1]="B";expected[2]="|";expected[3]="U";expected[4]=10;
  for(n=0;n<5;n=n+1)begin
   @(negedge tx);#(BIT_NS/2);
   if(tx!==0)$fatal(1,"start");
   for(k=0;k<8;k=k+1)begin #BIT_NS;octet[k]=tx;end
   #BIT_NS;if(tx!==1 || octet!==expected[n])$fatal(1,"9600 response byte %0d",n);
  end
  $display("UART_9600_PASS 50MHz default parameters, independent 9600 wire stimulus/decoder, LB|U LF");$finish;
 end
 initial begin #2000000;send_byte("U");send_byte(10);end
 initial begin #20000000;$fatal(1,"9600 timeout");end
endmodule
