`timescale 1ns/1ps
module uart_keypad_test #(
 parameter integer CLK_HZ=50000000, BAUD=9600,
 parameter integer DEBOUNCE=500000, POR_CYCLES=65535
)(input wire clk,uart_rxd,input wire [11:0] keys,
 output wire uart_txd,output wire [7:0] led,
 output wire [15:0] gpio_monitor);
 // BDIO 0..7: FPGA TX; BDIO 8..15: copies of incoming USB UART RX.
 assign gpio_monitor={ {8{uart_rxd}}, {8{uart_txd}} };
 localparam integer DIV=(CLK_HZ+BAUD/2)/BAUD;
 // Configuration initializes this counter; no numeric key doubles as reset.
 reg [31:0] por=0;wire rst=(por<POR_CYCLES);
 always @(posedge clk)if(rst)por<=por+1'b1;
 wire [7:0] rx_data;wire rx_valid,frame_error,tx_ready;
 reg tx_valid;reg [7:0] tx_data;
 uart_rx #(.DIV(DIV)) receiver(clk,rst,uart_rxd,rx_data,rx_valid,frame_error);
 uart_tx #(.DIV(DIV)) transmitter(clk,rst,tx_valid,tx_data,tx_ready,uart_txd);

 (* ASYNC_REG="TRUE" *) reg [11:0] key_meta,key_sync;
 reg [11:0] accepted,key_event,pending;
 integer debounce[0:11];integer i;
 always @(posedge clk)begin
  if(rst)begin key_meta<=0;key_sync<=0;accepted<=0;key_event<=0;
   for(i=0;i<12;i=i+1)debounce[i]<=0;
  end else begin
   key_meta<=keys;key_sync<=key_meta;key_event<=0;
   for(i=0;i<12;i=i+1)begin
    if(key_sync[i]==accepted[i])debounce[i]<=0;
    else if(debounce[i]==DEBOUNCE-1)begin
     accepted[i]<=key_sync[i];debounce[i]<=0;key_event[i]<=key_sync[i];
    end else debounce[i]<=debounce[i]+1;
   end
  end
 end
 // RX FIFO permits subsequent lines to arrive while the prior reply transmits.
 reg [7:0] fifo[0:2047];reg [10:0] wr,rd;
 wire [10:0] next_wr=wr+11'd1;
 reg rx_overflow,framing_seen;reg [7:0] last_rx;
 always @(posedge clk)begin
  if(rst)begin wr<=0;rx_overflow<=0;framing_seen<=0;last_rx<=0;end
  else begin
   if(frame_error)framing_seen<=1;
   if(rx_valid)begin
    last_rx<=rx_data;
    if(next_wr==rd)rx_overflow<=1;
    else begin fifo[wr]<=rx_data;wr<=next_wr;end
   end
  end
 end
 reg [7:0] line[0:127];reg [7:0] length,pos;
 reg too_long;reg [2:0] state;reg [4:0] prefix_pos;
 reg [7:0] key_char;
 localparam COLLECT=0,PREFIX=1,BODY=2,LF=3,KEYMSG=4,ERRORMSG=5;
 wire [143:0] error_text="ERR|LINE_TOO_LONG\n";
 reg [11:0] consume;reg [7:0] chosen;
 integer k;
 always @*begin
  consume=0;chosen=0;
  // Lowest numbered physical position has priority; all other bits remain queued.
  for(k=11;k>=0;k=k-1)if(pending[k])begin
   consume=12'b1<<k;
   if(k<9)chosen=8'h31+k;
   else if(k==9)chosen="*";else if(k==10)chosen="0";else chosen="#";
  end
  tx_valid=(state!=COLLECT);tx_data=10;
  case(state)
   PREFIX:case(prefix_pos)0:tx_data="L";1:tx_data="B";default:tx_data="|";endcase
   BODY:tx_data=line[pos];
   KEYMSG:case(prefix_pos)0:tx_data="K";1:tx_data="P";2:tx_data="|";3:tx_data=key_char;default:tx_data=10;endcase
   ERRORMSG:tx_data=error_text[143-prefix_pos*8 -: 8];
   default:tx_data=10;
  endcase
 end
 always @(posedge clk)begin
  if(rst)begin rd<=0;length<=0;pos<=0;too_long<=0;state<=COLLECT;prefix_pos<=0;key_char<=0;pending<=0;end
  else begin
   pending<=pending|key_event;
   case(state)
    COLLECT:begin
     if(wr!=rd)begin
      rd<=rd+1'b1;
      if(fifo[rd]==10)begin prefix_pos<=0;pos<=0;state<=too_long?ERRORMSG:PREFIX;end
      else if(fifo[rd]!=13)begin
       if(length<128)begin line[length]<=fifo[rd];length<=length+1'b1;end
       else too_long<=1;
      end
     end else if(pending!=0)begin
      pending<=(pending&~consume)|key_event;key_char<=chosen;prefix_pos<=0;state<=KEYMSG;
     end
    end
    PREFIX:if(tx_ready)begin
     if(prefix_pos==2)begin pos<=0;state<=(length==0)?LF:BODY;end
     else prefix_pos<=prefix_pos+1'b1;
    end
    BODY:if(tx_ready)begin if(pos==length-1)state<=LF;else pos<=pos+1'b1;end
    LF:if(tx_ready)begin length<=0;too_long<=0;state<=COLLECT;end
    KEYMSG:if(tx_ready)begin if(prefix_pos==4)state<=COLLECT;else prefix_pos<=prefix_pos+1'b1;end
    ERRORMSG:if(tx_ready)begin
     if(prefix_pos==17)begin length<=0;too_long<=0;state<=COLLECT;end
     else prefix_pos<=prefix_pos+1'b1;
    end
    default:state<=COLLECT;
   endcase
  end
 end
 assign led={rx_overflow,framing_seen,~rst,~tx_ready,last_rx[3:0]};
endmodule
