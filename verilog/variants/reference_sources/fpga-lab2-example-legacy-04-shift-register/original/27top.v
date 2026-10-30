module shift_register(
           input wire i, clk,
           output reg[3:0] o
       ); //입력 포트 선언 wire와 reg를 명시적으로 구분하여 선언하였다. 명시하지 않는 경우에는 자동으로 wire로 선언이 된다고 한다.

always @(posedge clk)
begin
    o[3] <= i;
    o[2] <= o[3];
    o[1] <= o[2];
    o[0] <= o[1];
end

// always @(posedge clk)
// begin
//     o[3] = i;
//     o[2] = o[3];
//     o[1] = o[2];
//     o[0] = o[1];
// end
// 등호(=, blocking)를 사용하면, 4개의 수식의 선후관계가 명확하게 존재한다.
// 등호(<=, nonblocking)를 사용하면, 4개의 수식이 동시에 실행하는 것처럼 존재한다.

// 가령, {a,b,c}=3'b000인 이전 상태에서
// begin
//  a=1
//  b=a
//  c=b
// end 과 같이 표현한다면, 이 식 이후에, {a,b,c}==3'b111이 된다. 반면

// begin
//  a<=1
//  b<=a
//  c<=b
// end 과 같이 표현한다면, 이 식 이후에, {a,b,c}==3'b100이 된다. 이전 상태를 충분히 반영하는
// 회로를 설계할 때는 nonblocking 표현을 사용하여야한다.
endmodule

