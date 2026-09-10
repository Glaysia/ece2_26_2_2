"""Generate editable LAB1 TeX from circuit metadata and measured simulation files."""
from pathlib import Path
import json, re, bisect
from lab1_code_panels import PANELS

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'example/fpga_projects_hdl/LAB1'
BASE = ROOT / 'weekly-slides/weekly-slides/LAB1_FPGA_0914'
CIRCUITS = json.loads((LAB/'docs/circuits.json').read_text(encoding='utf-8'))
PROJECTS = json.loads((LAB/'projects.json').read_text(encoding='utf-8'))
for project in PROJECTS:
    configuration=json.loads((LAB/project['path']/'simulation.json').read_text(encoding='utf-8'))
    project.update(configuration)
    project['constraints']='constraints/'+Path(project['constraints']).name
COURSE = 'https://github.com/Glaysia/ece2_26_2_2/blob/daily/0910/'
TEMPLATE = 'https://github.com/Glaysia/fpga-lab-template/tree/v2.0.0'
EXAMPLES = {p['project']:p for p in json.loads((LAB/'docs/example-repositories.json').read_text(encoding='utf-8'))}

def example_url(p):
    entry=EXAMPLES[p['path']]
    return entry['repository'].removesuffix('.git')+'/tree/'+entry['commit']

def student_setup(d,p):
    folder=p.get('student_folder','lab1_'+p['path'].split('/')[-1]+('_cli' if p['edition']=='opensource_cli' else ''))
    d.frame('시뮬레이션 도구 확인',para('Git·Python 3.10 이상·VS Code·Icarus Verilog를 설치한다. Windows PowerShell에서 한 줄씩 확인한다.')+terminal('git --version','python --version','iverilog -V','vvp -V')+para('설치·PATH 변경 후 VS Code를 다시 연다. Linux·macOS·WSL은 python 대신 python3를 사용한다.')+link(TEMPLATE,'설치와 빈 템플릿 안내'),d.label+'-setup')
    cli=p['edition']=='opensource_cli'
    continuation=chr(92) if cli else '`'
    d.frame('v2.0.0 템플릿을 새 이름으로 clone',para('아래는 '+('macOS·Linux·WSL의 Bash/Zsh' if cli else 'Windows PowerShell')+' 명령이다. 줄 끝 문자는 다음 줄로 명령을 이어 준다.')+terminal('git clone --branch v2.0.0 '+continuation,'  https://github.com/Glaysia/fpga-lab-template.git '+continuation,'  '+folder,'cd '+folder,'git switch -c main','code LAB1.code-workspace')+para('회로마다 마지막 폴더 이름을 바꾼다. 시작 파일은 주석뿐이며 코드 이미지를 보며 직접 작성한다.')+link(TEMPLATE,'고정된 수업 버전 v2.0.0'))
    d.frame('File → New Window',para('VS Code 상단 File → New Window. Ctrl+Shift+N도 같은 동작이다.')+crop('vscode:01-file-menu',(37,28,332,106),1.6)+para('새 창의 File → Open Workspace from File...을 누른다.')+crop('vscode:01-file-menu',(37,140,332,216),1.6))
    d.frame('프로젝트 하나의 workspace 열기',items(['방금 clone한 '+folder+' 폴더를 연다.','LAB1.code-workspace를 선택하고 Open. 모든 실습의 workspace 파일명은 같다.','Explorer에 PROJECT 하나와 src·sim·constraints·tools 폴더가 보이는지 확인한다.','src/design.v·sim/tb_design.v·constraints/pins.xdc는 아직 주석뿐이다.','simulation.json은 실행할 RTL·TB 파일과 TB top을 지정하는 설정이다.']))
    d.frame('추천 확장 설치',items(['왼쪽 Extensions 아이콘을 누른다.','검색창에 @recommended를 입력한다.','slang의 Install: Verilog/SystemVerilog 편집·진단.','VaporView의 Install: VCD 파형 확인.','vscode-pdf의 Install: 코드 옆에서 PDF 교안 열기.'])+para('WSL 사용자는 WSL 창에서 필요할 경우 Install in WSL을 누른다. 확장 설치와 Python·Icarus 설치는 별개다.'))
    names=[Path(x).name for x in p['sources']]
    d.frame('src에 RTL 파일 만들기',items(['Explorer에서 src 왼쪽 화살표를 눌러 펼친다.','design.v 우클릭 → Rename → '+names[0]+' 입력.','파일을 두 번 눌러 열고 뒤의 코드 이미지를 보며 전체 코드를 입력한다.','추가 RTL이 있으면 src 우클릭 → New File로 만든다.','전체 RTL 파일 목록은 다음 장의 src 표를 따른다.','File → Save All로 모든 파일을 저장한다.'])+para('설계 모듈명: '+p['top']+'. 파일명과 module 이름을 구분한다.'))
    d.frame('sim에 테스트벤치 만들기',items(['sim을 펼치고 tb_design.v 우클릭 → Rename.','새 파일명: '+Path(p['testbench']).name,'뒤의 TB 코드 이미지에 있는 선언·DUT 연결·입력 자극·예상값 검사를 직접 작성한다.','wave.vcd를 만드는 dumpfile·dumpvars와 종료 조건까지 작성한다.','TB 모듈명: '+p['simulation_top'],'File → Save All. TB를 합성용 RTL 폴더에 넣지 않는다.']))
    for start in range(0,len(names),6):
        d.frame('작성할 RTL 파일 목록'+(f' ({start//6+1})' if len(names)>6 else ''),table(['폴더','파일명'],[('src',n) for n in names[start:start+6]])+para('각 파일을 New File로 만들고 코드 이미지의 전체 내용을 작성한다. 파일마다 module 선언과 endmodule을 확인한다.'))
    d.frame('simulation.json을 내 파일에 맞추기',para('Explorer에서 simulation.json을 두 번 눌러 연다.','sources 배열: 앞의 모든 RTL 파일명 앞에 src/를 붙여 등록한다.','한 파일 예: "sources": ["src/'+names[0]+'"]','testbench: sim/'+Path(p['testbench']).name,'simulation_top: '+p['simulation_top'],'sources의 각 경로와 testbench·simulation_top 값은 큰따옴표로 감싼다. 여러 경로는 쉼표로 구분한다.','파일명·확장자·괄호·쉼표를 확인하고 Save All.'))

def student_constraints(d,p):
    d.frame('constraints에 XDC 직접 작성',items(['constraints를 펼치고 pins.xdc 우클릭 → Rename.','파일명: '+Path(p['constraints']).name,'핀 표와 코드 이미지를 보며 PACKAGE_PIN·IOSTANDARD·get_ports를 입력한다.','get_ports의 이름과 비트 번호를 자신이 작성한 RTL의 포트와 대조한다.','File → Save All. Vivado 또는 CLI 구현에는 이 파일을 직접 가져간다.'])+para('XDC는 Icarus 기능 시뮬레이션에서 사용하지 않는다. 파형 통과만으로 핀 배치까지 검증됐다고 판단하지 않는다.'))
    manifest=BASE/'student-code-captures.json'
    if manifest.exists():
        for panel in json.loads(manifest.read_text(encoding='utf-8')):
            if panel['source']==p['constraints']:
                d.frame('XDC 전체 코드 · '+str(panel['lines'][0])+'–'+str(panel['lines'][1])+'행',para(p['constraints']+' · 실제 VS Code 화면을 보며 직접 작성한다.')+'\\includegraphics[width=\\textwidth,height=4.2cm,keepaspectratio]{'+panel['image']+'}\\par\\vspace{0.18cm}'+para('핀 이름·포트 이름·대괄호·중괄호를 확인하고 저장한다.'))

def esc(value):
    return ''.join({'\\':r'\textbackslash{}','_':r'\_','&':r'\&','%':r'\%','$':r'\$','#':r'\#','^':r'\textasciicircum{}','~':r'\textasciitilde{}','{':r'\{','}':r'\}'}.get(c,c) for c in str(value))

TERMINAL_MACRO = r'\providecommand{\terminalbox}[1]{\par\vspace{0.15cm}{\setlength{\fboxsep}{7pt}\colorbox{black}{\parbox{\dimexpr\textwidth-14pt\relax}{\color{white}\ttfamily\fontsize{7}{9}\selectfont #1}}}\par\vspace{0.15cm}}'

def terminal(*commands):
    return '\\terminalbox{'+r'\\'.join(esc(line) for line in commands)+'}\n'

def para(*lines):
    return r'\par\vspace{0.22cm}'.join(esc(x) for x in lines)+r'\par'

