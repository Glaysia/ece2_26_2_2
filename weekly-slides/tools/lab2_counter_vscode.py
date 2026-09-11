"""Build the first counter's VS Code review handout from actual GUI captures."""
import json
from lab2_series import BASE, LAB, Deck, code, setup, paras, steps, terminal

p = json.loads((LAB/'projects.json').read_text('utf-8'))[0]
project = LAB/p['path']
config = json.loads((project/'simulation.json').read_text('utf-8'))
d = Deck('counter-vscode')

def screen(title, name, caption):
    d.frame(title, r'\includegraphics[width=\textwidth,height=5.0cm,keepaspectratio]{assets/vscode-0911/'+name+r'.png}\par\vspace{0.15cm}'+paras(caption))

d.frame('LAB 2 · 카운터: VS Code', paras('작성일 2026. 09. 11.','소스 작성 → 기능 시뮬레이션 → 파형 확인','첫 카운터의 VS Code 단계 확인용 자료'))
d.frame('목차', r'\navlink{setup}{프로젝트 시작}\par\vspace{0.4cm}\navlink{code}{RTL·테스트벤치·XDC 작성}\par\vspace{0.4cm}\navlink{simulation}{실행과 파형 확인}\par\vspace{0.4cm}\navlink{reports}{실험 전 레포트}', 'lab2-contents')
setup(d,p,project,config)
screen('새 VS Code 창', '01-new-window', 'File → New Window 또는 Ctrl+Shift+N으로 새 창을 연다.')
screen('워크스페이스 열기', '02-file-menu', 'File → Open Workspace from File...에서 프로젝트의 LAB1.code-workspace를 고른다.')
screen('프로젝트 폴더 확인', '03-workspace', 'Explorer에서 src·sim·constraints 폴더를 확인한다. 아래 캡처는 완성 예시 폴더에서 촬영했다.')
d.frame('카운터의 동작', paras('rst=1이면 0으로 초기화한다. enable=0이면 현재 값을 유지한다.','enable=1에서 down=0이면 증가, down=1이면 감소한다.','4비트 값이므로 15 다음은 0, 0에서 감소하면 15가 된다.'), 'code')
for name in [*config['sources'], config['testbench']]:
    code(d,project,name)
d.frame('XDC 작성과 검증 범위', paras('다음 세 화면의 XDC를 constraints/lab2_counter.xdc에 작성한다.','포트 이름을 lab2_counter.v와 대조한다.','Icarus는 XDC를 읽지 않는다. 이번 PASS는 counter4 코어의 기능 검사이며 보드 배선·핀·타이밍 검증은 별도 단계다.'))
code(d,project,p['constraints'])
d.frame('VS Code에서 실행', steps('File → Save All.','상단 Terminal → Run Task...를 누른다. 메뉴가 접혀 있으면 ...를 누른다.','01 Check tools로 도구 경로를 확인한 뒤 02 Simulate를 선택한다.'), 'simulation')
screen('Run Task 메뉴', '04-run-task-menu', 'Terminal → Run Task...를 누른다.')
screen('시뮬레이션 작업 선택', '05-task-list', '01 Check tools: 설치 확인. 02 Simulate: 컴파일과 테스트벤치 실행.')
screen('Python 실행 오류를 만났다면', '06-python-alias-error', '9009와 WindowsApps 경로가 나오면 Python 실행 별칭이 선택된 것이다.')
screen('설치된 Python 경로 지정', '07-python-path-fix', 'LAB1.code-workspace의 Windows command를 자신의 실제 python.exe 경로로 바꾸고 저장한다. 캡처의 UOS 경로는 이 PC의 예시다.')
d.frame('실행 경로를 수정할 때', steps('Ctrl+P → LAB1.code-workspace를 연다.','tasks 안의 windows → command 항목을 찾는다.','세 작업에 있는 Python 실행 경로를 자신의 설치 경로로 수정한다.','JSON 경로 구분자는 /를 사용한다. Ctrl+S로 저장한다.','Terminal → Run Task... → 02 Simulate를 다시 실행한다.'))
screen('실제 실행 결과', '08-counter-pass', 'LAB2_PASS counter4 checks=36. 종료 시각 356000 ps = 356 ns. 2026-09-11 GUI 실행에서 확인했다.')
d.frame('PASS가 확인한 내용', paras('리셋, 증가와 15→0 순환, 감소와 0→15 순환, enable=0 유지, 리셋 우선순위를 총 36회 검사한다.','이번 테스트벤치의 DUT는 counter4이다. 입력 동기화·디바운스와 실제 핀 동작까지 통과했다는 의미는 아니다.','편집기의 경고 4개는 남아 있다. 경고 0개로 기록하지 않는다.'))
screen('VaporView가 비활성화되어 있다면', '10-enable-waveform', 'Extensions에서 VaporView를 찾고 Enable 옆 화살표 → Enable (Workspace)를 선택한다.')
screen('VCD를 파형으로 열기', '11-vaporview-select', 'build/sim/wave.vcd를 연다. 텍스트로 보이면 탭 우클릭 → Reopen Editor With... → VaporView.')
screen('관찰할 신호 추가', '12-netlist-signals', 'Netlist View에서 tb_counter4를 펼친다. clk·rst·enable·down·value[3:0]를 더블클릭해 추가한다.')
screen('전체 파형 확인', '14-counter-wave-ns', 'Zoom Fit으로 전체 시간을 맞춘다. 신호 이름 열을 넓히고 하단 시간 단위를 ns로 바꾼다.')
d.frame('파형을 읽는 순서', steps('clk 상승 에지 직후 value가 바뀌는지 본다.','down=0의 증가 구간과 down=1의 감소 구간을 비교한다.','enable=0 구간에서 value가 유지되는지 확대한다.','마지막 rst=1 구간과 356 ns 종료를 확대해 확인한다.','신호 이름·시간축·입력·출력이 함께 보이게 캡처한다.'))
d.frame('실험 전 레포트', steps('RTL과 테스트벤치가 맡은 역할을 설명한다.','초기화·증가·감소·순환·유지의 예상 결과를 표로 적는다.','자신이 실행한 PASS 로그와 파형을 넣고 각 구간을 설명한다.','Python 경로 등 자신이 고친 설정과 발생한 오류를 적는다.','XDC는 작성했지만 이번 기능 시뮬레이션에 사용되지 않았음을 구분한다.'), 'reports')
assert d.missing == 0, d.missing
print(d.write('05.LAB2_01_COUNTER_VSCODE.tex','LAB2 카운터 · VS Code'))
