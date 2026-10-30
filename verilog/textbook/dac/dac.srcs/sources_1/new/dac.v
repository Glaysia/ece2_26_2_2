module dac (rst, clk, add_sel, dac_csn, dac_ldacn, dac_wen, dac_a_b, dac_d, led_out);

input rst, clk, add_sel;
output dac_csn, dac_ldacn, dac_wen, dac_a_b;
output [7:0] dac_d, led_out;

wire dac_csn, dac_ldacn, dac_a_b;
reg dac_wen;
wire [7:0] dac_d, led_out;

integer dac_cnt;
reg [1:0] reg_sw_wr;
integer cnt;
reg clk_cnt;

always @(posedge rst or posedge clk)
	if (rst) 
		begin
			cnt = 0;
			clk_cnt <= 0;
		end
	else
		if (cnt >= 99) 
			begin
				cnt = 0;
				clk_cnt <= ! clk_cnt;
			end
		else
			cnt = cnt + 1;

always @(posedge rst or posedge clk)
	if (rst)	reg_sw_wr = 0;
	else		reg_sw_wr = {reg_sw_wr[0], clk_cnt};

always @(posedge rst or posedge clk)
	if (rst) 
		begin
			dac_cnt = 0;
			dac_wen = 1;
		end
	else
		begin
			if (reg_sw_wr == 2'b01)	
				if (dac_cnt >= 255) dac_cnt = 0;
				else				dac_cnt = dac_cnt + 1;
			
			if (reg_sw_wr == 2'b10) dac_wen = 0;
			else					dac_wen = 1;
		end

assign dac_csn = 0;
assign dac_ldacn = 0;
assign dac_a_b = add_sel;
assign dac_d = dac_cnt;
assign led_out = dac_cnt;
		
endmodule
		
