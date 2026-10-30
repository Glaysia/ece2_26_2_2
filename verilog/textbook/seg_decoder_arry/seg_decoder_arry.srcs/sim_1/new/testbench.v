`timescale 10ns / 100ps

module testbench();
// input
reg [3:0] bcd;
reg [2:0] sw;
// output
wire [7:0] seg_data;
wire [7:0] seg_com;
// Instantiate the U1
seg_decoder_arry u1(bcd, sw, seg_data, seg_com);
// Specify input stimulus
initial begin
        bcd = 4'b0101;
        sw = 3'b000;
    #5  sw = 3'b001;
    #5  sw = 3'b010;
    #5  sw = 3'b011;
    #5  sw = 3'b100;
    #5  sw = 3'b101;
    #5  sw = 3'b110;
    #5  sw = 3'b111;
end

endmodule

