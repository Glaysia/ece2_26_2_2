`timescale 1ns/1ps
// External-interface timing check with the actual default 1 kHz parameters.
module tb_board_timing;
  reg clk=0, rst=1, key=0;
  wire pulse, lcd_e, lcd_rs, lcd_rw;
  wire [7:0] lcd_data;
  integer pulses=0, bytes_seen=0, init_seen=0;
  time reset_release, key_press, e_rise, previous_rise=0, bus_change=0;
  reg [7:0] expected_command;
  button_onepulse button(clk,rst,key,pulse);
  lcd_modes lcd(clk,rst,4'd0,lcd_e,lcd_rs,lcd_rw,lcd_data);
  always #500000 clk=~clk; // 1 ms period: the board source is 1 kHz.
  always @(lcd_data or lcd_rs) bus_change=$time;
  always @(posedge pulse) begin
    pulses=pulses+1;
    if($time-key_press<20000000) $fatal(1,"Debounce accepted less than 20 ms");
  end
  always @(posedge lcd_e) if(!rst) begin
    e_rise=$time;
    if(e_rise-reset_release<50000000) $fatal(1,"LCD power wait shorter than 50 ms");
    if(e_rise-bus_change<1000000) $fatal(1,"LCD setup shorter than 1 ms");
    if(previous_rise && e_rise-previous_rise<4000000) $fatal(1,"LCD byte interval shorter than 4 ms");
    if(bytes_seen==1 && e_rise-previous_rise<4100000) $fatal(1,"First function-set recovery too short");
    previous_rise=e_rise;
  end
  always @(negedge lcd_e) if(!rst && previous_rise) begin
    if($time-e_rise!=1000000) $fatal(1,"LCD enable pulse is not 1 ms");
    if(lcd_rw!==0) $fatal(1,"LCD must remain in write mode");
    if(init_seen<5) begin
      case(init_seen)
        0,1,2:expected_command=8'h38;
        3:expected_command=8'h0c;
        4:expected_command=8'h06;
      endcase
      if(lcd_rs!==0 || lcd_data!==expected_command) $fatal(1,"LCD initialization sequence mismatch");
      init_seen=init_seen+1;
    end
    bytes_seen=bytes_seen+1;
  end
  initial begin
    $dumpfile("wave.vcd"); $dumpvars(0,tb_board_timing);
    #2000000; rst=0; reset_release=$time;
    key_press=$time; key=1; #2000000; key=0;
    #30000000; if(pulses!=0) $fatal(1,"Short bounce generated a pulse");
    key_press=$time; key=1; #100000000;
    if(pulses!=1) $fatal(1,"Long press should generate exactly one pulse");
    key=0; #30000000;
    key_press=$time; key=1; #30000000; key=0;
    #300000000;
    if(pulses!=2 || init_seen!=5 || bytes_seen<39) $fatal(1,"Incomplete timing check");
    $display("LAB1_TIMING_PASS clock=1kHz pulses=%0d lcd_bytes=%0d",pulses,bytes_seen);
    $finish;
  end
  initial begin #1000000000; $fatal(1,"Timing watchdog"); end
endmodule
