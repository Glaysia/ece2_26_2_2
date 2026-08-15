`timescale 1us/1ns

module toplevel(
    input wire clk,
    input wire rst,
    output wire sum,
    output wire cout
);

reg flop1, flop2;


always @(posedge clk or posedge rst) begin
    if (rst) begin
    flop1 <= 1'b0;
    flop2 <= 1'b1;
    end
    else begin
    flop1 <= flop2; // <=와 =가 다름 blocking/nonblocking이 뭔지 나중에 알아보세요
    flop2 <= flop1;
    end
end

fulladder fa (
    .a(flop1),
    .b(flop2),
    .cin(1'b0),
    .sum(sum),
    .cout(cout)
);

endmodule

