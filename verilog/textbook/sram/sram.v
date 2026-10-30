
module sram(
  ctrl_w, ctrl_r,  address, data_in,
  ram_cs, ram_oe, ram_we,  ram_address, ram_data,
  led_out
);

input 			ctrl_w, ctrl_r;
input [3:0] 	address;
input [3:0] 	data_in;
output 			ram_cs, ram_oe, ram_we;
output [17:0] 	ram_address;
inout [15:0] 	ram_data;
output [7:0] 	led_out;

wire 				ram_cs, ram_oe, ram_we;
wire [17:0] 	ram_address;
wire [15:0] 	ram_data;
wire [7:0] 		led_out;

assign ram_cs = 1'b0;

assign ram_oe = ~ctrl_r;

assign ram_we = ~ ctrl_w;

assign ram_address = {14'b00000000000000 , address };

assign ram_data = (ctrl_w) ? {12'b000000000000 , data_in} : 16'bzzzzzzzzzzzzzzzz;

assign led_out = (ctrl_r) ? {4'b0000, ram_data[3:0]} : 8'b00000000;


endmodule
