
module stepmotor(clk, rst, stepmotor);

input clk;
input rst;

output [3:0] stepmotor;

reg [3:0] stepmotor;
reg [1:0] state;


always @(posedge clk)
	if (rst) state = 0;
	else 	 state = state + 1;

always @(posedge clk)
	case(state)
		2'd0 : stepmotor = 4'b0011;
		2'd1 : stepmotor = 4'b0110;
		2'd2 : stepmotor = 4'b1100;
		2'd3 : stepmotor = 4'b1001;
	endcase

endmodule
		
