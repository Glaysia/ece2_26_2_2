"""Integrated walkthrough from actual student VS Code/VaporView captures."""
from PIL import Image
from lab2_intro import paras


def walkthrough(d, base):
    def shot(title, name, caption, box):
        path = base / 'assets/integrated-0914' / (name + '.png')
        with Image.open(path) as im:
            width, height = im.size
        x1, y1, x2, y2 = box
        assert 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height
        trim = ' '.join(f'{v*.75:g}bp' for v in (x1, height-y2, width-x2, y1))
        d.frame(title, r'\includegraphics[width=\textwidth,height=4.7cm,keepaspectratio,trim='
                + trim + r',clip]{assets/integrated-0914/' + name
                + r'.png}\par\vspace{0.15cm}' + paras(caption))

    shot('통합 자기검사 통과', '01-simulation-pass',
         'Ctrl+Shift+B 또는 Terminal → Run Task... → 02 Simulate. LAB2_INTEGRATED_PASS modes=8 checks=2848을 확인한다. 종료 시각은 34326 ns다.',
         (369,703,701,721))
    shot('파형 확장 활성화', '18-enable-wave',
         'Extensions에서 @installed vaporview 검색. 꺼져 있으면 Enable 옆 화살표 → Enable (Workspace). 설치 전이면 앞의 추천 확장 절차를 따른다.',
         (554,183,855,267))
    shot('텍스트 대신 파형으로 열기', '19-reopen-wave',
         'build/sim/wave.vcd를 연다. 텍스트로 열렸다면 편집기 오른쪽 위 Text Editor 옆 화살표 → VaporView를 선택한다.',
         (1175,68,1440,185))
    shot('Netlist View 열기', '20-wave-empty',
         '빈 파형 화면의 Netlist View를 누른다. 왼쪽에서 tb_lab2_integrated를 찾는다.',
         (353,72,1100,195))
    shot('테스트벤치 신호와 내부 mode 추가', '21-add-signals',
         'tb_lab2_integrated를 우클릭 → Add All Variables in Scope (Shallow). 이어서 tb_lab2_integrated → dut를 펼쳐 mode를 더블클릭한다. mode는 맨 아래에 추가된다.',
         (54,48,450,342))
    shot('검사 수는 십진수로 표시', '22-checks-decimal',
         'checks를 우클릭 → Format Values → Decimal (Unsigned). LCD 데이터와 LED·세그먼트 버스는 16진수로 둔다.',
         (648,250,1103,486))
    shot('파형 이름을 읽기 쉽게', '25-name-only',
         '파형 영역에서 Ctrl+A → 신호 이름 우클릭 → Name → Name Only. 빈 영역을 클릭해 선택을 해제한다. Ctrl+B로 사이드바를 접으면 가로 공간이 넓어진다.',
         (325,250,777,474))
    shot('시간 단위와 전체 구간', '24-time-unit',
         '시간 눈금을 우클릭 → Time Unit → μs. 왼쪽 위 첫 돋보기인 Zoom Fit을 누르면 전체 34.326 μs를 볼 수 있다.',
         (794,136,1212,382))
    shot('8개 모드의 전환 확인', '26-wave-full-names',
         '맨 아래 mode는 0~7을 순회한 뒤 0으로 돌아온다. mode_button과 step_button의 역할을 구분하고 led·sw·seg_com·seg_data를 함께 비교한다. mode=7에서만 7세그먼트 스캔이 활성화된다.',
         (320,495,1427,774))
    shot('LCD에 MODE 05를 보내는 구간', '27-lcd-mode05',
         'Zoom In으로 약 17.1 μs 부근을 확대한다. lcd_data의 80은 첫 줄 주소 명령(RS=0), 뒤의 4D 4F 44 45 20 30 35는 MODE 05 문자(RS=1)다. 내부 mode=4와 LCD 표시 번호 05를 연결해 설명한다.',
         (330,380,1427,490))
    d.frame('LCD 데이터와 Enable의 관계', paras(
        '데이터가 바뀐 뒤 다음 클록에서 lcd_e가 올라가고, 그 다음 클록에서 내려간다. E가 높은 동안 데이터와 RS가 유지되는지 확대 파형에서 확인한다. lcd_rw는 항상 0이다.',
        '테스트벤치는 10 ns 주기로 시간을 줄여 검사한다. 실제 보드의 1 kHz 클록에서는 한 클록이 1 ms이므로 파형의 ns 값을 장비의 동작 시간으로 그대로 쓰지 않는다.',
        'LCD는 한 화면을 쓰기 시작할 때 모드를 저장한다. 버튼 입력 직후 화면 전체가 즉시 바뀌는 것으로 해석하지 말고 다음 화면 갱신을 확인한다.'))
