
module led_pwm (clk, rst, sw, led);

input clk, rst;  // clock 1kHz
input sw;

output [7:0] led;

reg [3:0] cnt;
reg [3:0] cnt_disp;
reg reg_led;


always @(posedge rst or posedge sw)
	if (rst) cnt = 0;
	else if (cnt >= 9) cnt = 0;
	else cnt = cnt + 1;

always @(posedge clk)
	if (rst) cnt_disp = 0;
	else if (cnt_disp >= 9) cnt_disp = 0;
	else cnt_disp = cnt_disp + 1;

always @(posedge clk)
	if (rst) reg_led = 0;
	else if (cnt_disp >= cnt) reg_led = 0;
	else reg_led = 1;

assign led = {reg_led, reg_led, reg_led, reg_led, 
				reg_led, reg_led, reg_led, reg_led};

endmodule


