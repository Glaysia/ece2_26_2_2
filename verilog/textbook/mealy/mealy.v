
module mealy(  rst, x, y);

input rst, x;
output [1:0] y;

reg [1:0] y;
reg state;

parameter s0=1'b0, s1=1'b1;

always @(posedge rst or posedge x)
begin
if (rst) state = s0;
else
	case(state)
	  s0 : state = s1;
	  s1 : state = s0;
	  default : state = s0;
	endcase
end

always @(state, x)
begin
  if ((state == s0) && ( x == 1'b1))
    y = 2'b10;
  else if ((state == s1) && (x == 1'b1))
    y = 2'b01;
  else
    y = 2'b00;
end

endmodule
