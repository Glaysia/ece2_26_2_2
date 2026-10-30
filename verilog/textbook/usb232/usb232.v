
module usb232(
  resetn, clk,   
  rxd,txd,
  rs232_data
);

input resetn, clk;
input rxd;
output [7:0] rs232_data;
output txd;

reg [7:0] rs232_data;

parameter d1_cnt_value = 104;
parameter d1_cnt_half = 52;

reg [7:0] rdata;
integer st_cnt, r_cnt;
integer rdata_cnt;

reg txd;

reg [7:0] tdata;
integer tdata_cnt;
integer t_cnt;

reg [1:0] r_state, t_state;


always @(posedge resetn or posedge clk)
begin
  if (resetn)
   begin
    r_state = 0;
	 tdata = 0;
	 rs232_data = 0;
   end
  else
		case (r_state)
			2'b00 : 
				if (rxd == 0)
					if (st_cnt >= d1_cnt_half)
					begin
						st_cnt = 0;
						r_state = 2'b01;
					end
					else
					begin
						st_cnt = st_cnt + 1;
						r_state = 2'b00;
					end
					
			2'b01 : 		  
				if (rdata_cnt == 9)		r_state = 2'b10;
				else							r_state = 2'b01;
				
			2'b10 :
			begin
				rs232_data = rdata;
				tdata = rdata;
				r_state = 2'b11;
			end
			
			2'b11 : 
				r_state = 2'b00;
				
			default : 
				r_state = 2'b00;
		endcase
end

always @(posedge resetn or posedge clk)
begin
  if (resetn)
    t_state = 0;
  else
		case (t_state)
			2'b00 : 
				if (r_state == 2'b11)		t_state = 2'b01;
				else								t_state = 2'b00;				
					
			2'b01 : 		  
				if ((tdata_cnt == 9) )	t_state = 2'b10;
				else											t_state = 2'b01;
				
			default : 
				t_state = 2'b00;
		endcase
end
			

always @(posedge resetn or posedge clk)
begin
  if (resetn)
   begin
		rdata_cnt = 0;
		r_cnt = 0;
   end
	else if (r_state == 2'b01)
		if (r_cnt >= d1_cnt_value) 
		begin
			r_cnt = 0;
		  
			if (rdata_cnt >= 9)		rdata_cnt = 0;
			else							rdata_cnt = rdata_cnt + 1;

		end
		 
		else
		 r_cnt = r_cnt + 1;
	else
	begin
		rdata_cnt = 0;
		r_cnt = 0;
	end

end

always @(posedge resetn or posedge clk)
begin
	if (resetn)
		rdata = 0;
	else if (r_state == 2'b01)
  
	  if (r_cnt == d1_cnt_value)
	  begin
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
	  end
end

always @(posedge resetn or posedge clk)
begin
	if (resetn)
	begin
		t_cnt = 0;
		tdata_cnt = 0;
	end
	
	else if (t_state == 2'b01)
	begin 
	
		if (t_cnt == d1_cnt_value)
		begin
			t_cnt = 0;
      
			if (tdata_cnt >= 10)      tdata_cnt = 0;
         else					        tdata_cnt = tdata_cnt + 1;
      
		end
   
		else
			t_cnt = t_cnt + 1;
	end
	
	else
	begin
		t_cnt = 0;
		tdata_cnt = 0;
	end
end


always @(posedge resetn or posedge clk)
begin
	if (resetn)
    txd = 1;
	else if (t_state == 2'b01)
    case (tdata_cnt)   
      0 :  txd = 0;
      1 :  txd = tdata[0];
      2 :  txd = tdata[1];
      3 :  txd = tdata[2];
      4 :  txd = tdata[3];
      5 :  txd = tdata[4];
      6 :  txd = tdata[5];
      7 :  txd = tdata[6];
      8 :  txd = tdata[7];
      9 : txd = 1;
      default : txd = 1;
    endcase
  
  else
	txd = 1;
end

endmodule
          
        
