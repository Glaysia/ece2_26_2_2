module register_4(
           input wire sw_s, sw_l,
           input wire[3:0] i,
           output reg[3:0]o
       ); //입력 포트 선언 wire와 reg를 명시적으로 구분하여 선언하였다. 명시하지 않는 경우에는 자동으로 wire로 선언이 된다고 한다.

reg [3:0] reg_tmp;
//모듈 내부에서 사용할 레지스터 변수 선언
always @(posedge sw_s)
    if (sw_s)	reg_tmp = i;

always @(posedge sw_l)
    if (sw_l)	o = reg_tmp;

endmodule