def items(lines):
    return '\\begin{enumerate}\\setlength{\\itemsep}{0.22cm}\n'+''.join('\\item '+esc(x)+'\n' for x in lines)+'\\end{enumerate}\n'

def link(url,label):
    return '\\href{'+url+'}{'+esc(label)+'}'

def table(headers,rows):
    cols='|' .join('l' for _ in headers)
    return '\\begin{center}\\renewcommand{\\arraystretch}{1.45}\n\\begin{tabular}{'+cols+'}\n'+' & '.join(map(esc,headers))+r'\\\hline'+'\n'+''.join(' & '.join(map(esc,row))+r'\\'+'\n' for row in rows)+'\\end{tabular}\\end{center}\n'

def crop(name,box,height=3.2):
    # Original screenshot pixels are 1486x944 (Vivado) or 1202x802 (VS Code).
    x1,y1,x2,y2=box
    w,h=(1202,802) if name.startswith('vscode:') else (1486,944)
    filename=name.removeprefix('vscode:')
    trim=' '.join(f'{v*.75:g}bp' for v in [x1,h-y2,w-x2,y1])
    return ('\\par\\vspace{0.18cm}{\\centering\\includegraphics[width=\\textwidth,height='+str(height)+'cm,keepaspectratio,trim='+trim+',clip]{assets/modern-01/'+filename+'.png}\\par}\\vspace{0.16cm}\n')

class Deck:
    def __init__(self,label,title):
        self.label=label;self.pages=[];self.title=title
    def frame(self,title,body,label=None):
        self.pages.append('\\begin{frame}'+('[label='+label+']' if label else '')+'{'+esc(title)+'}\\relax\n\\small\n'+body+'\n\\end{frame}\n')
    def write(self,name):
        pre='\\input{shared/lab1_preamble.tex}\n\\renewcommand{\\labonehome}{\\hyperlink{'+self.label+'-contents}{\\contentsbutton}}\n\\renewcommand{\\legacySource}[1]{}\n\\hypersetup{pdftitle={'+esc(self.title)+'}}\n\\begin{document}\n\\begingroup\n\\renewcommand{\\small}{\\fontsize{9}{11}\\selectfont}\n'
        pre=pre.replace('\\begin{document}',TERMINAL_MACRO+'\n\\begin{document}')
        path=BASE/(name+'.tex');content='% !TEX program = xelatex\n'+pre+'\n'.join(self.pages)+'\\endgroup\n\\end{document}\n'
        if not path.exists() or path.read_text(encoding='utf-8')!=content:path.write_text(content,encoding='utf-8')
        return len(self.pages)+sum((BASE/'sections/legacy_01_logic_gates.tex').read_text(encoding='utf-8').count('\\begin{frame}')-1 for page in self.pages if '\\input{sections/legacy_01_logic_gates.tex}' in page)

def vcd_values(path,top,signals,sample_ns):
    text=path.read_text(errors='replace');scale=re.search(r'\$timescale\s+(\d+)\s*(fs|ps|ns|us|ms|s)',text)
    factor=int(scale[1])*{'fs':1e-6,'ps':1e-3,'ns':1,'us':1e3,'ms':1e6,'s':1e9}[scale[2]]
    scope=[];ids={};history={};now=0
    for line in text.splitlines():
        line=line.strip();parts=line.split()
        if line.startswith('$scope'):scope.append(parts[2])
        elif line.startswith('$upscope'):scope.pop()
        elif line.startswith('$var'):
            name=''.join(parts[4:-1]);key='.'.join(scope+[name]);ids[key]=(parts[3],int(parts[2]));history.setdefault(parts[3],[])
        elif line.startswith('#'):now=int(line[1:])*factor
        elif line[:1] in '01xXzZ' and len(line)>1:history.setdefault(line[1:],[]).append((now,line[0]))
        elif line[:1] in ['b','B']:
            val,code=line[1:].split();history.setdefault(code,[]).append((now,val))
    rows=[]
    for sample in sample_ns:
        row=[f'{sample:g}']
        for sig in signals:
            code,width=ids[top+'.'+sig];changes=history[code];idx=bisect.bisect_right([x[0] for x in changes],sample)-1
            value=changes[idx][1] if idx>=0 else 'x'
            row.append(value.zfill(width) if set(value.lower())<=set('01') else value)
        rows.append(row)
    return rows

def code_panels(d, source):
    for panel in (x for x in PANELS if x['source']==source):
        first,last=panel['lines']
        image='\\par\\vspace{0.15cm}{\\centering\\includegraphics[width=\\textwidth,height=3.9cm,keepaspectratio]{assets/lab1-circuits/'+panel['image']+'}\\par}\\vspace{0.18cm}\n'
        d.frame(panel['title'],para(Path(source).name+f' · {first}–{last}행 · 실제 VS Code 화면')+image+para(*panel['notes']))

def integrated_gui(d):
    for title,image,notes in [
        ('통합 프로젝트 · 계층 확인 1','hierarchy-a',['Design Sources의 lab1_integrated 왼쪽 화살표를 펼친다.','버튼·논리 게이트·전가산기·가산기·감산기·비교기 연결을 확인한다.']),
        ('통합 프로젝트 · 계층 확인 2','hierarchy-b',['아래로 스크롤해 MUX·DEMUX·인코더·디코더·7세그먼트·LCD를 확인한다.','RTL 14개 파일로 통합 top·10개 실험 회로·버튼·LCD를 구성한다. full_adder 아래의 반가산기도 포함한다.']),
        ('통합 프로젝트 · 구현 결과 읽기','build-runs',['아래 Design Runs에서 impl_1의 write_bitstream Complete!를 확인한다.','이 화면은 제작자가 배치 빌드한 결과를 GUI에서 연 기록이다. Methodology 경고 28개는 별도로 해석한다.']),
    ]:
        d.frame(title,'\\par\\vspace{0.2cm}{\\centering\\includegraphics[width=\\textwidth,height=3.5cm,keepaspectratio]{assets/integrated-gui/'+image+'.png}\\par}\\vspace{0.25cm}\n'+para(*notes))
    def shot(name,height):
        return '\\par\\vspace{0.15cm}{\\centering\\includegraphics[width=\\textwidth,height='+height+'cm,keepaspectratio]{assets/integrated-gui/'+name+'.png}\\par}\\vspace{0.2cm}\n'
    d.frame('통합 파형 · 전체 구간 보기',para('시뮬레이션 뒤 Untitled 1 탭을 누르고 오른쪽 위 사각형으로 파형 패널을 확대한다.','돋보기 +는 확대, −는 축소, 네 방향 화살표는 Zoom Fit이다.')+shot('wave-controls','0.65')+shot('wave-io','2.4')+para('위에서부터 clk·rst·mode_button·sw·led·seg_data다. 전체 종료는 72.43µs이며 버튼 입력 사이에 회로별 256개 벡터를 검사한다.','빠른 TB의 10ns 클록이다. 실물 보드의 1kHz 시간으로 해석하지 않는다.'))
    d.frame('통합 파형 · LCD 문자로 읽기',para('파형 목록을 아래로 스크롤해 completed_line1과 completed_line2를 찾는다.','첫 신호를 클릭하고 Shift+↓로 둘째 신호까지 선택한다. 우클릭 → Radix → ASCII를 누른다.')+shot('radix-parent','0.55')+shot('ascii-menu','1.6')+para('두 신호는 LCD 출력 버스에서 실제로 받은 바이트를 TB가 조립한 16문자다. 설정은 표시 형식만 바꾼다.'))
    d.frame('통합 파형 · 모드와 회로명 대조',para('두 줄이 보이는 상태에서 초반 파형을 클릭하고 돋보기 +를 두 번 눌러 확대한다.')+shot('lcd-strings','1.5')+para('위 줄은 completed_line1: MODE 01 → MODE 02 → MODE 03이다.','아래 줄은 completed_line2: AND OR XOR → FULL ADDER → 4 BIT ADDER다.','번호와 회로명이 함께 바뀌는지 확인한다. 초기화·리셋 및 나머지 모드도 TB가 비교하며 외부 LCD의 실측은 별도로 수행한다.'))
    d.frame('통합 프로젝트 · GUI 실행 검증',para('아래 Log 탭 → Simulation에서 검사 수와 종료 시각을 확인한다.')+shot('pass-log','1.2')+para('Run Simulation → Run Behavioral Simulation의 2,560개 PASS와 종료 72430ns를 실제 GUI에서 확인했다.','시뮬레이션을 정상 종료한 뒤 VCD를 다시 보관했다. 날짜·버전·공백을 제외한 모든 선언·시간·값이 사전 VCD와 마지막 72430ns까지 일치한다.')+link(example_url(next(p for p in PROJECTS if p['path']=='vivado_2026_1/11_integrated'))+'/evidence/historical-course/gui-simulation.json','통합 GUI 실행·파형 비교 기록'))

