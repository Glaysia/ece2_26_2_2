
module serial(  rst, clk,  rxd,  rs232_data
);

input rst, clk;
input rxd;
output [7:0] rs232_data;

reg [7:0] rs232_data;

parameter d1_cnt_value = 103;
parameter d1_cnt_half = 51;

reg start;
reg [7:0] rdata;
integer st_cnt, r_cnt;
integer rdata_cnt;

always @(posedge rst or posedge clk)
begin
  if (rst)
   begin
    start = 0;	st_cnt = 0;	rdata_cnt = 0;
   end
  else if ((start == 0) & (rxd == 0))
   begin
    if (st_cnt >= d1_cnt_half)
     begin
      start = 1;      st_cnt = 0;
     end
    else
     begin
      start = 0;      st_cnt = st_cnt + 1;
     end
   end
  else if (start == 1)
   if (r_cnt >= d1_cnt_value) 
    begin
     r_cnt = 0;
     
     if (rdata_cnt >= 8)
      begin
       rdata_cnt = 0;       start = 0;
      end
     else
      begin
       rdata_cnt = rdata_cnt + 1;       start = 1;
      end
    end
   else
    r_cnt = r_cnt + 1;
end

always @(posedge rst or posedge clk)
begin
  if (rst)
   begin
    rdata = 0;
    rs232_data = 0;
   end
  else if (r_cnt == d1_cnt_value)
    case (rdata_cnt)
      0 : rdata[0] = rxd;
      1 : rdata[1] = rxd;
      2 : rdata[2] = rxd;
      3 : rdata[3] = rxd;
      4 : rdata[4] = rxd;
      5 : rdata[5] = rxd;
      6 : rdata[6] = rxd;
      7 : rdata[7] = rxd;
      default : rdata = rdata;
    endcase
  else if (rdata_cnt == 8)
    rs232_data = rdata;
end

endmodule
          
