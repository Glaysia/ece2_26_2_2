module mealy(
           input wire rst, x,
           output reg [1:0] y
       );
//모듈 선언 단에 입출력 포트와 비트 수, reg, wire여부 등을 한 번에 지정할 수 있다

// input rst, x;
// output [1:0] y;
// reg [1:0] y;

reg state;
// 필요한 state가 3개이므로 2비트 레지스터 스테이트 변수 할당
parameter s0=1'b0, s1=1'b1;

always @(posedge rst or posedge x) begin
    if (rst) state = s0;
    else
    case(state)
        s0 : state = s1;
        s1 : state = s0;
        default : state = s0;
    endcase
end

//무어머신은 현재 state가 다음 state를 결정하는 state machine이다
//밀리머신은 다음 state를 결정하는 요소가 현재
//state 뿐만 아니라 입력신호도 존재하는 state machine이다

always @(state, x)
begin
    if ((state == s0) && (x == 1'b1))
        y = 2'b10;
    else if ((state == s1) && (x == 1'b1))
        y = 2'b01;
    else
        y = 2'b00;
end

endmodule
