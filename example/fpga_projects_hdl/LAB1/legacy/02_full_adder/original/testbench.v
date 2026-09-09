`timescale 10ns / 100ps

module testbench();
// input
reg a, b, cin;
// output
wire s, cout;
// Instantiate the U1
full_adder u1(a, b, cin, s, cout);
// Specify input stimulus
initial begin
    	a = 0; b = 0; cin=0;
    #10 a = 1; b = 0; cin=0;
    #10 a = 0; b = 1; cin=0;
    #10 a = 1; b = 1; cin=0;
    #10 a = 0; b = 0; cin=1;
    #10 a = 1; b = 0; cin=1;
    #10 a = 0; b = 1; cin=1;
    #10 a = 1; b = 1; cin=1;
end

endmodule

