// Input clock MUST be the trainer's 1 kHz main clock (B6).
// Mode button N8; reset K4; data DIPSW1..8 = sw[7]..sw[0].
module lab1_integrated #(parameter integer DEBOUNCE_CYCLES=20, LCD_POWER_WAIT=50)(
 input wire clk,rst,mode_button, input wire [7:0] sw,
 output reg [7:0] led, output wire [7:0] seg_data,
 output wire lcd_e,lcd_rs,lcd_rw, output wire [7:0] lcd_data);
 wire press; reg [3:0] mode;
 button_onepulse #(DEBOUNCE_CYCLES) button(clk,rst,mode_button,press);
 always @(posedge clk or posedge rst)
  if(rst) mode<=0;
  else if(press) mode<=(mode==9)?0:mode+1;
 wire gx,gy,gz,fs,fc,ac,borrow,mz;
 wire [3:0] sum,difference;
 wire [2:0] comparison,encoded;
 wire [7:0] demuxed,decoded,hex_segments;
 logic_gate gates(sw[7],sw[6],gx,gy,gz);
 full_adder fa(sw[7],sw[6],sw[5],fs,fc);
 adder_4bit add4(sw[7:4],sw[3:0],sum,ac);
 sub_4bit sub4(sw[7:4],sw[3:0],difference,borrow);
 compare_4 comp(sw[7:4],sw[3:0],comparison);
 mux_4x1 mux(sw[7:4],sw[1:0],mz);
 demux_1x8 demux(sw[7],sw[2:0],demuxed);
 encoder8x3 encoder(sw,encoded);
 decoder3x8 decoder(sw[2],sw[1],sw[0],decoded);
 seg_decoder seven(sw[3:0],hex_segments);
 assign seg_data=(mode==9)?hex_segments:8'b0;
 always @* begin
  led=0;
  case(mode)
   0:led={gx,gy,gz,5'b0};
   1:led={fc,fs,6'b0};
   2:led={ac,sum,3'b0};
   3:led={borrow,difference,3'b0};
   4:led={comparison,5'b0};
   5:led={mz,7'b0};
   6:led=demuxed;
   7:led={encoded,5'b0};
   8:led=decoded;
   9:led=hex_segments;
   default:led=0;
  endcase
 end
 lcd_modes #(LCD_POWER_WAIT) display(clk,rst,mode,lcd_e,lcd_rs,lcd_rw,lcd_data);
endmodule
