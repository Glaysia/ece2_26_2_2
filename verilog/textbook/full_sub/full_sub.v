
module full_sub(
a,b,c,d,bor
);       

input a, b, c;                        
output d, bor;

wire d1, b1, b2;

half_sub u1(a,b,d1,b1);
half_sub u2(d1,c,d,b2);

assign bor = b1 | b2; 

endmodule
