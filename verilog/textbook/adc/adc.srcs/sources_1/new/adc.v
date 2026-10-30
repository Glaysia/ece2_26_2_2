module adc (rst, clk, add_sel, adc_sclk, adc_ncs, adc_din, adc_dout, led_out);

input rst, clk;
input [2:0] add_sel;
output adc_sclk, adc_ncs, adc_din;
input adc_dout;
output [7:0] led_out;

wire adc_sclk, adc_ncs;
reg adc_din;
wire [7:0] led_out;

reg [1:0] clk_cnt;
reg sclk;
wire rclk;
reg cs;
reg [15:0] out_buf;

integer cs_cnt;

always @(posedge rst or posedge clk)
	if (rst) clk_cnt = 0;
	else clk_cnt = clk_cnt + 1;
	
assign rclk = clk_cnt[1];

always @(posedge rst or posedge rclk)
	if (rst) cs_cnt = 0;
	else
		if (cs_cnt >= 31) cs_cnt = 0;
		else			  cs_cnt = cs_cnt + 1;

always @(posedge rst or posedge clk)
	if (rst) sclk = 1;
	else
		if ((cs_cnt >= 1) && (cs_cnt <= 16)) sclk = rclk;
		else								 			sclk = 1;
	
assign adc_sclk = sclk;

always @(posedge rst or posedge clk)
	if (rst) cs = 1;
	else
		if ((cs_cnt >= 1) && (cs_cnt <= 17)) cs = 0;
		else								 cs = 1;
	
assign adc_ncs = cs;

always @(posedge rst or posedge clk)
	if (rst) adc_din = 1;
	else	
		case (cs_cnt)
			5'd1 : adc_din = 1;			// write en '1' write, '0' read
			5'd2 : adc_din = 0;			// seq
			5'd3 : adc_din = 1;			// don't care
			5'd4 : adc_din = add_sel[2];	// add 2
			5'd5 : adc_din = add_sel[1];	// add 1
			5'd6 : adc_din = add_sel[0];	// add 0
			5'd7 : adc_din = 1;			// pm 1
			5'd8 : adc_din = 1;			// pm 0
			5'd9 : adc_din = 0;			// shadow
			5'd10 : adc_din = 1;			// don't care
			5'd11 : adc_din = 1;			// range 
			5'd12 : adc_din = 1;			// coding
			default : adc_din = 1;
		endcase

always @(posedge rst or posedge sclk)
	if (rst) out_buf <= 0;
	else	out_buf <= {out_buf[14:0], adc_dout};

assign led_out = (cs_cnt == 20) ? out_buf[11:4] : led_out;

endmodule