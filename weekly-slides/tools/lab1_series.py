"""Generate editable LAB1 TeX from circuit metadata and measured simulation files."""
from pathlib import Path
import json, re, bisect

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'example/fpga_projects_hdl/LAB1'
BASE = ROOT / 'weekly-slides/weekly-slides/LAB1_FPGA_0914'
CIRCUITS = json.loads((LAB/'docs/circuits.json').read_text(encoding='utf-8'))
PROJECTS = json.loads((LAB/'projects.json').read_text(encoding='utf-8'))
COURSE = 'https://github.com/Glaysia/ece2_26_2_2/blob/daily/0910/'
TEMPLATE = 'https://github.com/Glaysia/fpga-lab-template/tree/main/'

def esc(value):
    return ''.join({'\\':r'\textbackslash{}','_':r'\_','&':r'\&','%':r'\%','$':r'\$','#':r'\#','{':r'\{','}':r'\}'}.get(c,c) for c in str(value))

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

def prelude(d,c,p):
    label=d.label;ed=p['edition'];legacy=ed=='legacy'
    d.frame(f"{c['n']:02d} · {c['title']}",para('VS Code 사전 시뮬레이션 → '+('레거시 Vivado' if legacy else 'Vivado 2026.1')+' → 보드 실험',c['rule'])+items(['템플릿을 clone하고 이 회로의 workspace를 연다.','예상값·코드·테스트벤치를 읽고 시뮬레이션한다.','Vivado 결과와 실제 보드 동작을 비교한다.','자신의 사진·영상·레포트를 GitHub에 연결한다.'])+para('작성일 2026. 09. 10. · 이해리'))
    d.frame('실습 목차',para('1부 · VS Code 사전 실습')+'\\navlink{'+label+'-setup}{새 창·workspace·확장·코드 열기}\\par\\vspace{0.2cm}\n\\navlink{'+label+'-sim}{예상값·작업 실행·로그·파형·실험 전 레포트}\\par\\vspace{0.4cm}\n'+para('2부 · Vivado 실습')+'\\navlink{'+label+'-vivado}{프로젝트·소스·top·시뮬레이션·핀·비트스트림}\\par\\vspace{0.4cm}\n'+para('3부 · 결과 정리')+'\\navlink{'+label+'-post}{보드·사진·영상·GitHub·실험 후 레포트}\\par\\vspace{0.35cm}\n'+link('04.LAB1_00_CONTENTS.pdf','전체 목차 PDF 열기'),label+'-contents')
    d.frame('준비할 프로그램',para('Git·Python 3·VS Code·slang-server·VaporView를 준비한다.','Vivado GUI를 열기 전에도 XSim 도구가 필요하므로 Vivado는 미리 설치한다.','git --version / python --version / code --version','vivado -version / xvlog --version / xelab --version / xsim --version','명령이 없으면 설치와 PATH 또는 VIVADO_BIN을 확인하고 VS Code를 다시 연다.')+link('01.vivado_2026_1_설치_매뉴얼.pdf','Vivado 설치 PDF')+r'\quad'+link('02.vscode_verilog_환경설정_매뉴얼.pdf','VS Code 환경설정 PDF'),label+'-setup')
    d.frame('별도 템플릿 clone',para('PowerShell에서 실습 폴더를 둘 위치로 이동한 뒤 실행한다.','git clone https://github.com/Glaysia/fpga-lab-template.git','cd fpga-lab-template','자신의 저장소를 만들려면 GitHub의 Use this template → Create a new repository를 사용하고 자신의 주소를 clone한다.')+link(TEMPLATE,'학생용 템플릿 열기'))
    d.frame('File → New Window',para('VS Code 상단 File → New Window를 누른다. Ctrl+Shift+N도 같은 동작이다.')+crop('vscode:01-file-menu',(37,27,342,496),3.3)+para('새 창에서 File → Open Workspace from File...을 선택한다.','Open File...로 코드 하나만 여는 것과 구분한다.'))
    d.frame('이 회로의 workspace 선택',para('clone한 폴더에서 다음 경로로 이동한다.',p['path'],p['id']+'.code-workspace')+crop('vscode:02-workspace',(42,33,349,496),2.6)+para('PROJECT는 이 회로의 실행 설정과 결과, COMMON은 공유 RTL·TB·XDC다.','위 화면은 공통 폴더 구조 예이며 선택할 파일명은 이 슬라이드의 경로를 따른다.'))
    d.frame('확장 설치·활성화',para('Extensions에서 slang-server와 VaporView를 검색한다.')+crop('vscode:03-enable-slang',(351,70,1200,294),2.8)+para('없으면 Install, 꺼져 있으면 Enable 또는 Enable (Workspace).','Verilog 구문 강조가 보여도 시뮬레이션이 통과했다는 뜻은 아니다.'))
    srcs=[Path(x).name for x in p['sources']]
    d.frame('Explorer에서 파일 열기',items(['PROJECT와 COMMON 왼쪽 화살표를 눌러 펼친다.','RTL: '+', '.join(srcs)+'. 파일을 두 번 누르면 탭으로 열린다.','검증 TB: '+Path(p['testbench']).name+'.','핀 제약: '+Path(p['constraints']).name+'.','수정 후 File → Save All. 저장한 뒤에 시뮬레이션한다.'])+link(TEMPLATE+p['path'],'이 프로젝트 소스·workspace 열기'))
    d.frame('입출력과 동작 규칙',para(c['ports'],c['rule'],c['board']),label+'-sim')
    d.frame('실행 전에 예상값 작성',table(['입력 또는 조건','예상 결과'],c['examples'])+para(c['focus'],'예상값을 계산한 근거를 자신의 말로 설명한다.'))
    if c['n']==2 and not legacy:
        for module in ['half_adder','full_adder']:
            d.frame(module+' 연결 읽기',para('실제 배포 RTL을 VS Code에서 연 화면이다.')+'\\par\\vspace{0.25cm}\\includegraphics[width=\\textwidth,trim=265bp 410bp 0bp 28bp,clip]{assets/lab1-circuits/'+module+'-rtl.png}\n'+para('반가산기는 두 입력의 XOR를 합, AND를 carry로 출력한다.' if module=='half_adder' else '첫 반가산기의 합과 cin을 두 번째 반가산기에 연결한다. 두 carry를 OR로 합친다.'))
    elif not legacy and c['n'] in [3,4,5]:
        shot={3:'adder_4bit',4:'sub_4bit',5:'compare_4'}[c['n']]
        d.frame('RTL 구조를 설명한다',para('실제 배포 RTL을 VS Code에서 연 화면이다.','설계 top: '+p['top'])+'\\par\\vspace{0.25cm}\\includegraphics[width=\\textwidth]{assets/lab1-circuits/'+shot+'-rtl-crop.png}\\par\\vspace{0.25cm}\n'+para(c['rule'],'포트 선언·비트 폭·출력 연결을 짚어 설명한다. 저장소 소스를 복사해 사용해도 된다.')+link(TEMPLATE+p['path'],'배포 소스 확인'))
    else:
        d.frame('RTL 구조를 설명한다',para('설계 top: '+p['top'],'RTL 파일: '+', '.join(srcs),c['rule'],'소스를 저장소에서 직접 열고 포트 선언·비트 폭·출력 연결을 짚어 설명한다. 저장소 소스를 복사해 사용해도 된다.')+link(TEMPLATE+p['path'],'배포 소스 확인'))
    if legacy and c['n']==4:
        d.frame('원본 감산기의 borrow 보충',para('원본은 a>b일 때만 borrow=0으로 두어 a=b에서도 borrow=1이 된다.','original/sub_4bit.v는 원본 바이트를 보존한다. corrected/sub_4bit.v는 비교를 a>=b로 고친 보충 파일이다.','배포 workspace와 XPR은 수정본으로 검사한다. 원본 오류 검출 로그와 수정 후 256개 통과 결과를 구분한다.'))
    d.frame('테스트벤치와 통과 기준',para('시뮬레이션 top: '+p['simulation_top'],f"{c['cases']}개 입력 조합을 모두 검사한다. 각 자극은 10ns, 종료 시각은 {c['cases']*10}ns다.",'기대값과 실제 출력이 다르면 $fatal로 중단한다. 검사 횟수와 watchdog도 확인한다.','통과 문구: LAB1_PASS '+p['top']+' cases='+str(c['cases']),'원본 레거시 testbench.v와 별도의 자기검사 TB는 파일과 역할을 구분한다.'))
    d.frame('저장 → Terminal → Run Task',para('File → Save All 다음 Terminal → Run Task...을 누른다.')+crop('vscode:06-tasks',(293,0,909,125),2.1)+items(['01 Check tools를 실행하고 도구 버전을 확인한다.','02 Simulate를 선택하고 종료까지 기다린다.','03 Open waveform으로 생성된 VCD를 연다.'])+para('작업이 없으면 올바른 .code-workspace를 열었는지 확인한다.'))
    logfile=LAB/p['path']/'build/vscode/simulation.log'
    marker='LAB1_PASS '+p['top']+' cases='+str(c['cases'])
    measured=logfile.is_file() and marker in logfile.read_text(errors='replace')
    d.frame('실행 로그 확인',para('PROJECT → build → vscode → simulation.log를 연다.',marker if measured else '이 프로젝트의 실제 실행 결과는 검증표에서 확인한다.',f"정상 종료 시각: {c['cases']*10}ns. PASS 문구와 검사 수를 함께 확인한다.",'실패하면 compile.log → elaborate.log → simulation.log 순서로 원인을 찾는다.','코드 저장 → 02 Simulate 재실행 → 새 로그 확인 순서로 복귀한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/'+p['path']+'/README.md','프로젝트 검증 안내'))
    d.frame('VCD를 파형으로 열기',items(['03 Open waveform 또는 build/vscode/wave.vcd를 연다.','텍스트로 열리면 탭 우클릭 → Reopen Editor With... → VaporView.','Netlist View에서 '+p['simulation_top']+'을 펼친다.','신호 '+', '.join(c['signals'])+'를 각각 두 번 눌러 추가한다.','Zoom to Fit를 누르고 Time Units를 ns로 맞춘다.','전환 경계 대신 구간 중간에 커서를 두고 값을 읽는다.']))
    d.frame('파형 화면의 읽는 순서',crop('vscode:08-vapor-wave',(352,37,1202,469),3.4)+para('위는 공통 파형 조작 예다. 이번 회로에서는 앞 장의 신호 이름을 선택한다.',c['focus'],'신호 이름 → 시간 구간 → 커서 값 → 예상 결과 순서로 비교한다.'))
    wave=LAB/p['path']/'build/vscode/wave.vcd'
    if measured and wave.is_file():
        ns=sorted(set([0,1,min(3,c['cases']-1),c['cases']//2,c['cases']-1]))
        rows=vcd_values(wave,p['simulation_top'],c['signals'],[n*10+5 for n in ns])
        d.frame('실제 VCD의 구간 중간값',table(['시간(ns)']+c['signals'],rows)+para('이 표는 실행된 VCD에서 읽은 값이다. 다중 비트는 이진수다.','표의 시간으로 파형 커서를 옮겨 직접 대조하고, 추가 경계 조건도 확인한다.'))
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
    d.frame('File → Project → New...',crop('40-new-project-menu',(8,32,442,153),2.3)+para('New Project 안내에서 Next. Project name: '+p['top'],'Project location: 자신의 clone 폴더 / '+p['path']+' / vivado','Create project subdirectory를 해제하고 Next. RTL Project와 Do not specify sources at this time을 선택한다.'))
    d.frame('정확한 부품 선택',crop('43-select-part',(233,332,773,521),3.1)+para('Parts에서 xc7s75fgga484-1 검색 → 정확히 같은 행 선택 → Next.','요약에서 Spartan-7, fgga484, -1을 확인하고 Finish.'))
    d.frame('RTL을 Design Sources에 추가',crop('46-design-kind',(344,362,795,461),2.1)+para('왼쪽 Add Sources → Add or create design sources → Next → Add Files.','등록할 RTL: '+', '.join(Path(x).name for x in p['sources']),'Copy sources into project를 해제하고 Finish. VS Code와 같은 원본을 참조한다.'))
    d.frame('Simulation Sources에 TB 추가',crop('50-simulation-kind',(344,363,795,461),2.1)+para('Add Sources → Add or create simulation sources → Next → Add Files.',Path(p['testbench']).name+'를 선택한다. sim_1을 유지한다.','Copy sources into project는 해제, Include all design sources for simulation은 체크 → Finish.'))
    d.frame('XDC를 Constraints에 추가',crop('53-constraints-kind',(344,363,795,461),2.1)+para('Add Sources → Add or create constraints → Next → Add Files.',Path(p['constraints']).name+' 선택 → Copy constraints files into project 해제 → Finish.','소스 중복 등록이나 잘못된 종류로 추가한 파일이 없는지 확인한다.'))
    d.frame('두 top을 구분한다',para('Design Sources의 top: '+p['top'],'Simulation Sources → sim_1의 top: '+p['simulation_top'],'Sources의 화살표를 눌러 계층을 펼친다. 굵은 이름이 top이다.','잘못 지정되었다면 올바른 모듈 우클릭 → Set as Top. 이미 top이면 해당 메뉴가 비활성인 것이 정상이다.','테스트벤치를 합성할 설계 top으로 지정하지 않는다.'))
    d.frame('Run Behavioral Simulation',crop('58-run-behavioral',(12,422,467,636),3.0)+para('Run Simulation → Run Behavioral Simulation. 컴파일과 elaboration을 기다린다.','파형에서 신호를 선택하고 Zoom Fit, 시간 단위, 커서 값을 확인한다.','Tcl Console의 PASS 문구와 종료 시각을 확인한다. 오류면 Messages의 첫 오류로 돌아간다.'))
    sim=LAB/p['path']/'build/vivado-sim/simulation.log';marker='LAB1_PASS '+p['top']+' cases='+str(c['cases'])
    d.frame('VS Code 결과와 비교',para('두 실행은 같은 RTL과 자기검사 TB를 사용한다.',marker if sim.exists() and marker in sim.read_text(errors='replace') else 'Vivado 실행 상태와 근거 로그는 프로젝트 검증표에서 확인한다.','VS Code 로그: build/vscode/. GUI 로그: vivado/'+p['top']+'.sim/sim_1/behav/xsim/.',c['focus'],'로그·파형을 서로 다른 이름으로 보관하고 네 가지 정보인 입력·출력·시간·검사 수를 비교한다.'))
    pins(d,p)
    d.frame('Run Synthesis',crop('62-run-synthesis',(10,604,260,704),2.1)+para('File → Close Simulation → OK. Flow Navigator → Run Synthesis.','Launch Runs: 기본 디렉터리, Launch runs on local host, PC 자원에 맞는 jobs → OK.','Synthesis successfully completed를 확인한다. 실패했으면 다음 단계로 넘어가지 않는다.'))
    d.frame('Run Implementation',crop('64-synthesis-complete',(558,302,918,491),2.8)+para('합성 완료 창에서 Run Implementation → OK. Launch Runs에서 OK.','완료 창을 닫았다면 Flow Navigator → Run Implementation.','Implementation successfully completed가 나올 때까지 기다린다.'))
    d.frame('Generate Bitstream',crop('66-implementation-complete',(558,302,918,491),2.8)+para('구현 완료 창에서 Generate Bitstream → OK → Launch Runs의 OK.','또는 Program and Debug → Generate Bitstream.','최종 상태 write_bitstream Complete!를 확인한다. 파일 생성과 보드 기록은 다른 단계다.'))
    result=LAB/p['path']/'build/build/result.json';status=json.loads(result.read_text())['status'] if result.exists() else '미실행'
    d.frame('생성 파일과 보고서',para('생성 bit: vivado/'+p['top']+'.runs/impl_1/'+p['top']+'.bit','제작 실행 결과와 증빙은 프로젝트의 evidence/validation.json과 README 검증표를 확인한다.','DRC 오류를 확인하고 CFGBVS / CONFIG_VOLTAGE 경고는 실제 보드 구성 전압과 대조한다.','1kHz 클록의 내부 타이밍과 지연 제약이 없는 외부 입출력을 구분한다.' if p['top']=='lab1_integrated' else '클록 없는 조합회로의 setup/hold NA를 타이밍 검증 완료로 해석하지 않는다.','사용한 커밋·bit 해시·DRC·타이밍 보고서를 결과와 함께 남긴다.'))

def post(d,c,p):
    if p['edition']=='opensource_cli':
        d.frame('보드 실험으로 이어갈 때',para('현재 검증한 CLI 흐름은 S75 데이터베이스의 핀 누락으로 bit를 생성하지 못했다.','보드 실험은 같은 RTL의 Vivado 통합 프로젝트에서 생성한 bit로 진행한다.','CLI 실행 결과와 Vivado bit의 생성 경로·해시를 구분하여 레포트에 적는다.')+link('04.LAB1_10A_INTEGRATED_VIVADO.pdf','Vivado 통합 매뉴얼'))
    d.frame('실제 보드 연결',crop('70-auto-connect',(270,123,704,309),3.0)+para('Open Hardware Manager → Open target → Auto Connect.',c['board'],'장치가 없으면 보드 전원·USB JTAG·드라이버·VM USB 연결을 점검한다.'),d.label+'-post')
    d.frame('Program Device와 동작 확인',items(['연결된 장치 이름이 xc7s75인지 확인한다.','장치 우클릭 → Program Device.','이번 프로젝트의 '+p['top']+'.bit를 선택하고 Program.','기록 완료를 확인한 뒤 입력을 바꾸고 출력과 예상값을 비교한다.','기록 성공 화면과 실제 보드 동작은 각각 증빙한다.'])+para('제작 환경의 실제 보드 기록·촬영 검증 여부는 검증표를 따른다. 파일 생성만으로 보드 동작 성공을 선언하지 않는다.'))
    d.frame('사진과 시연 영상 촬영',para(c['board'],'사진에는 보드 연결과 입력·출력 위치가 함께 보이게 한다.','영상에는 입력을 조작하는 과정과 그에 따른 출력 변화를 담는다.','예상표의 정상·경계 조건을 직접 보여주고 회로 번호를 파일명에 적는다.','통합 영상이라면 각 회로의 타임스탬프를 레포트에서 연결한다.'))
    d.frame('GitHub 결과 정리',items(['reports/pre와 reports/post에 실험 전·후 레포트를 둔다.','evidence/vscode와 evidence/vivado에 로그·파형·캡처를 구분한다.','evidence/board/photos와 videos에 직접 촬영한 자료를 둔다.','큰 영상·bit는 배포 위치를 정하고 README와 레포트에서 연결한다.','웹에서 사진 표시와 영상 재생 또는 다운로드가 되는지 확인한다.'])+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/reports.md','레포트 양식·예시·GitHub 안내'))
    d.frame('실험 후 레포트',items(['Vivado 버전·part·top·핀 제약·코드 커밋을 기록한다.','VS Code와 Vivado의 입력·출력·시간·검사 수를 비교한다.','합성·구현·bit 경로와 경고·수정 사항을 설명한다.','장치 기록 화면·사진·영상과 해당 조건을 연결한다.','예상값·두 시뮬레이션·실측의 일치 또는 차이 원인을 해석한다.','미수행 항목은 미완료로 남기고 후속 확인을 적는다.'])+link('04.LAB1_00_CONTENTS.pdf','전체 목차 PDF')+r'\quad'+link(TEMPLATE+p['path'],'프로젝트로 돌아가기'))

def legacy_pages(d,c):
    d.frame('원문 Vivado 실습으로 이동',para('이후 원문은 원본의 사진·문구·순서를 유지한다.','배포 프로젝트는 Vivado 2020.1 원본 XPR 형식을 기반으로 상대경로를 정리했다. 구버전 실행 검증은 별도로 확인한다.','수업에서는 원문의 합성·구현에 앞서 자기검사 TB로 Behavioral Simulation을 먼저 실행한다.','원본 testbench.v와 검증용 TB의 입력 순서·실행 시간은 서로 다를 수 있다.'),d.label+('-original-intro' if c['n']==1 else '-vivado'))
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
    d.frame('템플릿과 새 창',para('Git·Python 3·VS Code와 '+('Icarus Verilog·Yosys·openXC7' if cli else 'Vivado 2026.1 XSim')+'을 준비한다.','git clone https://github.com/Glaysia/fpga-lab-template.git','VS Code: File → New Window → Open Workspace from File...')+crop('vscode:01-file-menu',(37,27,342,496),2.5)+para(p['path']+'/'+p['id']+'.code-workspace'),label+'-setup')
    d.frame('확장과 Explorer',para('Extensions에서 slang-server와 VaporView를 Install 또는 Enable (Workspace).')+crop('vscode:03-enable-slang',(351,70,1200,294),2.4)+para('Explorer에서 COMMON → rtl → lab1_integrated.v를 두 번 누른다.','COMMON → tb → tb_lab1_integrated.sv, constraints → lab1_integrated.xdc도 연다.','PROJECT에는 project.json·workspace·결과 폴더가 있다. File → Save All.'))
    d.frame('세 작업을 순서대로 실행',crop('vscode:06-tasks',(293,0,909,125),2.1)+items(['Terminal → Run Task... → 01 Check tools.','02 Simulate → 종료까지 기다린다.','PROJECT/build/vscode/simulation.log를 연다.','LAB1_PASS lab1_integrated cases=2560을 확인한다.','03 Open waveform으로 wave.vcd를 연다.'])+para('CLI workspace는 Icarus Verilog를 선택한다.' if cli else 'GUI를 열기 전에도 설치된 XSim 실행 파일은 사용한다.'))
    d.frame('통합 테스트의 검사 범위',para('10개 모드 × DIP 256개 = 2,560개 출력 비교.','reset → MODE 01, 짧은 바운스 무시, 길게 눌러도 한 번만 전환, 10→01 순환을 검사한다.','LCD 초기 명령과 외부 버스에서 완성된 두 줄의 번호·이름을 비교한다.','TB는 10ns 클록, 디바운스 4클록, 전원 대기 5클록으로 시간을 줄인다. 실제 합성은 1kHz 보드 설정이다.','XSim 검사 종료: 72430ns. 실제 보드의 전압·LCD 연결은 별도로 확인한다.'))
    d.frame('VaporView에서 통합 파형 읽기',items(['wave.vcd가 텍스트면 탭 우클릭 → Reopen Editor With... → VaporView.','Netlist에서 tb_lab1_integrated를 펼친다.','clk, rst, mode_button, sw, led, seg_data를 추가한다.','dut 안의 mode와 lcd_e, lcd_rs, lcd_rw, lcd_data를 추가한다.','Zoom to Fit 뒤 모드가 바뀌는 구간을 확대한다.','버튼 입력부터 모드 변경까지의 지연과 LCD 한 화면 갱신을 구분한다.']))
    d.frame('실험 전 레포트에 넣을 것',items(['모드별 예상 입력·출력과 비트 순서를 표로 작성한다.','10개 회로·버튼·LCD 파일의 역할을 설명한다.','PASS 로그, VCD, 모드 전환 및 LCD 파형 캡처를 연결한다.','TB에서 줄인 시간과 실제 1kHz 설정을 구분한다.','실험에서 확인할 버튼·LCD·DIP·LED 장면을 계획한다.'])+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/reports.md','레포트 양식과 예시'))
    d.frame('통합 구조와 입력 배치',para('lab1_integrated → 10개 조합회로 + button_onepulse + lcd_modes.','clk=B6(1kHz), KEY1=reset, KEY2=mode_button.','DIP1–8은 sw[7:0], LED1–8은 led[7:0]에 대응한다.','개별 실습의 KEY 입력은 통합본에서 DIP로 옮겨 모드 버튼과 충돌하지 않게 한다.','단일 7세그먼트는 모드 10에서만 동작한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/integrated.md','통합 동작 명세와 핀표'),label+'-modes')
    mode_rows=[('01','a=DIP1, b=DIP2','LED1=AND, 2=OR, 3=XOR'),('02','a,b,cin=DIP1,2,3','LED1=carry, 2=sum'),('03','a=DIP1–4, b=DIP5–8','LED1=carry, 2–5=sum'),('04','a=DIP1–4, b=DIP5–8','LED1=borrow, 2–5=diff'),('05','a=DIP1–4, b=DIP5–8','LED1=큼, 2=같음, 3=작음'),('06','i=DIP1–4, s=DIP7–8','LED1=i[3-s]'),('07','i=DIP1, s=DIP6–8','s=0→LED1, s=7→LED8'),('08','DIP1–8 중 하나만 1','LED1–3: DIP1→0, DIP8→7'),('09','abc=DIP6,7,8','0→LED8, 7→LED1'),('10','hex=DIP5–8','a–dp 패턴, 1이면 점등')]
    for n in range(0,10,5):d.frame('모드별 조작 '+str(n+1)+'–'+str(n+5),table(['모드','입력','출력'],mode_rows[n:n+5])+para('사용하지 않는 LED 비트는 0이다. reset하면 모드 01.'))
    d.frame('버튼을 길게 누르면',para('2단 동기화 → 안정된 입력 20클록 확인 → 상승 시 1클록 펄스.','1kHz에서 약 20ms 안정 시간에 동기화 지연이 추가된다.','누른 채 유지하면 한 번만 바뀐다. 뗀 뒤 다시 눌러야 다음 모드가 된다.','모드 10 다음은 01. reset은 즉시 01로 돌아간다.','실험 영상에서 짧게 누르기·길게 누르기·순환을 각각 보여준다.'))
    d.frame('LCD가 표시되는 과정',para('전원 대기 50ms → 38,38,38,0C,06 초기 명령 → 두 줄 반복 갱신.','첫 줄 MODE 01…MODE 10, 두 번째 줄 회로 이름.','E high는 1ms, 바이트 간격은 최소 4ms. 첫 초기 명령 간격은 더 길다.','한 화면 시작 때 모드를 저장하여 두 줄이 다른 모드로 섞이지 않게 한다.','새 모드는 현재 전송을 마친 뒤 갱신되므로 잠깐 기다리고 읽는다.'))

def cli_steps(d,p):
    d.frame('CLI 실행 환경',para('macOS ARM64 바이너리 배포를 확인하고 WSL Ubuntu-26.04에서 Linux x86-64 바이너리를 실행했다.','제작자에게 Mac이 없으므로 Mac 실행·보드 기록을 검증했다고 쓰지 않는다.','APIO 1.5.1, OSS CAD Suite 2026.08.19, openXC7 2026.08.20.','Yosys 0.63+173 / nextpnr-xilinx 68aeeb3 / Icarus Verilog 14.0 개발 버전.')+link('https://github.com/FPGAwars/tools-openxc7/releases/tag/2026-08-20','openXC7 공식 ARM64·Linux 배포'),d.label+'-vivado')
    d.frame('설치와 경로',para('Python 3의 venv를 만들고 pip install apio==1.5.1을 실행한다.','apio packages install로 oss-cad-suite와 openxc7을 준비한다.','도구 경로는 ~/.apio/packages/oss-cad-suite/bin 및 openxc7/bin이다.','LD_LIBRARY_PATH를 두 묶음의 lib로 전역 지정하지 않는다. 각 배포의 실행 래퍼가 자신의 라이브러리를 선택한다.','macOS는 darwin-arm64, WSL은 linux-x86-64 자산을 사용한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/cli.md','복사 가능한 전체 설치·실행 명령'))
    d.frame('대상 부품 데이터베이스',para('대상은 xc7s75fgga484-1이다. xc7s50으로 바꾸지 않는다.','배포에 포함된 S50 chipdb만으로는 S75를 빌드할 수 없다.','openXC7/prjxray-db의 spartan7 자료와 bbaexport.py·bbasm으로 정확한 부품의 chipdb를 준비한다.','데이터베이스 버전, 내보내기 결과와 실패 로그를 보관한다.')+link('https://github.com/openXC7/prjxray-db','공식 디바이스 데이터베이스'))
    d.frame('실제 실행 결과와 남은 제약',para('Icarus: 2,560개 통과. Yosys: 논리 게이트·통합 합성 성공.','nextpnr: 논리 게이트 K4, 통합 클록 B6 핀을 찾지 못해 실패. 프레임·bit 단계는 실행하지 못했다.','검증한 S75 DB의 필수 핀 38개 중 28개가 빠져 있다. S75 tilegrid는 S50 파일과 바이트 단위로 같았다.','Vivado 공식 부품 데이터에는 K4와 B6가 존재한다. 다른 핀·다른 FPGA로 바꾸어 성공 처리하지 않는다.','CLI bit 목표는 미완료이며, 실행 로그·DB 해시·후속 작업을 공개한다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/cli.md','실패 근거와 데이터베이스 대조'))
    d.frame('검증 가능한 순서로 실행',items(['02 Simulate: Icarus Verilog의 2,560개 검사와 VCD.','Yosys: synth_xilinx로 RTL을 Xilinx 셀에 매핑.','nextpnr-xilinx: 정확한 chipdb와 XDC로 배치·배선.','fasm2frames: FASM을 디바이스 프레임으로 변환.','xc7frames2bit: 정확한 part.yaml로 bit 생성.'])+para('각 단계의 입력·출력·종료 코드를 확인한다. 앞 단계 실패 후 오래된 산출물을 사용하지 않는다.'))
    d.frame('실행 명령과 결과 확인',para('프로젝트 폴더: opensource_cli/integrated.','python3 ../../tools/lab1.py simulate --project . --simulator iverilog','python3 ../../tools/openxc7_build.py --project .','생성 명령·실행 로그·상태·bit 해시는 프로젝트 build/cli와 검증 문서에서 확인한다.','합성 성공만으로 배치배선·bit 생성 완료를 선언하지 않는다.')+link(COURSE+'example/fpga_projects_hdl/LAB1/docs/cli.md','실제 단계별 결과'))
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
    inventory=[]
    for c in CIRCUITS:
        for ed in ['vivado_2026_1','legacy']:
            if c['n']==1 and ed=='vivado_2026_1':continue
            p=next(p for p in PROJECTS if p['path']==ed+'/'+c['slug'])
            modern=ed=='vivado_2026_1';number=c['n'] if modern else c['n']+10
            name=f"04.LAB1_{number:02d}_{c['pdf']}_{'VIVADO' if modern else 'LEGACY'}"
            d=Deck(('modern-' if modern else 'legacy-')+f"{c['n']:02d}",c['title'])
            prelude(d,c,p)
            if modern:vivado(d,c,p)
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
        else:vivado(d,c,p)
        post(d,c,p)
        inventory.append({'file':name,'pages':d.write(name),'project':p['path']})
    overview(inventory)
    (BASE/'series-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(inventory,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
