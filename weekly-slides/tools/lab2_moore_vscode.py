"""Moore GUI walkthrough using actual student workspace screenshots."""
from PIL import Image
from lab2_intro import paras

def walkthrough(d,base):
    def shot(title,name,caption,box):
        path=base/'assets/moore-0914'/(name+'.png')
        with Image.open(path) as im: width,height=im.size
        x1,y1,x2,y2=box
        assert 0<=x1<x2<=width and 0<=y1<y2<=height
        trim=' '.join(f'{v*.75:g}bp' for v in (x1,height-y2,width-x2,y1))
        d.frame(title,r'\includegraphics[width=\textwidth,height=4.7cm,keepaspectratio,trim='+trim+r',clip]{assets/moore-0914/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))
    shot('Moore 자기검사 통과','01-simulation-pass','Ctrl+Shift+B 또는 Terminal → Run Task... → 02 Simulate. LAB2_PASS moore_cycle checks=23을 확인한다. 종료 시각 226000 ps는 226 ns다.',(370,737,660,754))
    shot('파형 확장 활성화','09-enable-wave','Extensions에서 @installed vaporview를 검색한다. 꺼져 있으면 Enable 옆 화살표 → Enable (Workspace). 미설치 상태라면 앞의 추천 확장 절차를 따른다.',(554,183,850,265))
    shot('파형 뷰어 선택','10-open-with','build/sim/wave.vcd를 연다. 텍스트로 열리면 탭 우클릭 → Reopen Editor With... → VaporView.',(425,10,1018,165))
    shot('테스트벤치 신호 추가','12-add-signals','Netlist View에서 tb_moore_cycle을 펼친다. 이름을 우클릭 → Add All Variables in Scope (Shallow). 하위 task의 내부 변수까지 넣는 Recursive와 구분한다.',(54,47,446,338))
    shot('네 번의 상태 순환 확인','13-wave-full','Zoom Fit을 누르고 신호 이름 열을 넓힌다. 화면 단위는 ps다. 50000 ps = 50 ns이며 전체 실행은 226 ns다. value의 0 → 1 → 2 → 0 순환과 중간 유지 구간을 비교한다.',(353,93,1427,355))
    d.frame('첫 순환을 에지별로 읽기',paras('5 ns에 리셋되어 value=0이다. 6 ns에 advance가 1이 되어도 7 ns 검사 시점에는 value=0을 유지한다. 15 ns 상승 에지에서 value=1이 된다.','25 ns에는 advance=0, 35 ns에는 enable=0이므로 각각 value=1을 유지한다. 45 ns에 value=2, 55 ns에 value=0으로 돌아온다.','TB의 step은 에지 뒤 1 ns를 기다려 비교한다. 파형의 변화 시각과 검사 로그 시각을 구분하여 실험 전 레포트에 설명한다.'))
