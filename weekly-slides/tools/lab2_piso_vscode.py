"""PISO walkthrough backed by the actual v2.0.1 student workspace captures."""
from PIL import Image
from lab2_intro import paras


def walkthrough(d, base):
    def shot(title, name, caption, box):
        path = base / 'assets/piso-0913' / (name + '.png')
        with Image.open(path) as im:
            width, height = im.size
        x1,y1,x2,y2=box
        assert 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height
        trim=' '.join(f'{v*.75:g}bp' for v in (x1,height-y2,width-x2,y1))
        d.frame(title,r'\includegraphics[width=\textwidth,height=4.7cm,keepaspectratio,trim='+trim+r',clip]{assets/piso-0913/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

    shot('PISO 자기검사 통과','08-simulation-pass',
         'Ctrl+Shift+B 또는 Terminal → Run Task... → 02 Simulate. LAB2_PASS piso4 checks=114를 확인한다. 바로 다음 종료 로그는 976000 ps = 976 ns다.',(369,720,890,751))
    shot('설치된 파형 확장 활성화','09-enable-wave',
         'Extensions → @installed vaporview. 확장이 꺼져 있으면 톱니바퀴 → Enable (Workspace). 설치되지 않았다면 앞의 추천 확장 절차로 설치한다.',(54,104,630,236))
    shot('VCD를 VaporView로 열기','10-open-with',
         'Explorer → build/sim/wave.vcd. 텍스트로 열리면 파일 탭 우클릭 → Reopen Editor With... → VaporView.',(425,11,1017,162))
    shot('일곱 신호를 차례로 추가','11-netlist',
         'Netlist View → tb_piso4 펼치기. clk, rst, load, enable, data_in, value, serial_out을 차례로 더블클릭한다.',(52,46,346,399))
    shot('0–976 ns 전체 실행 확인','12-wave-full',
         'Zoom Fit으로 전체 구간을 맞춘다. 오른쪽 아래 Time Units → ns. 신호 이름이 잘리면 이름 열 경계를 오른쪽으로 끈다. data_in의 0부터 F까지 16개 입력을 확인한다.',(353,92,1430,355))
    shot('A 입력의 로드·유지·시프트','13-wave-a',
         '600–670 ns 부근을 확대한다. 615 ns 에지에 A가 저장되고 625 ns 에지에는 유지된다. 635·645·655·665 ns 에지 뒤 value는 4·8·0·0이다. 화면의 버스 값은 16진수다.',(444,123,1429,355))
    d.frame('파형과 TB 검사 시각 연결',paras(
        'TB의 step은 상승 에지 뒤 1 ns를 기다린다. 저장은 615 ns, load 검사는 616 ns다. 626 ns에는 hold와 첫 직렬 비트 1을 검사한다.',
        '이후 636·646·656 ns에 읽는 serial_out은 0·1·0이다. 각 비트를 읽고 다음 step을 실행하므로 shift 뒤에만 읽는 방식과 구분한다.',
        'VaporView 화면의 커서는 626.599 ns다. 이때 value=A, serial_out=1이다. TB 비교 시각 자체가 커서 시각인 것은 아니다.'))
