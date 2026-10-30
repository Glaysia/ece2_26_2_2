module servo_ctrl(
 clk, resetn, l_ctrl, r_ctrl,
 servo
);

input clk;
input resetn, l_ctrl, r_ctrl;
output servo;

integer tmp, cnt;
reg l, r;
reg servo;

always @(posedge resetn or posedge clk)
begin
  if (resetn) cnt = 0;
  else
    if (cnt >= 199)  cnt = 0;
    else  cnt = cnt + 1;
end

always @(posedge resetn or posedge clk)
begin
  if (resetn) tmp = 15;
  else
  begin
    l <= l_ctrl; r <= r_ctrl;
	 
    if (l == 0 & l_ctrl & tmp > 7) tmp = tmp - 1;
    else if (r == 0 & r_ctrl & tmp < 23) tmp = tmp + 1;
  end
end

always @(cnt or tmp)
begin
  if (cnt < tmp)
    servo = 1;
  else
    servo = 0;
end

endmodule
