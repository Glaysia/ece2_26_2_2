
module rgb_pwm (clk, rst, sw_r, sw_g, sw_b, led_r, led_g, led_b);

input clk, rst;  // clock 1kHz
input sw_r, sw_g, sw_b;

output [3:0] led_r;
output [3:0] led_g;
output [3:0] led_b;

reg [3:0] cnt_r;
reg [3:0] cnt_g;
reg [3:0] cnt_b;

reg [3:0] cnt_disp;

reg reg_r, reg_g, reg_b;


// rgb duty rate set

always @(posedge rst or posedge sw_r)
	if (rst) cnt_r = 0;
	else if (cnt_r >= 9) cnt_r = 0;
	else cnt_r = cnt_r + 1;

always @(posedge rst or posedge sw_g)
	if (rst) cnt_g = 0;
	else if (cnt_g >= 9) cnt_g = 0;
	else cnt_g = cnt_g + 1;

always @(posedge rst or posedge sw_b)
	if (rst) cnt_b = 0;
	else if (cnt_b >= 9) cnt_b = 0;
	else cnt_b = cnt_b + 1;

// rgb display

always @(posedge clk)
	if (rst) cnt_disp = 0;
	else if (cnt_disp >= 9) cnt_disp = 0;
	else cnt_disp = cnt_disp + 1;

always @(posedge clk)
	if (rst) reg_r = 0;
	else if (cnt_disp >= cnt_r) reg_r = 0;
	else reg_r = 1;

assign led_r = {reg_r, reg_r, reg_r, reg_r};

always @(posedge clk)
	if (rst) reg_g = 0;
	else if (cnt_disp >= cnt_g) reg_g = 0;
	else reg_g = 1;

assign led_g = {reg_g, reg_g, reg_g, reg_g};

always @(posedge clk)
	if (rst) reg_b = 0;
	else if (cnt_disp >= cnt_b) reg_b = 0;
	else reg_b = 1;

assign led_b = {reg_b, reg_b, reg_b, reg_b};

endmodule