def individual_gui(d,c,p):
    evidence=LAB/p['path']/'evidence/historical-course/gui-simulation.json'
    if not evidence.exists():
        return
    result=json.loads(evidence.read_text(encoding='utf-8'))
    assert result['standalone_comparison']['status']=='PASS'
    prefix=f"{c['n']:02d}"
    def shot(name,height):
        return '\\par\\vspace{0.15cm}{\\centering\\includegraphics[width=\\textwidth,height='+str(height)+'cm,keepaspectratio]{assets/latest-gui/'+prefix+'-'+name+'.png}\\par}\\vspace{0.2cm}\n'
    notes={
        2:'70–80ns에서 a=b=cin=1이면 s=1, cout=1이다.',
        3:'310–320ns에서 a=1, b=f이면 s=0, cout=1이다. f는 16진수 15다.',
        4:'170–180ns에서 a=b=1이면 d=0, bor=0이다. 180–190ns의 1−2에서는 d=f, bor=1이다.',
        5:'160–170ns의 a=1, b=0과 170–180ns의 a=b=1을 비교한다. o의 세 비트는 대소 관계를 나타낸다.',
        6:'i=8인 320–360ns에서 s=0일 때만 z=1이다. 8은 이진수 1000이며 이 회로는 i[3−s]를 선택한다.',
        7:'i=1인 80–160ns에서 s가 0부터 7까지 바뀌며 o가 80부터 01까지 이동한다. 표시값은 16진수다.',
        8:'i=01과 i=03을 비교한다. 단일 비트 입력과 여러 비트 입력의 인코딩 규칙을 확인한다.',
        9:'a·b·c의 8개 조합에 따라 o의 한 비트만 1이 된다. 다중 비트 값은 16진수 표시다.',
        10:'80–90ns의 bcd=8에서 seg_data=fe다. 10–15 입력에 대응하는 A–F의 표시값도 확인한다.',
    }
    d.frame('이 회로의 실제 GUI 파형',para('Untitled 파형 탭 → 오른쪽 위 사각형으로 패널 확대 → Zoom Fit.','신호가 촘촘하면 관심 시간의 파형을 클릭하고 돋보기 +로 확대한다.')+shot('wave-crop',2.1)+para('위에서부터 '+', '.join(c['signals'])+' 순서다.',notes[c['n']],'전환 경계 대신 구간 중간에 커서를 놓고 사전 VCD와 대조한다.'))
    d.frame('이 회로의 GUI 실행·구현 확인',para('Log 탭 → Simulation에서 PASS·검사 수·종료 시각을 확인한다.')+shot('pass-crop',1.1)+para(f"실제 GUI 실행: {result['cases']}개 PASS, 종료 {result['end_ns']}ns. 정상 종료 후 전체 VCD가 사전 결과와 일치했다.")+shot('build-crop',1.3)+para('Design Runs의 impl_1: write_bitstream Complete!를 확인한다. 위 구현 화면은 기존 배치 빌드 결과를 GUI에서 연 기록이다.')+link(example_url(p)+'/evidence/historical-course/gui-simulation.json','GUI 실행·전체 파형 비교 근거'))

