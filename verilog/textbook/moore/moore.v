
module moore(  rst, x, y);

input rst;
input x;
output [1:0] y;

reg [1:0] y;
reg [1:0] state;

parameter s0=2'b00, s1=2'b01, s2=2'b10;

always @(posedge rst or posedge x)
begin
	if (rst) state = s0;
	else
	  case(state)
	    s0 : state = s1;
	    s1 : state = s2;
	    s2 : state = s0;
	    default : state = s0;
	  endcase
end

always @(state)
begin
	case(state)
	  s0 : y = 2'b00;
	  s1 : y = 2'b01;
	  s2 : y = 2'b10;
	  default : y = 2'b11;
	endcase
end

endmodule
