`timescale 10ns / 10ps

module testbench();
// input
reg sw;
// output
wire [3:0] cled_r, cled_g, cled_b;
// Instantiate the U1
rgb_led u1(sw, cled_r, cled_g, cled_b);
// Specify input stimulus
initial begin
		sw=0;
end

always #5 sw = ~sw;

endmodule

