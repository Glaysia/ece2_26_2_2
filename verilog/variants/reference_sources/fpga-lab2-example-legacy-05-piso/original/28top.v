
module piso4(
           input wire shldn, clk,
           input wire[3:0] d,
           output wire q
       ); //입력 포트 선언 wire와 reg를 명시적으로 구분하여 선언하였다. 명시하지 않는 경우에는 자동으로 wire로 선언이 된다고 한다.

reg [3:0] tmp;
//모듈 내부에서 사용할 레지스터 변수 선언

always @(posedge shldn or posedge clk)
    if (shldn) 	tmp = d;
    else tmp = {tmp[2:0], 1'b0};

assign q = tmp[3];

endmodule


