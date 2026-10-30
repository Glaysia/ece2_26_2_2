
module piano ( clk, rst, key, piezo );

input clk, rst;  // clock 1MHz
input [7:0] key;

output piezo;

reg piezo;

parameter do =12'd3830;  // 261 Hz 
parameter rae =12'd3400;    // 294 Hz 
parameter mi =12'd3038;    // 329 Hz 
parameter fa =12'd2864;    // 349 Hz 
parameter sol =12'd2550;    // 392 Hz 
parameter la =12'd2272;    // 440 Hz 
parameter ti =12'd2028;    // 493 Hz 
parameter high_do =12'd1912;    // 523 Hz 

reg [11:0] cnt;

reg [11:0] cnt_limit;


always @(key)
	if (rst) cnt_limit = 0;
	else
		case(key)
			8'h80 : cnt_limit = do;
			8'h40 : cnt_limit = rae;
			8'h20 : cnt_limit = mi;
			8'h10 : cnt_limit = fa;
			8'h08 : cnt_limit = sol;
			8'h04 : cnt_limit = la;
			8'h02 : cnt_limit = ti;
			8'h01 : cnt_limit = high_do;
			default : cnt_limit = 0;
		endcase
	
always @(posedge clk)
	if (rst)	cnt = 0; 
	else if (cnt >= cnt_limit/2) 
		begin
			piezo = !piezo;
			cnt = 0;
		end
	else
		cnt = cnt + 1;


endmodule
	


