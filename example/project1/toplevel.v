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

// 순차논리회로: 스테이트를 가지며 과거부터 현재의 모든 입력에 의해 출력이 결정됨, 클럭이 있어야 이해하기 쉬움 

fulladder fa (
    .a(flop1),
    .b(flop2),
    .cin(1'b0),
    .sum(sum),
    .cout(cout)
);
// 조합논리회로: 스테이트를 가지지 않고 클력에 관련없이 무조건 같은 입력엔 같은 출력을 내는 함수 같은 개념 

endmodule

