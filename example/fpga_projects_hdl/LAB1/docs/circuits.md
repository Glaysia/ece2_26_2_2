# 회로별 규칙과 검증

[전체 프로젝트](../README.md) · [통합 모드](integrated.md)

## 01. AND·OR·XOR 논리 게이트

입력 a, b / 출력 x, y, z

같은 입력 a, b에 대해 x는 AND, y는 OR, z는 XOR이다.

KEY1=a, KEY2=b. LED1=x, LED2=y, LED3=z.

자기검사 4개, 각 10ns. 마지막 30–40ns 구간에서 AND와 OR는 1, XOR는 0이다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-01-logic-gates/blob/8d25deb5c064edd95d61488a32d643c4bb331fb8/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-01-logic-gates/blob/9055c8002ec5149907f393a1c781000d44125e38/README.md) · [통합 모드 01](integrated.md#mode-01)

## 02. 전가산기

입력 a, b, cin / 출력 s, cout

반가산기 두 개로 세 입력을 더한다. 첫 합과 cin을 다시 더하고 두 carry를 OR로 합친다.

KEY1=a, KEY2=b, KEY3=cin. LED1=cout, LED2=s.

자기검사 8개, 각 10ns. 30–40ns의 0+1+1=2와 70–80ns의 1+1+1=3을 비교한다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-02-full-adder/blob/8b506af67d1e0cb7bc63854c8bb2a2633d3326be/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-02-full-adder/blob/0fe260d299847628fd01626c76ae87150f601ca1/README.md) · [통합 모드 02](integrated.md#mode-02)

## 03. 4비트 가산기

입력 a[3:0], b[3:0] / 출력 s[3:0], cout

0–15 범위의 두 수를 더한다. 결과는 carry 1비트와 합 4비트로 총 5비트다.

DIP1–4=a[3:0], DIP5–8=b[3:0]. LED1=cout, LED2–5=s[3:0].

자기검사 256개, 각 10ns. 310–320ns의 1+15에서 하위 합이 0이어도 전체 결과는 16이다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-03-adder4/blob/08543696c146164de20930270b01bfbd12ccdd72/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-03-adder4/blob/14578fedf93bb22b3366f2070d80cfe4a46ff62e/README.md) · [통합 모드 03](integrated.md#mode-03)

## 04. 4비트 감산기

입력 a[3:0], b[3:0] / 출력 d[3:0], bor

d는 a-b의 하위 4비트이고 bor는 a<b일 때만 1이다. 같은 수끼리 빼면 borrow는 0이다.

DIP1–4=a[3:0], DIP5–8=b[3:0]. LED1=bor, LED2–5=d[3:0].

자기검사 256개, 각 10ns. 10–20ns의 0-1과 170–180ns의 1-1에서 borrow가 다름을 확인한다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-04-subtractor4/blob/f7d79cd1f95d423edaa3746b75002b0ecf8c5eea/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-04-subtractor4/blob/6383aa022813906c7f438351eabe580c132879d5/README.md) · [통합 모드 04](integrated.md#mode-04)

## 05. 4비트 크기 비교기

입력 a[3:0], b[3:0] / 출력 o[2:0]

o[2]는 a>b, o[1]은 a=b, o[0]은 a<b를 나타낸다. 세 결과 중 하나만 1이다.

DIP1–4=a[3:0], DIP5–8=b[3:0]. LED1=큼, LED2=같음, LED3=작음.

자기검사 256개, 각 10ns. 0–10ns, 10–20ns, 160–170ns에서 같음·작음·큼을 각각 읽는다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-05-comparator4/blob/913b0f41c48c2351cdaba21380d0d83770c43445/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-05-comparator4/blob/d8e0f25d8058df9c07084f03cf997ae649fd84af/README.md) · [통합 모드 05](integrated.md#mode-05)

## 06. 4:1 멀티플렉서

입력 i[3:0], s[1:0] / 출력 z

선택 s=00,01,10,11은 각각 i[3],i[2],i[1],i[0]을 z로 보낸다. 원본의 비트 순서를 따른다.

KEY1–4=i[3:0], DIP1–2=s[1:0]. LED1=z.

자기검사 64개, 각 10ns. i=1000인 320–360ns에서 s를 바꿨을 때 선택된 입력을 추적한다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-06-mux4to1/blob/009d192cb7f873a2b31d0386ea68cc451fdec89b/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-06-mux4to1/blob/80d65af6339ade695aad964c39f66efb37ac7367/README.md) · [통합 모드 06](integrated.md#mode-06)

## 07. 1:8 디멀티플렉서

입력 i, s[2:0] / 출력 o[7:0]

입력 i를 선택된 한 출력에 보낸다. s=000이면 o[7], s=111이면 o[0]이다. i=0이면 모든 출력이 0이다.

KEY1=i, DIP1–3=s[2:0]. LED1–8=o[7:0].

자기검사 16개, 각 10ns. 80–90ns에서 가장 왼쪽 비트, 150–160ns에서 가장 오른쪽 비트가 켜진다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-07-demux1to8/blob/3e8c1e3f1cef7f602d586e152754182f43ac3679/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-07-demux1to8/blob/2e2ab8cf96476f44e9357cc4aa48570b7e18b613/README.md) · [통합 모드 07](integrated.md#mode-07)

## 08. 8:3 인코더

입력 i[7:0] / 출력 a[2:0]

한 비트만 켜진 입력을 번호로 바꾼다. i[7]만 1이면 0, i[0]만 1이면 7이다. 0 또는 다중 입력은 000을 출력한다.

KEY1–8=i[7:0]. LED1–3=a[2:0]. 출력 000만으로 유효 입력 여부를 판단할 수 없다.

자기검사 256개, 각 10ns. 10–20ns의 01과 30–40ns의 03을 비교한다. 이 회로는 우선순위 인코더가 아니다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-08-encoder8to3/blob/485a6c588c7c9230222c4763deb372f36e5b3384/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-08-encoder8to3/blob/7f88377d78cf60cece52021e238a9ecc62d70a0b/README.md) · [통합 모드 08](integrated.md#mode-08)

## 09. 3:8 디코더

입력 a, b, c / 출력 o[7:0]

입력 abc의 이진 번호와 같은 o 비트를 1로 만든다. 000은 o[0], 111은 o[7]이다.

KEY1=a, KEY2=b, KEY3=c. LED1–8=o[7:0]이므로 000에서 LED8, 111에서 LED1이 켜진다.

자기검사 8개, 각 10ns. 0–10ns의 출력 01과 70–80ns의 출력 80을 읽고 비트 번호를 확인한다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-09-decoder3to8/blob/d5a11d33868dfb9ff71b7e598644099a9ce59b65/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-09-decoder3to8/blob/e4d6725666068c25fb4a261ba10512cd2e350ad7/README.md) · [통합 모드 09](integrated.md#mode-09)

## 10. 7세그먼트 디코더

입력 bcd[3:0] / 출력 seg_data[7:0]

4비트 입력의 0–F를 표시한다. seg_data[7:0] 순서는 a,b,c,d,e,f,g,dp이며 1에서 점등하고 dp는 항상 0이다.

DIP1–4=bcd[3:0]. 단일 7세그먼트 a–dp. 이름은 bcd지만 입력 10–15도 A,b,C,d,E,F로 정의한다.

자기검사 16개, 각 10ns. 80–90ns에서 8의 일곱 획이 모두 켜지고 dp 비트는 0인지 확인한다.

[최신 프로젝트](https://github.com/Glaysia/fpga-lab-example-vivado-2026-1-10-seven-segment/blob/6cad34ce6d1385cd261b510024d50936dccb8f45/README.md) · [레거시](https://github.com/Glaysia/fpga-lab-example-legacy-10-seven-segment/blob/ccd38e3159da27d975bcb65cb2a34911d881a701/README.md) · [통합 모드 10](integrated.md#mode-10)
