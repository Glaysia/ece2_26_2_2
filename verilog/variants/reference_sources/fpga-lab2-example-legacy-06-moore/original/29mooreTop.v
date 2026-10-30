module moore(
           input wire rst, x,
           output reg [1:0] y
       );
//모듈 선언 단에 입출력 포트와 비트 수, reg, wire여부 등을 한 번에 지정할 수 있다

// input rst;
// input x;
// output [1:0] y;
// reg [1:0] y;

reg [1:0] state;
// 필요한 state가 3개이므로 2비트 레지스터 스테이트 변수 할당
parameter s0=2'b00, s1=2'b01, s2=2'b10;

always @(posedge rst or posedge x)
begin
    if (rst) state = s0;
    else
    case(state)
        s0 : state = s1;
        s1 : state = s2;
        s2 : state = s0;
        default : state = s0;
    endcase
end

//무어머신은 현재 state가 다음 state를 결정하는 state machine이다
//밀리머신은 다음 state를 결정하는 요소가 현재
//state 뿐만 아니라 입력신호도 존재하는 state machine이다

always @(state)
begin
    case(state)
        s0 : y = 2'b00;
        s1 : y = 2'b01;
        s2 : y = 2'b10;
        default : y = 2'b11;
    endcase
end

endmodule
