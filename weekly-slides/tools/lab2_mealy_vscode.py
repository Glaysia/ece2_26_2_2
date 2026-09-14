"""Mealy walkthrough using actual student VS Code captures."""
from PIL import Image
from lab2_intro import paras

def walkthrough(d,base):
    def shot(title,name,caption,box):
        path=base/'assets/mealy-0914'/(name+'.png')
        with Image.open(path) as im: width,height=im.size
        x1,y1,x2,y2=box
        assert 0<=x1<x2<=width and 0<=y1<y2<=height
        trim=' '.join(f'{v*.75:g}bp' for v in (x1,height-y2,width-x2,y1))
        d.frame(title,r'\includegraphics[width=\textwidth,height=4.7cm,keepaspectratio,trim='+trim+r',clip]{assets/mealy-0914/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))
    shot('Mealy 자기검사 통과','01-simulation-pass','Ctrl+Shift+B 또는 Terminal → Run Task... → 02 Simulate. LAB2_PASS mealy_toggle checks=11을 확인한다. 종료 시각 67000 ps는 67 ns다.',(370,736,650,753))
    shot('파형 확장 활성화','10-enable-wave','Extensions에서 @installed vaporview 검색. 꺼져 있으면 Enable 옆 화살표 → Enable (Workspace). 설치되어 있지 않으면 앞의 추천 확장 절차를 따른다.',(554,183,850,266))
    shot('파형 파일 열기','11-open-wave','build/sim/wave.vcd를 연다. 빈 파형 화면에서 Netlist View를 누른다. 텍스트로 열리면 탭 우클릭 → Reopen Editor With... → VaporView.',(353,72,1050,188))
    shot('테스트벤치 신호 추가','12-add-signals','tb_mealy_toggle을 펼치고 이름을 우클릭 → Add All Variables in Scope (Shallow). bit_in·checks·clk·enable·rst·state·value가 추가된다.',(54,47,450,341))
    shot('검사 번호를 십진수로','13-format-checks','파형의 checks 이름을 우클릭 → Format Values → Decimal (Unsigned). 검사 번호를 0부터 11까지 읽을 수 있다. 짧은 검사 구간은 확대해서 확인한다.',(590,208,1043,432))
    shot('상태와 조합 출력을 함께 비교','14-wave-full','Zoom Fit을 누르고 이름 열을 넓힌다. 단위는 ps다. 12500 ps = 12.5 ns, 전체 실행은 67 ns다. state와 value가 바뀌는 시점을 각각 clk·bit_in과 비교한다.',(353,93,1427,355))
    d.frame('클록 사이 출력 변화 읽기',paras('5 ns 에지에서 state=0으로 리셋한다. 6 ns에 bit_in=1로 바꾸면 다음 클록을 기다리지 않고 value=2가 된다. TB는 7 ns에 확인한다.', '25 ns 에지에서 state=1, value=1이 된다. 26 ns에 bit_in=0으로 바꾸면 state는 1인 채 value=0이 된다. 27 ns 검사가 이 차이를 확인한다.', '36 ns에 bit_in=1이면 value=1, 45 ns 에지에서 state=0이면 value=2다. enable은 상태 갱신을 제어하며 조합 출력 자체를 끄지 않는다.'))
