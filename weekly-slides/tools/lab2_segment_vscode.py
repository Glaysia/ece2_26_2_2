"""Segment scan walkthrough backed by actual student VS Code captures."""
from PIL import Image
from lab2_intro import paras

def walkthrough(d,base):
    def shot(title,name,caption,box):
        path=base/'assets/segment-0914'/(name+'.png')
        with Image.open(path) as im: width,height=im.size
        x1,y1,x2,y2=box
        assert 0<=x1<x2<=width and 0<=y1<y2<=height
        trim=' '.join(f'{v*.75:g}bp' for v in (x1,height-y2,width-x2,y1))
        d.frame(title,r'\includegraphics[width=\textwidth,height=4.7cm,keepaspectratio,trim='+trim+r',clip]{assets/segment-0914/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))
    shot('7세그먼트 자기검사 통과','01-simulation-pass','Ctrl+Shift+B 또는 Terminal → Run Task... → 02 Simulate. LAB2_PASS segment_scan8 checks=194를 확인한다. 종료 시각 1306000 ps는 1306 ns다.',(370,718,725,738))
    shot('파형 확장 활성화','17-enable-wave','Extensions에서 @installed vaporview 검색. 꺼져 있으면 Enable 옆 화살표 → Enable (Workspace). 설치되어 있지 않으면 앞의 추천 확장 절차를 따른다.',(554,183,855,266))
    shot('파형 파일 열기','18-open-wave','build/sim/wave.vcd를 연다. 텍스트로 열리면 탭 우클릭 → Reopen Editor With... → VaporView. 빈 파형 화면에서 Netlist View를 누른다.',(353,72,1095,188))
    shot('테스트벤치 신호 추가','19-add-signals','tb_segment_scan8 이름을 우클릭 → Add All Variables in Scope (Shallow). clk·rst·enable·digits·index·segments·select와 검사 변수가 추가된다.',(54,47,450,344))
    shot('검사 번호를 십진수로','20-format-checks','파형의 checks 이름을 우클릭 → Format Values → Decimal (Unsigned). 이름 열 경계를 오른쪽으로 끌어 신호 이름이 모두 보이게 한다.',(600,185,1068,442))
    shot('자리 선택 사이의 소등 구간','21-wave-detail','단위는 ps다. 15000 ps = 15 ns. select는 15 ns에 01, 35 ns에 00, 55 ns에 02가 된다. 00인 구간은 모든 자리를 끄는 구간이다. enable=0인 25 ns와 45 ns 에지에서는 각각 점등·소등 상태가 유지된다.',(353,93,1427,470))
    shot('두 입력 묶음과 네 번의 순회','22-wave-full','Zoom Fit으로 전체 1306 ns를 본다. digits는 76543210에서 fedcba98로 바뀐다. 각 입력 묶음마다 index=0~7을 두 번 순회해 0~F의 세그먼트 패턴을 검사한다. 마지막에는 rst로 index=0·select=00을 확인한다.',(353,93,1427,470))
    d.frame('파형과 실제 보드의 극성 연결',paras('코어 select는 active-high다. 01은 index=0 자리 하나를 선택하고 00은 모든 자리를 끈다. segments는 abcdefg와 dp 순서이며 dp는 항상 0이다.', '보드 연결 모듈은 select의 비트 순서를 뒤집고 반전하여 seg_com에 연결한다. 따라서 코어 index=0은 보드 COM[7]에 해당하며, 코어 select=00은 보드 seg_com=FF가 된다.', '테스트벤치는 enable을 멈춰 유지 동작도 검사한다. 보드 모듈은 enable=1로 연결해 1 kHz 클록에서 자동 순환한다. N8 버튼을 누르는 동작과 자동 스캔을 혼동하지 않는다.'))
