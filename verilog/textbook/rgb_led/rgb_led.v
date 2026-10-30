
module rgb_led ( sw, cled_r, cled_g, cled_b);

input sw;

output [3:0] cled_r;
output [3:0] cled_g;
output [3:0] cled_b;

wire [3:0] cled_r;
wire [3:0] cled_g;
wire [3:0] cled_b;

reg [2:0] reg_rgb = 3'b000;

always @(posedge sw)
	reg_rgb = reg_rgb + 1;

assign cled_r = {reg_rgb[2], reg_rgb[2], reg_rgb[2], reg_rgb[2]};
assign cled_g = {reg_rgb[1], reg_rgb[1], reg_rgb[1], reg_rgb[1]};
assign cled_b = {reg_rgb[0], reg_rgb[0], reg_rgb[0], reg_rgb[0]};
	
endmodule
				
				
		
						