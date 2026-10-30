`timescale 1ns/1ps
module tb_uart_keypad;
 reg clk=0,rx=1;reg [11:0] keys=0;wire tx;wire [7:0] led;wire [15:0] gpio;
 always #5 clk=~clk;
 localparam D=16;
 uart_keypad_test #(.CLK_HZ(1600000),.BAUD(100000),.DEBOUNCE(8),.POR_CYCLES(8)) dut(clk,rx,keys,tx,led,gpio);
 // Sample after continuous assignments settle, away from stimulus delta cycles.
 always @(negedge clk) begin #1; if(!dut.rst) begin
  if(gpio!=={{8{rx}},{8{tx}}})$fatal(1,"16-pin GPIO UART mirror mismatch");
 end end
 reg [7:0] received[0:2047];integer count=0,j,n,base;
 reg [7:0] octet;
 // Independent wire decoder checks start/data/stop at bit centers.
 initial forever begin
  @(negedge tx); #(D*10/2);
  if(tx!==0)$fatal(1,"bad TX start");
  for(j=0;j<8;j=j+1)begin #(D*10);octet[j]=tx;end
  #(D*10);if(tx!==1)$fatal(1,"bad TX stop");
  received[count]=octet;count=count+1;
 end
 task send_byte(input [7:0] b);
  integer k;begin
   @(negedge clk);rx=0;repeat(D)@(negedge clk);
   for(k=0;k<8;k=k+1)begin rx=b[k];repeat(D)@(negedge clk);end
   rx=1;repeat(D)@(negedge clk);
  end
 endtask
 task send_text(input string s);integer k;begin for(k=0;k<s.len();k=k+1)send_byte(s[k]);end endtask
 task expect_text(input string s);integer k,start;begin
  start=base;
  wait(count>=start+s.len());repeat(20)@(negedge clk);
  for(k=0;k<s.len();k=k+1)if(received[start+k]!==s[k])$fatal(1,"byte %0d got %h expected %h",start+k,received[start+k],s[k]);
  base=start+s.len();
 end endtask
 initial begin
  base=0;repeat(20)@(negedge clk);
  send_text("BLABLA");repeat(100)@(negedge clk);if(count!=0)$fatal(1,"reply before LF");
  send_byte(10);expect_text("LB|BLABLA\n");
  send_text("\nA");send_byte(13);send_text("\nB\n");expect_text("LB|\nLB|A\nLB|B\n");
  // One event per stable press, no repeats while held.
  keys[0]=1;expect_text("KP|1\n");repeat(1000)@(negedge clk);
  if(count!=base)$fatal(1,"held key repeated");
  keys=0;repeat(20)@(negedge clk);
  for(n=1;n<12;n=n+1)begin
   keys=12'b1<<n;
   if(n<9)expect_text($sformatf("KP|%0d\n",n+1));
   else if(n==9)expect_text("KP|*\n");else if(n==10)expect_text("KP|0\n");else expect_text("KP|#\n");
   keys=0;repeat(20)@(negedge clk);
  end
  // Bounce shorter than debounce must not emit a key.
  keys=1;repeat(3)@(negedge clk);keys=0;repeat(40)@(negedge clk);
  if(count!=base)$fatal(1,"bounce emitted key");
  for(n=0;n<128;n=n+1)send_byte("x");send_byte(10);
  expect_text("LB|");for(n=0;n<128;n=n+1)expect_text("x");expect_text("\n");
  for(n=0;n<129;n=n+1)send_byte("y");send_byte(10);expect_text("ERR|LINE_TOO_LONG\n");
  send_text("OK\n");expect_text("LB|OK\n");
  if(led[7:6]!=0)$fatal(1,"UART error flags");
  $display("UART_KEYPAD_PASS bytes=%0d LF CRLF empty burst 12keys hold bounce length overflow recovery GPIO16",count);$finish;
 end
 initial begin #20000000;$fatal(1,"timeout");end
endmodule