def prelude(d,c,p):
    label=d.label;ed=p['edition'];legacy=ed=='legacy'
    d.frame(f"{c['n']:02d} · {c['title']}",para('VS Code 사전 시뮬레이션 → '+('레거시 Vivado' if legacy or p.get('legacy_target') else 'Vivado 2026.1')+' → 보드 실험',c['rule'])+items(['템플릿을 clone하고 이 회로의 workspace를 연다.','예상값을 계산하고 RTL·TB·XDC를 직접 작성해 시뮬레이션한다.','Vivado 결과와 실제 보드 동작을 비교한다.','자신의 사진·영상·레포트를 GitHub에 연결한다.'])+para('작성일 2026. 09. 10. · 이해리'))
    d.frame('실습 목차',para('1부 · VS Code 사전 실습')+'\\navlink{'+label+'-setup}{새 창·workspace·확장·코드 열기}\\par\\vspace{0.2cm}\n\\navlink{'+label+'-sim}{예상값·작업 실행·로그·파형·실험 전 레포트}\\par\\vspace{0.4cm}\n'+para('2부 · Vivado 실습')+'\\navlink{'+label+'-vivado}{프로젝트·소스·top·시뮬레이션·핀·비트스트림}\\par\\vspace{0.4cm}\n'+para('3부 · 결과 정리')+'\\navlink{'+label+'-post}{보드·사진·영상·GitHub·실험 후 레포트}\\par\\vspace{0.35cm}\n'+link('04.LAB1_00_CONTENTS.pdf','전체 목차 PDF 열기'),label+'-contents')
    student_setup(d,p)
    if p.get('legacy_target'):
        modern_file=f"04.LAB1_{c['n']:02d}_{c['pdf']}_VIVADO.pdf"
        d.frame('VS Code 실습은 대응 최신판을 재사용',para(f"이 PDF의 사전 실습은 {c['n']:02d}번 최신판과 같은 RTL·자기검사 TB·실행 방법이다.",'실습 폴더는 이번 레거시용 이름으로 만들되, 같은 코드 이미지를 보고 직접 작성한다.','VS Code의 PASS·파형·실험 전 레포트 뒤에 이 PDF의 원본 Vivado 강의자료를 진행한다.','원본 testbench.v는 자극 순서·시간이 다를 수 있다. 동일 결과 비교에는 앞에서 작성한 자기검사 TB를 등록한다.')+link(modern_file,f"{c['n']:02d}번 VS Code 상세 실습 열기"))
    srcs=[Path(x).name for x in p['sources']]
    d.frame('입출력과 동작 규칙',para(c['ports'],c['rule'],c['board']),label+'-sim')
    d.frame('실행 전에 예상값 작성',table(['입력 또는 조건','예상 결과'],c['examples'])+para(c['focus'],'예상값을 계산한 근거를 자신의 말로 설명한다.'))
    if c['n']==1 and not legacy:
        d.frame('논리 게이트 RTL 직접 작성',para('src/logic_gate.v의 전체 내용을 입력하고 저장한다.')+crop('vscode:04-rtl',(375,90,1002,210),2.2)+para(c['rule']))
    elif c['n']==2 and not legacy:
        for module in ['half_adder','full_adder']:
            d.frame(module+' 연결 읽기',para('실제 배포 RTL을 VS Code에서 연 화면이다.')+'\\par\\vspace{0.25cm}\\includegraphics[width=\\textwidth,trim=265bp 410bp 0bp 28bp,clip]{assets/lab1-circuits/'+module+'-rtl.png}\n'+para('반가산기는 두 입력의 XOR를 합, AND를 carry로 출력한다.' if module=='half_adder' else '첫 반가산기의 합과 cin을 두 번째 반가산기에 연결한다. 두 carry를 OR로 합친다.'))
    elif not legacy and c['n'] in range(3,11):
        shot={3:'adder_4bit',4:'sub_4bit',5:'compare_4',6:'mux_4x1',7:'demux_1x8',8:'encoder8x3',9:'decoder3x8',10:'seg_decoder'}[c['n']]
        image_width='\\textwidth'
        rtl_notes=[c['rule']] if c['n']==10 else [c['rule'],'포트 선언·비트 폭·출력 연결을 짚어 설명한다. 저장소 소스를 복사해 사용해도 된다.']
        d.frame('RTL 구조를 설명한다',para('실제 배포 RTL을 VS Code에서 연 화면이다.','설계 top: '+p['top'])+'\\par\\vspace{0.25cm}\\includegraphics[width='+image_width+']{assets/lab1-circuits/'+shot+'-rtl-crop.png}\\par\\vspace{0.25cm}\n'+para(*rtl_notes)+link(example_url(p),'배포 소스 확인'))
    else:
        d.frame('RTL 구조를 설명한다',para('설계 top: '+p['top'],'RTL 파일: '+', '.join(srcs),c['rule'],'소스를 저장소에서 직접 열고 포트 선언·비트 폭·출력 연결을 짚어 설명한다. 저장소 소스를 복사해 사용해도 된다.')+link(example_url(p),'배포 소스 확인'))
    if legacy and c['n']==4:
        d.frame('원본 감산기의 borrow 보충',para('원본은 a>b일 때만 borrow=0으로 두어 a=b에서도 borrow=1이 된다.','original/sub_4bit.v는 원본 바이트를 보존한다. src/sub_4bit.v는 비교를 a>=b로 고친 보충 파일이다.','새 workspace의 sources에는 수정본을 등록한다. 원본 오류 검출 로그와 수정 후 256개 통과 결과를 구분한다.'))
    d.frame('테스트벤치와 통과 기준',para('시뮬레이션 top: '+p['simulation_top'],f"{c['cases']}개 입력 조합을 모두 검사한다. 각 자극은 10ns, 종료 시각은 {c['cases']*10}ns다.",'기대값과 실제 출력이 다르면 $fatal로 중단한다. 검사 횟수와 watchdog도 확인한다.','통과 문구: LAB1_PASS '+p['top']+' cases='+str(c['cases']),'원본 레거시 testbench.v와 별도의 자기검사 TB는 파일과 역할을 구분한다.'))
    if c['n']==1 and not legacy:
        for image,lines in [('tb-student-01','1–12행'),('tb-student-02','13–22행')]:
            d.frame('테스트벤치 직접 작성 · '+lines,para('sim/tb_logic_gate_modern.sv · 같은 파일에 순서대로 이어 입력한다.')+'\\includegraphics[width=\\textwidth,height=3.8cm,keepaspectratio]{assets/modern-01/'+image+'.png}\\par\\vspace{0.18cm}'+para('긴 오류 문자열은 화면 줄바꿈이다. 문자열 중간에 Enter를 넣지 않는다.'))
    else:code_panels(d,'common/tb/'+Path(p['testbench']).name)
    d.frame('저장 → Terminal → Run Task',para('File → Save All 다음 Terminal → Run Task...을 누른다.')+crop('vscode:06-tasks',(293,0,909,125),2.1)+items(['01 Check tools를 실행하고 도구 버전을 확인한다.','02 Simulate를 선택하고 종료까지 기다린다.','03 Open waveform으로 생성된 VCD를 연다.'])+para('작업이 없으면 올바른 .code-workspace를 열었는지 확인한다.'))
    logfile=LAB/p['path']/'evidence/standalone-simulation.txt'
    marker='LAB1_PASS '+p['top']+' cases='+str(c['cases'])
    measured=logfile.is_file() and marker in logfile.read_text(errors='replace')
    d.frame('실행 로그 확인',para('터미널과 build/sim/run-.../simulation.log에서 이번 실행을 확인한다.',marker if measured else '이 프로젝트의 실제 실행 결과는 검증표에서 확인한다.',f"정상 종료 시각: {c['cases']*10}ns. PASS 문구와 검사 수를 함께 확인한다.",'실패하면 이번 실행 폴더의 compile.log와 simulation.log에서 첫 오류를 찾는다.','코드 저장 → 02 Simulate 재실행 → 새 로그 확인 순서로 복귀한다.')+link(example_url(p),'프로젝트 검증 안내'))
    d.frame('VCD를 파형으로 열기',items(['03 Open waveform 또는 build/sim/wave.vcd를 연다.','텍스트로 열리면 탭 우클릭 → Reopen Editor With... → VaporView.','Netlist View에서 '+p['simulation_top']+'을 펼친다.','신호 '+', '.join(c['signals'])+'를 각각 두 번 눌러 추가한다.','Zoom to Fit를 누르고 Time Units를 ns로 맞춘다.','전환 경계 대신 구간 중간에 커서를 두고 값을 읽는다.']))
    d.frame('파형 화면의 읽는 순서',crop('vscode:08-vapor-wave',(352,37,1202,469),3.4)+para('위는 공통 파형 조작 예다. 이번 회로에서는 앞 장의 신호 이름을 선택한다.',c['focus'],'신호 이름 → 시간 구간 → 커서 값 → 예상 결과 순서로 비교한다.'))
    wave=LAB/p['path']/'build/sim/wave.vcd'
    if measured and wave.is_file():
        ns=sorted(set([0,1,min(3,c['cases']-1),c['cases']//2,c['cases']-1]))
        rows=vcd_values(wave,p['simulation_top'],c['signals'],[n*10+5 for n in ns])
        d.frame('실제 VCD의 구간 중간값',table(['시간(ns)']+c['signals'],rows)+para('이 표는 실행된 VCD에서 읽은 값이다. 다중 비트는 이진수다.','표의 시간으로 파형 커서를 옮겨 직접 대조하고, 추가 경계 조건도 확인한다.'))
    student_constraints(d,p)
    d.frame('실험 전 레포트',items(['목적·포트·비트 폭·예상표와 동작 원리를 설명한다.','소스와 TB 링크, 코드 커밋, 도구 버전을 남긴다.','입력 조합·기대값·자동 비교·종료 조건을 설명한다.','자신의 PASS 로그와 파형 원본·캡처를 첨부한다.','시간 구간별 값을 해석하고 예상값과 비교한다.','오류·수정·재실행, 보드에서 확인할 입력과 출력을 적는다.'])+para('교재 캡처를 자신의 실행 결과로 제출하지 않는다.'))

def pins(d,p):
    text=(LAB/p['path']/p['constraints']).resolve().read_text()
    rows=re.findall(r'set_property PACKAGE_PIN (\S+) \[get_ports\s+\{?([^}\]]+(?:\[\d+\])?)\}?\]',text)
    # XDC port names include square brackets; parse line-wise instead.
    rows=[]
    for line in text.splitlines():
        m=re.match(r'set_property PACKAGE_PIN (\S+) \[get_ports (.*)\]$',line.strip())
        if m:rows.append([m[2].strip('{}'),m[1]])
    for start in range(0,len(rows),6):
        d.frame('대상 부품·핀 제약'+(f' ({start//6+1})' if len(rows)>6 else ''),para('xc7s75fgga484-1 · IOSTANDARD=LVCMOS33')+table(['포트','PACKAGE_PIN'],rows[start:start+6])+para('XDC에서 포트·핀 번호를 대조한다. 다른 보드에는 그대로 쓰지 않는다.'))

def vivado(d,c,p):
    d.frame('Vivado GUI에서 이어서 실습',para('사전 시뮬레이션과 실험 전 레포트를 마친 뒤 Vivado 2026.1을 연다.','이후 단계는 메뉴와 버튼을 직접 누른다.','공통 클릭 화면은 첫 회로에서 실제 캡처했다. 이번 회로의 입력 파일과 top은 다음 슬라이드의 값을 따른다.')+link('04.LAB1_01_LOGIC_GATES_VIVADO.pdf','첫 회로의 상세 GUI 매뉴얼'),d.label+'-vivado')
    d.frame('File → Project → New...',crop('40-new-project-menu',(8,32,442,153),2.3)+para('New Project 안내에서 Next. Project name: '+p['top'],'Project location: 자신의 clone 폴더 / vivado','Create project subdirectory를 해제하고 Next. RTL Project와 Do not specify sources at this time을 선택한다.'))
    d.frame('정확한 부품 선택',crop('43-select-part',(233,332,773,521),3.1)+para('Parts에서 xc7s75fgga484-1 검색 → 정확히 같은 행 선택 → Next.','요약에서 Spartan-7, fgga484, -1을 확인하고 Finish.'))
    d.frame('RTL을 Design Sources에 추가',crop('46-design-kind',(344,362,795,461),2.1)+para('왼쪽 Add Sources → Add or create design sources → Next → Add Files.','등록할 RTL: '+', '.join(Path(x).name for x in p['sources']),'Copy sources into project를 해제하고 Finish. VS Code와 같은 원본을 참조한다.'))
    d.frame('Simulation Sources에 TB 추가',crop('50-simulation-kind',(344,363,795,461),2.1)+para('Add Sources → Add or create simulation sources → Next → Add Files.',Path(p['testbench']).name+'를 선택한다. sim_1을 유지한다.','Copy sources into project는 해제, Include all design sources for simulation은 체크 → Finish.'))
    d.frame('XDC를 Constraints에 추가',crop('53-constraints-kind',(344,363,795,461),2.1)+para('Add Sources → Add or create constraints → Next → Add Files.',Path(p['constraints']).name+' 선택 → Copy constraints files into project 해제 → Finish.','소스 중복 등록이나 잘못된 종류로 추가한 파일이 없는지 확인한다.'))
    d.frame('두 top을 구분한다',para('Design Sources의 top: '+p['top'],'Simulation Sources → sim_1의 top: '+p['simulation_top'],'Sources의 화살표를 눌러 계층을 펼친다. 굵은 이름이 top이다.','잘못 지정되었다면 올바른 모듈 우클릭 → Set as Top. 이미 top이면 해당 메뉴가 비활성인 것이 정상이다.','테스트벤치를 합성할 설계 top으로 지정하지 않는다.'))
    d.frame('Run Behavioral Simulation',crop('58-run-behavioral',(12,422,467,636),3.0)+para('Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration을 기다린다.','파형에서 신호를 선택하고 Zoom Fit, 시간 단위, 커서 값을 확인한다.','Tcl Console의 PASS 문구와 종료 시각을 확인한다. 오류면 Messages의 첫 오류로 돌아간다.'))
    sim=LAB/p['path']/'build/vivado-sim/simulation.log';marker='LAB1_PASS '+p['top']+' cases='+str(c['cases'])
    d.frame('VS Code 결과와 비교',para('두 실행은 같은 RTL과 자기검사 TB를 사용한다.',marker if sim.exists() and marker in sim.read_text(errors='replace') else 'Vivado 실행 상태와 근거 로그는 프로젝트 검증표에서 확인한다.','VS Code 로그: build/sim/run-.../. GUI 로그: vivado/'+p['top']+'.sim/sim_1/behav/xsim/.',c['focus'],'로그·파형을 서로 다른 이름으로 보관하고 네 가지 정보인 입력·출력·시간·검사 수를 비교한다.'))
    pins(d,p)
    d.frame('Run Synthesis',crop('62-run-synthesis',(10,604,260,704),2.1)+para('File → Close Simulation → OK. Flow Navigator → Run Synthesis.','Launch Runs: 기본 디렉터리, Launch runs on local host, PC 자원에 맞는 jobs → OK.','Synthesis successfully completed를 확인한다. 실패했으면 다음 단계로 넘어가지 않는다.'))
    d.frame('Run Implementation',crop('64-synthesis-complete',(558,302,918,491),2.8)+para('합성 완료 창에서 Run Implementation → OK. Launch Runs에서 OK.','완료 창을 닫았다면 Flow Navigator → Run Implementation.','Implementation successfully completed가 나올 때까지 기다린다.'))
    d.frame('Generate Bitstream',crop('66-implementation-complete',(558,302,918,491),2.8)+para('구현 완료 창에서 Generate Bitstream → OK → Launch Runs의 OK.','또는 Program and Debug → Generate Bitstream.','최종 상태 write_bitstream Complete!를 확인한다. 파일 생성과 보드 기록은 다른 단계다.'))
    result=LAB/p['path']/'build/build/result.json';status=json.loads(result.read_text())['status'] if result.exists() else '미실행'
    d.frame('생성 파일과 보고서',para('생성 bit: vivado/'+p['top']+'.runs/impl_1/'+p['top']+'.bit','제작 실행 결과와 증빙은 프로젝트의 evidence/validation.json과 README 검증표를 확인한다.','DRC 오류를 확인하고 CFGBVS / CONFIG_VOLTAGE 경고는 실제 보드 구성 전압과 대조한다.','1kHz 클록의 내부 타이밍과 지연 제약이 없는 외부 입출력을 구분한다.' if p['top']=='lab1_integrated' else '클록 없는 조합회로의 setup/hold NA를 타이밍 검증 완료로 해석하지 않는다.','사용한 커밋·bit 해시·DRC·타이밍 보고서를 결과와 함께 남긴다.'))

def post(d,c,p):
    if p['edition']=='opensource_cli':
        cli_post(d,c,p)
        return
    d.frame('실제 보드 연결',crop('70-auto-connect',(270,123,704,309),3.0)+para('Open Hardware Manager → Open target → Auto Connect.',c['board'],'장치가 없으면 보드 전원·USB JTAG·드라이버·VM USB 연결을 점검한다.'),d.label+'-post')
    d.frame('Program Device와 동작 확인',items(['연결된 장치 이름이 xc7s75인지 확인한다.','장치 우클릭 → Program Device.','이번 프로젝트의 '+p['top']+'.bit를 선택하고 Program.','기록 완료를 확인한 뒤 입력을 바꾸고 출력과 예상값을 비교한다.','기록 성공 화면과 실제 보드 동작은 각각 증빙한다.'])+para('제작 환경의 실제 보드 기록·촬영 검증 여부는 검증표를 따른다. 파일 생성만으로 보드 동작 성공을 선언하지 않는다.'))
    d.frame('사진과 시연 영상 촬영',para(c['board'],'사진에는 보드 연결과 입력·출력 위치가 함께 보이게 한다.','영상에는 입력을 조작하는 과정과 그에 따른 출력 변화를 담는다.','예상표의 정상·경계 조건을 직접 보여주고 회로 번호를 파일명에 적는다.','통합 영상이라면 각 회로의 타임스탬프를 레포트에서 연결한다.'))
    d.frame('GitHub 결과 정리',items(['reports/pre와 reports/post에 실험 전·후 레포트를 둔다.','evidence/vscode와 evidence/vivado에 로그·파형·캡처를 구분한다.','evidence/board/photos와 videos에 직접 촬영한 자료를 둔다.','큰 영상·bit는 배포 위치를 정하고 README와 레포트에서 연결한다.','웹에서 사진 표시와 영상 재생 또는 다운로드가 되는지 확인한다.'])+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/reports.md','레포트 양식·예시·GitHub 안내'))
    d.frame('실험 후 레포트',items(['Vivado 버전·part·top·핀 제약·코드 커밋을 기록한다.','VS Code와 Vivado의 입력·출력·시간·검사 수를 비교한다.','합성·구현·bit 경로와 경고·수정 사항을 설명한다.','장치 기록 화면·사진·영상과 해당 조건을 연결한다.','예상값·두 시뮬레이션·실측의 일치 또는 차이 원인을 해석한다.','미수행 항목은 미완료로 남기고 후속 확인을 적는다.'])+link('04.LAB1_00_CONTENTS.pdf','전체 목차 PDF')+r'\quad'+link(example_url(p),'프로젝트로 돌아가기'))

def cli_post(d,c,p):
    guide='https://trabucayre.github.io/openFPGALoader/guide/first-steps.html'
    d.frame('openFPGALoader 설치',para('bit 생성과 FPGA 기록은 별도 단계다. macOS는 아래 명령을 사용한다.')+terminal('brew install openfpgaloader')+para('Windows MSYS2 UCRT64 환경에서는 다음 명령을 사용한다.')+terminal('pacman -S mingw-w64-ucrt-x86_64-openFPGALoader')+para('Linux는 배포판 패키지 또는 공식 빌드 안내를 따른다. 설치한 환경에서 확인한다.')+terminal('openFPGALoader --help')+link(guide,'공식 설치·기록 안내'),d.label+'-post')
    d.frame('보드와 JTAG 케이블 확인',items(['보드 전원과 USB JTAG 케이블을 연결한다.','openFPGALoader --list-cables로 지원 케이블 식별자를 확인한다.','openFPGALoader --list-boards로 지원 보드 식별자를 확인한다.','보드가 목록에 없으면 실제 연결된 JTAG 케이블의 식별자를 -c에 지정한다.','VM 또는 WSL에서는 해당 실행 환경에 USB 장치가 연결되어 있는지 확인한다.'])+para('다른 FPGA 보드 이름을 임의로 선택하지 않는다. 보드 모델과 케이블 모델은 별개의 정보다.'))
    d.frame('CLI로 생성한 bit를 SRAM에 기록',para('아래 MY_CABLE은 직전 단계에서 확인한 실제 케이블 식별자로 바꾼다.')+terminal('openFPGALoader -c MY_CABLE build/cli/lab1_integrated.bit')+para('자신의 소스로 만든 최신 bit인지 경로·생성 로그·해시를 확인한 뒤 실행한다.','터미널의 장치 정보·진행률·종료 코드와 최종 상태를 보관한다.','기본 기록은 SRAM이며 전원을 끄면 사라진다. -f는 Flash 기록 옵션이므로 이 SRAM 실습 명령에는 넣지 않는다.')+link(guide,'SRAM·Flash와 케이블 옵션'))
    d.frame('기록 뒤 모드·LCD 동작 확인',para(c['board'],'reset으로 01을 확인하고 버튼을 짧게·길게 눌러 한 번씩 전환되는지 본다.','10 다음 01로 돌아오는지, LCD 번호·이름이 실제 선택 회로와 일치하는지 확인한다.','모드마다 DIP를 조작하여 예상표의 정상·경계 조건과 LED·7세그먼트 출력을 비교한다.','기록 성공 로그와 실제 회로 동작을 각각 증빙한다.'))
    d.frame('CLI 실험 후 레포트와 GitHub',items(['Icarus·Yosys·nextpnr·프레임 변환·openFPGALoader 버전과 실행 명령을 기록한다.','RTL·TB·XDC 커밋, 정확한 part, DB 커밋과 bit 해시를 연결한다.','evidence/cli에 합성·배치배선·bit 생성 로그를 보관한다.','evidence/programming에 케이블·장치·기록 로그와 캡처를 보관한다.','보드 사진과 10개 모드 시연 영상에 조건·타임스탬프를 붙인다.','사전 파형·예상값·실측 차이를 해석하고 reports/post에서 증빙을 링크한다.'])+link('04.LAB1_00_CONTENTS.pdf','전체 목차 PDF'))

def legacy_pages(d,c):
    d.frame('원문 Vivado 실습으로 이동',para('이후 원문은 원본의 사진·문구·순서를 유지한다.','배포 프로젝트는 Vivado 2020.1 원본 XPR 형식을 기반으로 상대경로를 정리했다. 구버전 실행 검증은 별도로 확인한다.','수업에서는 원문의 합성·구현에 앞서 자기검사 TB로 Behavioral Simulation을 먼저 실행한다.','원본 testbench.v와 검증용 TB의 입력 순서·실행 시간은 서로 다를 수 있다.'),d.label+('-original-intro' if c['n']==1 else '-vivado'))
    if c['n']==4:
        d.frame('원본 감산기의 동등 입력 보충',para('원본 a>b 비교는 a=b에서도 borrow=1로 출력한다. 원본 강의 화면은 그대로 보존한다.','정상적인 감산에서 a=b이면 borrow=0이다. 사전 실습의 a<b와 같은 의미가 되도록 원본 if 비교를 a>=b로 수정한다.','a=b, a<b, a>b를 자기검사 TB로 다시 확인하고 원본·수정본 차이를 실험 후 레포트에 적는다.'))
    if c['n']==1:
        # Existing reconstruction retains every source page and its separate image crops.
        d.pages.append('\\input{sections/legacy_01_logic_gates.tex}\n')
        return
    for n in range(c['range'][0],c['range'][1]+1):
        image=f"assets/legacy-{c['n']:02d}/page-{n:03d}.png"
        d.pages.append('\\begin{frame}[plain,label='+d.label+'-p'+str(n)+']\\relax\n\\begin{tikzpicture}[remember picture,overlay]\n\\node[inner sep=0pt] at (current page.center) {\\includegraphics[width=\\paperwidth,height=\\paperheight,keepaspectratio]{'+image+'}};\n\\node[anchor=west] at ([xshift=0.65cm,yshift=0.52cm]current page.south west) {\\labonehome};\n\\node[anchor=east,text=gray,font=\\scriptsize] at ([xshift=-0.57cm,yshift=0.52cm]current page.south east) {\\insertframenumber};\n\\end{tikzpicture}\n\\end{frame}\n')

def integrated_prelude(d,p):
    cli=p['edition']=='opensource_cli';label=d.label
    d.frame('버튼·LCD 통합 실습',para('VS Code 사전 시뮬레이션 → '+('오픈소스 CLI' if cli else 'Vivado 2026.1')+' → 보드 실험','같은 RTL에 10개 회로를 넣고 버튼으로 선택한다. LCD에 모드 번호와 회로 이름을 표시한다.','작성일 2026. 09. 10. · 이해리')+items(['먼저 2,560개 입력과 버튼·LCD 동작을 검사한다.','합성·배치배선·비트스트림을 생성한다.','보드에서 모드를 순환하고 사진·영상으로 설명한다.']))
    d.frame('통합 실습 목차',para('1부 · VS Code 사전 시뮬레이션')+'\\navlink{'+label+'-setup}{clone·새 창·workspace·실행·파형}\\par\\vspace{0.4cm}\n'+para('2부 · 통합 회로 이해')+'\\navlink{'+label+'-modes}{10개 모드·버튼·LCD·보드 연결}\\par\\vspace{0.4cm}\n'+para('3부 · 구현과 결과')+'\\navlink{'+label+'-vivado}{'+('CLI 설치·실행·검증 범위' if cli else 'Vivado GUI·핀·합성·구현·bit')+'}\\par\\vspace{0.2cm}\n\\navlink{'+label+'-post}{보드·사진·영상·실험 후 레포트}\\par\\vspace{0.3cm}\n'+link('04.LAB1_00_CONTENTS.pdf','전체 목차 PDF'),label+'-contents')
    student_setup(d,p)
    d.frame('통합에 포함할 개별 회로',para('01–10번에서 작성한 회로를 src에 모아 통합 top에 연결한다. 아래의 코드 화면도 그대로 재사용한다.','full_adder.v와 half_adder.v는 함께 필요하다. 통합 RTL·버튼·LCD까지 합성 파일은 총 14개다.','이미 작성한 파일은 복사해도 되며 simulation.json의 sources에 14개를 모두 등록한다.')+link('04.LAB1_00_CONTENTS.pdf','개별 회로별 상세 설명으로 이동'))
    for name in ['logic_gate','half_adder','full_adder','adder_4bit','sub_4bit','compare_4','mux_4x1','demux_1x8','encoder8x3','decoder3x8','seg_decoder']:
        if name=='logic_gate':body=crop('vscode:04-rtl',(375,90,1002,210),2.2)
        elif name in ['half_adder','full_adder']:
            body='\\includegraphics[width=\\textwidth,trim=265bp 410bp 0bp 28bp,clip]{assets/lab1-circuits/'+name+'-rtl.png}'
        else:body='\\includegraphics[width=\\textwidth,height=3.8cm,keepaspectratio]{assets/lab1-circuits/'+name+'-rtl-crop.png}'
        d.frame('개별 RTL 재사용 · '+name,para('src/'+name+'.v · 전체 코드를 입력하거나 앞서 작성한 같은 파일을 복사한다.')+body+'\\par\\vspace{0.18cm}'+para('모듈 이름과 입출력 폭을 유지하고 File → Save All.'))
    for source in ['rtl/lab1_integrated.v','rtl/button_onepulse.v','rtl/lcd_modes.v','tb/tb_lab1_integrated.sv']:
        code_panels(d,'common/'+source)
    d.frame('세 작업을 순서대로 실행',crop('vscode:06-tasks',(293,0,909,125),2.1)+items(['Terminal → Run Task... → 01 Check tools.','02 Simulate → 종료까지 기다린다.','터미널과 build/sim/run-.../simulation.log를 확인한다.','LAB1_PASS lab1_integrated cases=2560을 확인한다.','03 Open waveform으로 wave.vcd를 연다.'])+para('모든 workspace의 사전 시뮬레이션은 Icarus Verilog다. SIMULATED와 TB의 실제 검사 결과를 구분한다.'))
    d.frame('통합 테스트의 검사 범위',para('10개 모드 × DIP 256개 = 2,560개 출력 비교.','reset → MODE 01, 짧은 바운스 무시, 길게 눌러도 한 번만 전환, 10→01 순환을 검사한다.','LCD 초기 명령과 외부 버스에서 완성된 두 줄의 번호·이름을 비교한다.','TB는 10ns 클록, 디바운스 4클록, 전원 대기 5클록으로 시간을 줄인다. 실제 합성은 1kHz 보드 설정이다.','Icarus 검사 종료: 72430ns. 실제 보드의 전압·LCD 연결은 별도로 확인한다.'))
    d.frame('VaporView에서 통합 파형 읽기',items(['wave.vcd가 텍스트면 탭 우클릭 → Reopen Editor With... → VaporView.','Netlist에서 tb_lab1_integrated를 펼친다.','clk, rst, mode_button, sw, led, seg_data를 추가한다.','dut 안의 mode와 lcd_e, lcd_rs, lcd_rw, lcd_data를 추가한다.','Zoom to Fit 뒤 모드가 바뀌는 구간을 확대한다.','버튼 입력부터 모드 변경까지의 지연과 LCD 한 화면 갱신을 구분한다.']))
    student_constraints(d,p)
    d.frame('실험 전 레포트에 넣을 것',items(['모드별 예상 입력·출력과 비트 순서를 표로 작성한다.','10개 회로·버튼·LCD 파일의 역할을 설명한다.','PASS 로그, VCD, 모드 전환 및 LCD 파형 캡처를 연결한다.','TB에서 줄인 시간과 실제 1kHz 설정을 구분한다.','실험에서 확인할 버튼·LCD·DIP·LED 장면을 계획한다.'])+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/reports.md','레포트 양식과 예시'))
    d.frame('통합 구조와 입력 배치',para('lab1_integrated → 10개 조합회로 + button_onepulse + lcd_modes.','clk=B6(1kHz), KEY1=reset, KEY2=mode_button.','DIP1–8은 sw[7:0], LED1–8은 led[7:0]에 대응한다.','개별 실습의 KEY 입력은 통합본에서 DIP로 옮겨 모드 버튼과 충돌하지 않게 한다.','단일 7세그먼트는 모드 10에서만 동작한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/integrated.md','통합 동작 명세와 핀표'),label+'-modes')
    mode_rows=[('01','a=DIP1, b=DIP2','LED1=AND, 2=OR, 3=XOR'),('02','a,b,cin=DIP1,2,3','LED1=carry, 2=sum'),('03','a=DIP1–4, b=DIP5–8','LED1=carry, 2–5=sum'),('04','a=DIP1–4, b=DIP5–8','LED1=borrow, 2–5=diff'),('05','a=DIP1–4, b=DIP5–8','LED1=큼, 2=같음, 3=작음'),('06','i=DIP1–4, s=DIP7–8','LED1=i[3-s]'),('07','i=DIP1, s=DIP6–8','s=0→LED1, s=7→LED8'),('08','DIP1–8 중 하나만 1','LED1–3: DIP1→0, DIP8→7'),('09','abc=DIP6,7,8','0→LED8, 7→LED1'),('10','hex=DIP5–8','a–dp 패턴, 1이면 점등')]
    for n in range(0,10,5):d.frame('모드별 조작 '+str(n+1)+'–'+str(n+5),table(['모드','입력','출력'],mode_rows[n:n+5])+para('사용하지 않는 LED 비트는 0이다. reset하면 모드 01.'))
    d.frame('버튼을 길게 누르면',para('2단 동기화 → 안정된 입력 20클록 확인 → 상승 시 1클록 펄스.','1kHz에서 약 20ms 안정 시간에 동기화 지연이 추가된다.','누른 채 유지하면 한 번만 바뀐다. 뗀 뒤 다시 눌러야 다음 모드가 된다.','모드 10 다음은 01. reset은 즉시 01로 돌아간다.','실험 영상에서 짧게 누르기·길게 누르기·순환을 각각 보여준다.'))
    d.frame('LCD가 표시되는 과정',para('전원 대기 50ms → 38,38,38,0C,06 초기 명령 → 두 줄 반복 갱신.','첫 줄 MODE 01…MODE 10, 두 번째 줄 회로 이름.','E high는 1ms, 바이트 간격은 최소 4ms. 첫 초기 명령 간격은 더 길다.','한 화면 시작 때 모드를 저장하여 두 줄이 다른 모드로 섞이지 않게 한다.','새 모드는 현재 전송을 마친 뒤 갱신되므로 잠깐 기다리고 읽는다.'))

def cli_steps(d,p):
    d.frame('CLI 실행 환경',para('macOS ARM64 공식 바이너리 배포를 확인하고 WSL Ubuntu-26.04에서 Linux x86-64 바이너리로 실행했다.','APIO 1.5.1, OSS CAD Suite 2026.08.19, openXC7 2026.08.20.','Yosys → nextpnr → frames → bit까지 정확한 S75로 성공했다.','Mac 직접 실행과 실제 보드 프로그래밍은 이 제작 검증에 포함하지 않는다.')+link('https://github.com/FPGAwars/tools-openxc7/releases/tag/2026-08-20','공식 ARM64·Linux 배포'),d.label+'-vivado')
    d.frame('도구 설치',para('macOS·WSL의 Bash/Zsh 터미널에서 실행한다.')+terminal('python3 -m venv ~/.local/share/fpga-apio','source ~/.local/share/fpga-apio/bin/activate','pip install apio==1.5.1','apio packages install')+para('WSL에 venv가 없으면 먼저 python3-venv를 설치한다.','macOS는 darwin-arm64, WSL은 linux-x86-64 배포를 사용한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/cli.md','설치·실행 명령 전체'))
    d.frame('도구 경로 확인',terminal('export PATH="$HOME/.apio/packages/oss-cad-suite/bin:$PATH"','export PATH="$HOME/.apio/packages/openxc7/bin:$PATH"','yosys --version','nextpnr-xilinx --version')+para('새 터미널에는 PATH 설정을 다시 적용한다.','LD_LIBRARY_PATH로 두 묶음의 lib를 섞지 않는다. 배포 래퍼가 자신의 라이브러리를 선택한다.'))
    d.frame('정확한 S75 데이터 준비',para('대상 부품은 xc7s75fgga484-1이다.','upstream PR 15가 S75를 올바른 S100 fabric에 연결한다. S75와 같은 실리콘 구조를 공유하는 매핑이며 부품명·IDCODE는 S75다.','해당 fgga484 패키지의 실제 338개 I/O 핀을 적용한다. 학생은 Vivado를 설치·실행할 필요가 없다.','준비 도구는 공개 DB 커밋과 핀 표 해시를 고정하고 모두 검사한다.')+link('https://github.com/openXC7/prjxray-db/pull/15','데이터 수정의 근거'))
    d.frame('도구 보조 파일 받기',para('아래는 회로 프로젝트와 별개인 도구 데이터 폴더다.')+terminal('mkdir -p ~/fpga-cli/lab1-tools','cd ~/fpga-cli/lab1-tools','repo=fpga-lab-example-opensource-cli-integrated','base=https://raw.githubusercontent.com/Glaysia/$repo/v2.0.1/tools','curl --fail --location "$base/prepare_s75.py" -o prepare_s75.py','pins=xc7s75fgga484-1-package-pins.csv','curl --fail --location "$base/$pins" -o "$pins"')+para('고정된 보조 도구 태그는 v2.0.1, 학생 빈 템플릿 태그는 v2.0.0이다.'))
    d.frame('S75 chipdb 생성',terminal('python3 prepare_s75.py')+para('다운로드·bbaexport·bbasm 종료를 기다린다.','~/fpga-cli/lab1-s75/prepared.json에서 part와 338개 핀, DB 커밋·chipdb 해시를 확인한다.','실패하면 같은 폴더의 export.log·bbasm.log를 읽는다. 메모리 부족일 때 다른 무거운 앱을 닫고 다시 실행한다.','이후 VS Code의 학생 프로젝트 터미널로 돌아간다.'))
    d.frame('내 프로젝트에서 사전 검사',para('clone한 workspace에서 RTL 14개·TB·XDC·simulation.json을 직접 작성한다.','프로젝트 루트는 src·sim·constraints가 있는 폴더다.')+terminal('python3 tools/lab1.py simulate','mkdir -p build/cli')+para('2,560개 입력 검사와 버튼·LCD 검사를 확인한다.','실험 전 레포트의 예상값·로그·파형을 저장한 뒤 합성으로 이동한다.'))
    d.frame('합성 명령 파일을 직접 작성',para('Explorer의 PROJECT 우클릭 → New File → synth.ys. 다음 네 줄을 작성하고 저장한다.')+terminal('read_verilog src/*.v','synth_xilinx -family xc7 -top lab1_integrated','write_json build/cli/design.json','stat')+para('src에는 합성할 RTL만 두고 TB는 sim에 둔다.'))
    d.frame('Yosys 실행과 결과 읽기',terminal('yosys -l build/cli/synthesis.log -s synth.ys')+para('오류 없이 끝나는지와 build/cli/design.json의 갱신을 확인한다.','stat의 셀 종류·개수를 읽고 top이 lab1_integrated인지 확인한다.','합성 로그를 evidence/cli에 보관한다. 실패했으면 원인을 수정하고 이 명령부터 다시 실행한다.'))
    d.frame('nextpnr 배치배선',terminal('chip="$HOME/fpga-cli/lab1-s75/xc7s75fgga484-1.bin"','db="$HOME/fpga-cli/lab1-s75/prjxray-db/spartan7"','part=xc7s75fgga484-1','nextpnr-xilinx --chipdb "$chip" '+chr(92),'  --xdc constraints/lab1_integrated.xdc '+chr(92),'  --json build/cli/design.json --fasm build/cli/design.fasm '+chr(92),'  --freq 0.001 --log build/cli/place-route.log')+para('B6의 1kHz를 MHz로 표현하면 0.001이다. XDC와 같은 클록이다.','K4/B6 핀 오류가 나면 이전 S50 기반 chipdb를 사용했는지 확인한다.'))
    d.frame('프레임 변환',terminal('fasm2frames --db-root "$db" --part "$part" '+chr(92),'  build/cli/design.fasm build/cli/design.frames')+para('앞 장과 같은 터미널을 사용한다. db와 part 변수를 유지한다.','배치배선이 성공한 새 design.fasm을 사용한다.','종료 코드 0과 design.frames의 갱신을 확인한다.','해당 S75 DB와 다른 부품의 part.yaml을 섞지 않는다.'))
    d.frame('bit 파일 생성',terminal('xc7frames2bit --part_file "$db/$part/part.yaml" '+chr(92),'  --part_name "$part" --frm_file build/cli/design.frames '+chr(92),'  --output_file build/cli/lab1_integrated.bit')+para('build/cli/lab1_integrated.bit가 이번 실행으로 생성됐는지 확인한다.','실행 명령·종료 코드·파일 크기·생성 시각을 실험 후 레포트에 보관한다.','제작 검증에서는 3,686,926바이트가 생성됐다.'))
    d.frame('생성한 bit 다시 읽기',terminal('bitread --part_file "$db/$part/part.yaml" -C -z -y '+chr(92),'  -o build/cli/bits.txt build/cli/lab1_integrated.bit')+para('체크섬 검사와 Number of configuration frames: 9104, DONE을 확인한다.','이 검사는 파일 구조를 확인한다. 실제 장치 기록·LCD·버튼 동작은 다음 실험 단계에서 확인한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/cli-pr15-evidence/bitread.txt','제작 실행의 9,104프레임 읽기 로그'))
    d.frame('검증 결과와 다음 실험',para('Icarus 통합 자기검사 2,560개 통과.','Yosys·nextpnr·fasm2frames·xc7frames2bit 종료 코드 모두 0.','정확한 S75 bit 생성 및 9,104프레임 체크섬 검사 통과.','소스·XDC·DB·chipdb 해시와 실행 로그를 공개했다.','다음은 openFPGALoader로 실제 장치에 기록하고 모드·LCD·입출력을 사진과 영상으로 검증한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/cli.md','전체 명령·근거·기록 절차'))
    pins(d,p)


def overview(inventory):
    d=Deck('lab1','LAB1 목차와 공통 안내')
    d.frame('LAB 1 · 조합회로 실습',para('전자전기컴퓨터설계실험Ⅱ','VS Code에서 먼저 검증하고, Vivado와 보드에서 확인한다.','개별 회로 10개 · 레거시 10개 · 통합 2개','작성일 2026. 09. 10. · 이해리')+link('https://github.com/Glaysia/fpga-lab-template','학생용 템플릿 저장소'))
    d.frame('전체 목차',para('A · Vivado 2026.1')+'\\navlink{lab1-modern}{개별 회로 01–10}\\quad'+link('04.LAB1_10A_INTEGRATED_VIVADO.pdf','버튼·LCD 통합')+'\\par\\vspace{0.45cm}\n'+para('B · 오픈소스 CLI')+link('04.LAB1_10B_INTEGRATED_CLI.pdf','macOS ARM64 배포·WSL 실행·통합 프로젝트')+'\\par\\vspace{0.45cm}\n'+para('C · 레거시 Vivado')+'\\navlink{lab1-legacy}{원본 교안과 개별 회로 10개}\\par\\vspace{0.45cm}\n\\navlink{lab1-reports}{실험 전·후 레포트와 제출}\\quad\\navlink{lab1-start}{시작·설치·PDF 사용법}', 'lab1-contents')
    d.frame('시작과 자료 사용법',para('ZIP을 모두 푼 뒤 같은 폴더에 PDF를 둔다.','각 PDF 좌하단 목차 버튼은 그 PDF 2쪽으로 이동한다.','다른 PDF 링크가 뷰어에서 열리지 않으면 같은 폴더의 해당 파일을 직접 연다.','VS Code 사전 시뮬레이션 → 실험 전 레포트 → Vivado/CLI → 보드 → 실험 후 레포트 순서다.')+link('01.vivado_2026_1_설치_매뉴얼.pdf','Vivado 설치')+r'\quad'+link('02.vscode_verilog_환경설정_매뉴얼.pdf','VS Code 환경설정'),'lab1-start')
    for ed,label,title in [('vivado_2026_1','lab1-modern','A · Vivado 2026.1'),('legacy','lab1-legacy','C · 레거시 Vivado')]:
        if ed=='legacy':
            d.frame('통합 프로젝트와 제작 검증',para('KEY1은 reset, KEY2는 다음 모드. DIP로 입력하고 LED·LCD·7세그먼트로 확인한다.','VS Code 작업은 도구 확인·시뮬레이션·파형의 세 가지다. Vivado에서는 GUI를 직접 누른다.')+link('04.LAB1_10A_INTEGRATED_VIVADO.pdf','Vivado 통합')+r'\quad'+link('04.LAB1_10B_INTEGRATED_CLI.pdf','CLI 통합')+r'\par\vspace{0.4cm}'+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/validation.md','제작 검증 현황·로그·미완료 항목'))
        for start in [0,5]:
            body=''
            for c in CIRCUITS[start:start+5]:
                n=c['n']+(10 if ed=='legacy' else 0);fn=f"04.LAB1_{n:02d}_{c['pdf']}_{'LEGACY' if ed=='legacy' else 'VIVADO'}.pdf"
                body+=link(fn,f"{c['n']:02d} · {c['title']}")+r'\par\vspace{0.35cm}'+'\n'
            d.frame(title+f' · {start+1:02d}–{start+5:02d}',body,label if start==0 else None)
    d.frame('실험 전 레포트',items(['목적·포트·예상표와 소스·TB를 설명한다.','VS Code 새 창·workspace·도구 버전을 기록한다.','Check tools → Simulate → Open waveform을 수행한다.','로그·파형 캡처·구간별 값과 해석을 연결한다.','오류·수정·재실행과 보드 실험 계획을 적는다.'])+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/reports.md','양식·첫 회로 예시·GitHub 안내'),'lab1-reports')
    d.frame('실험 후 레포트',items(['Vivado 시뮬레이션을 사전 결과와 비교한다.','합성·구현·bit·DRC·타이밍 결과를 기록한다.','실제 장치에 기록하고 입력·출력을 확인한다.','사진과 조작 영상을 GitHub 레포트에 연결한다.','예상값·두 시뮬레이션·실측의 차이를 설명한다.'])+para('미수행 항목을 실제 수행 결과로 작성하지 않는다.'))
    d.write('04.LAB1_00_CONTENTS')

def main():
    inventory=[{'file':'04.LAB1_01_LOGIC_GATES_VIVADO','pages':65,'project':'vivado_2026_1/01_logic_gates','hand_authored':True}]
    for c in CIRCUITS:
        for ed in ['vivado_2026_1','legacy']:
            if c['n']==1 and ed=='vivado_2026_1':continue
            p=next(p for p in PROJECTS if p['path']==ed+'/'+c['slug'])
            modern=ed=='vivado_2026_1';number=c['n'] if modern else c['n']+10
            name=f"04.LAB1_{number:02d}_{c['pdf']}_{'VIVADO' if modern else 'LEGACY'}"
            d=Deck(('modern-' if modern else 'legacy-')+f"{c['n']:02d}",c['title'])
            if modern:prelude(d,c,p)
            else:
                shared=dict(next(q for q in PROJECTS if q['path']=='vivado_2026_1/'+c['slug']))
                shared.update(legacy_target=True,student_folder='lab1_legacy_'+c['slug'])
                prelude(d,c,shared)
            if modern:
                vivado(d,c,p)
                individual_gui(d,c,p)
            else:legacy_pages(d,c)
            post(d,c,p)
            if c['n']==1:
                d.pages[-1]=d.pages[-1].replace('\\small','\\hypertarget{lab1-reports}{}\\small',1)
            count=d.write(name);inventory.append({'file':name,'pages':count,'project':p['path']})
    for ed in ['vivado_2026_1','opensource_cli']:
        p=next(p for p in PROJECTS if p['edition']==ed and p['top']=='lab1_integrated')
        cli=ed=='opensource_cli';name='04.LAB1_'+('10B_INTEGRATED_CLI' if cli else '10A_INTEGRATED_VIVADO')
        d=Deck('integrated-cli' if cli else 'integrated-vivado','버튼·LCD 통합 실습')
        integrated_prelude(d,p)
        c={'cases':2560,'focus':'모드 전환·버튼·LCD와 2,560개 입력 결과를 비교한다.','board':'KEY1=reset, KEY2=다음 모드. DIP1–8=sw[7:0]. LED1–8=led[7:0].'}
        if cli:cli_steps(d,p)
        else:
            vivado(d,c,p)
            integrated_gui(d)
        post(d,c,p)
        inventory.append({'file':name,'pages':d.write(name),'project':p['path']})
    overview(inventory)
    (BASE/'series-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(inventory,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
