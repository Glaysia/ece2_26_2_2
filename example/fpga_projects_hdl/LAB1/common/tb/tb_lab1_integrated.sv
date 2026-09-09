`timescale 1ns/1ps
module tb_lab1_integrated;
 reg clk=0,rst=1,mode_button=0; reg [7:0] sw=0;
 wire [7:0] led,seg_data,lcd_data; wire lcd_e,lcd_rs,lcd_rw;
 lab1_integrated #(.DEBOUNCE_CYCLES(4),.LCD_POWER_WAIT(5)) dut(.*);
 always #5 clk=~clk;
 integer checked=0,m,n,k,v,frames=0,addr=0;
 reg [7:0] expected,expected_seg;
 reg [127:0] line1,line2,expected_name,completed_line1,completed_line2;
 reg [55:0] expected_heading;
 integer init_count=0;
 reg [7:0] init_words[0:4];
 reg [7:0] digits[0:15];
 task cycles(input integer amount);
  repeat(amount) @(negedge clk);
 endtask
 task assert_mode(input integer value);
  if(dut.mode!==value) $fatal(1,"Mode expected %0d actual %0d",value,dut.mode);
 endtask
 task press_once;
  mode_button=1; cycles(12); mode_button=0; cycles(12);
 endtask
 // Decode the actual external LCD bus at E falling edge.
 always @(negedge lcd_e) if(!rst) begin
  if(lcd_rw!==0) $fatal(1,"LCD must write only");
  if(!lcd_rs) begin
   if(init_count<5) begin
    if(lcd_data!==init_words[init_count]) $fatal(1,"LCD initialization command %0d got %h",init_count,lcd_data);
    init_count=init_count+1;
   end
   if(lcd_data==8'h80) begin addr=0;line1=0;end
   else if(lcd_data==8'hc0) begin addr=64;line2=0;end
  end else begin
   if(addr<16) line1[127-addr*8 -: 8]=lcd_data;
   if(addr>=64 && addr<80) line2[127-(addr-64)*8 -: 8]=lcd_data;
   if(addr==79) begin
    completed_line1=line1;completed_line2=line2;frames=frames+1;
   end
   addr=addr+1;
  end
 end
 initial begin
  init_words[0]=8'h38;init_words[1]=8'h38;init_words[2]=8'h38;init_words[3]=8'h0c;init_words[4]=8'h06;
  digits[0]=252;digits[1]=96;digits[2]=218;digits[3]=242;
  digits[4]=102;digits[5]=182;digits[6]=190;digits[7]=224;
  digits[8]=254;digits[9]=246;digits[10]=238;digits[11]=62;
  digits[12]=156;digits[13]=122;digits[14]=158;digits[15]=142;
  $dumpfile("wave.vcd");$dumpvars(0,tb_lab1_integrated);
  cycles(3);rst=0;cycles(12);assert_mode(0);
  // Bounces shorter than four samples must not be accepted.
  repeat(3) begin mode_button=1;cycles(1);mode_button=0;cycles(2);end
  cycles(12);assert_mode(0);
  for(m=0;m<10;m=m+1) begin
   assert_mode(m);
   for(n=0;n<256;n=n+1) begin
    sw=n;cycles(1);expected=0;expected_seg=0;
    case(m)
     0:expected={sw[7]&sw[6],sw[7]|sw[6],sw[7]^sw[6],5'b0};
     1:expected=(int'(sw[7])+int'(sw[6])+int'(sw[5]))<<6;
     2:expected=((n/16)+(n%16))<<3;
     3:expected=((((n/16)<(n%16))?16:0)|(((n/16)-(n%16))&15))<<3;
     4:expected=(((n/16)>(n%16))?4:(((n/16)==(n%16))?2:1))<<5;
     5:expected=(((n/16)>>(3-(n%4)))&1)<<7;
     6:expected=(n>=128)?(128>>(n%8)):0;
     7:begin for(k=0;k<8;k=k+1)if(n==(128>>k))expected=k<<5;end
     8:expected=1<<(n%8);
     9:begin expected=digits[n%16];expected_seg=expected;end
    endcase
    if(led!==expected || seg_data!==expected_seg)
     $fatal(1,"mode=%0d sw=%h expected LED=%h got=%h",m,sw,expected,led);
    checked=checked+1;
   end
   // Allow two complete 16x2 refreshes, including a mode change midway through a frame.
   cycles(350);
   expected_heading="MODE 00";
   expected_heading[15:8]=(m==9)?8'h31:8'h30;
   expected_heading[7:0]=(m==9)?8'h30:(8'h31+m);
   if(completed_line1[127:72]!==expected_heading || init_count!=5)
    $fatal(1,"LCD mode text mismatch: %s",completed_line1);
   case(m)
    0:expected_name="AND OR XOR      ";1:expected_name="FULL ADDER      ";
    2:expected_name="4 BIT ADDER     ";3:expected_name="4 BIT SUBTRACT  ";
    4:expected_name="4 BIT COMPARE   ";5:expected_name="4 TO 1 MUX      ";
    6:expected_name="1 TO 8 DEMUX    ";7:expected_name="8 TO 3 ENCODER  ";
    8:expected_name="3 TO 8 DECODER  ";9:expected_name="HEX 7 SEGMENT   ";
   endcase
   if(completed_line2!==expected_name)$fatal(1,"LCD circuit text mismatch: %s",completed_line2);
   // A long press advances once and only once.
   mode_button=1;cycles(80);assert_mode((m==9)?0:m+1);
   mode_button=0;cycles(12);
  end
  assert_mode(0);press_once;assert_mode(1);
  init_count=0;rst=1;cycles(3);rst=0;cycles(200);assert_mode(0);
  if(init_count!=5 || completed_line1[127:72]!=="MODE 01")$fatal(1,"LCD reset recovery failed");
  if(checked!=2560 || frames<10)$fatal(1,"Incomplete integrated test");
  $display("LAB1_PASS lab1_integrated cases=%0d",checked);$finish;
 end
 initial begin #1000000;$fatal(1,"Watchdog");end
endmodule
