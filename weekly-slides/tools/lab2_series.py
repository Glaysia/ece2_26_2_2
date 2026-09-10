"""Generate 18 LAB2 manuscripts and an exact inventory of required real code captures.

No code screenshots are fabricated. Missing captures remain visible draft notices.
"""
from pathlib import Path
import hashlib
import json
import math
import re

from lab2_intro import esc, paras, steps, table, terminal
from verify_lab2_cores import EDITS
from lab2_legacy_assets import SOURCES as LEGACY_SOURCES

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'
BASE=ROOT/'weekly-slides/weekly-slides/LAB2_FPGA_0921'
GUI='../LAB1_FPGA_0914/assets/modern-01/'
CAPTURES={}

def crop(name,box,height=2.2,vscode=False):
    x1,y1,x2,y2=box; w,h=(1202,802) if vscode else (1486,944)
    trim=' '.join(f'{v*.75:g}bp' for v in [x1,h-y2,w-x2,y1])
    return '\\par{\\centering\\includegraphics[width=\\textwidth,height='+str(height)+'cm,keepaspectratio,trim='+trim+',clip]{'+GUI+name+'.png}\\par}\\vspace{0.18cm}'

class Deck:
    def __init__(self,identity): self.identity=identity; self.pages=[]; self.missing=0
    def frame(self,title,body,label=None):
        self.pages.append('\\begin{frame}'+('[label='+label+']' if label else '')+'{'+esc(title)+'}\n\\small\n'+body+'\n\\end{frame}\n')
    def write(self,name,title):
        header=r'''% !TEX program = xelatex
\input{shared/lab2_preamble.tex}
\renewcommand{\legacySource}[1]{}
\newcommand{\terminalbox}[1]{\par\vspace{0.15cm}{\setlength{\fboxsep}{7pt}\colorbox{black}{\parbox{\dimexpr\textwidth-14pt\relax}{\color{white}\ttfamily\fontsize{7}{9}\selectfont #1}}}\par\vspace{0.15cm}}
\begin{document}
\renewcommand{\small}{\fontsize{9}{11}\selectfont}
'''
        header=header.replace('\\begin{document}','\\hypersetup{pdftitle={'+esc(title)+'}}\n\\begin{document}')
        content=header+'\n'.join(self.pages)+'\\end{document}\n'
        target=BASE/name
        if not target.exists() or target.read_text(encoding='utf-8')!=content:
            target.write_text(content,encoding='utf-8')
        return {'file':name.removesuffix('.tex'),'title':title,'pages':len(self.pages),'missing_code_captures':self.missing,
                'status':'DRAFT_MISSING_REAL_CAPTURES' if self.missing else 'RENDER_REVIEW_REQUIRED'}

def code(d,project,relative):
    source=project/relative; content=source.read_bytes(); digest=hashlib.sha256(content).hexdigest()
    lines=content.decode('utf-8-sig').splitlines()
    for start in range(1,len(lines)+1,16):
        end=min(start+15,len(lines)); key=digest[:16]+f'-{start:03}-{end:03}'
        image='assets/code/'+key+'.png'
        record=CAPTURES.setdefault(key,{'image':image,'sha256':digest,'lines':[start,end],'sources':[],
                                       'max_columns':max(map(len,lines[start-1:end])),
                                       'requirement':'Actual VS Code editor capture matching these source bytes; no rendered/fabricated editor',
                                       'status':'MISSING'})
        location=source.relative_to(ROOT).as_posix()
        if location not in record['sources']: record['sources'].append(location)
        # Presence alone is not provenance: a capture must also have a reviewed record.
        verified=BASE/'assets/code'/f'{key}.json'
        ready=False
        if (BASE/image).exists() and verified.exists():
            proof=json.loads(verified.read_text(encoding='utf-8'))
            ready=(proof.get('source_sha256')==digest and proof.get('lines')==[start,end]
                   and proof.get('actual_vscode_capture') is True
                   and proof.get('image_sha256')==hashlib.sha256((BASE/image).read_bytes()).hexdigest())
        if ready:
            panel='\\includegraphics[width=\\textwidth,height=4.45cm,keepaspectratio]{'+image+'}\\par'
            record['status']='CAPTURE_PRESENT_REVIEW_REQUIRED'
        else:
            d.missing+=1
            panel='\\vspace{0.4cm}\\fbox{\\parbox{0.91\\textwidth}{'+paras('제작 중: 이 구간의 실제 VS Code 코드 화면을 아직 넣지 않았다.','파일의 '+str(start)+'–'+str(end)+'행 전체와 행 번호가 보여야 한다.','GUI 조작 중단 지시를 유지하고 있어 임의로 만든 화면으로 대체하지 않았다.')+'}}\\par\\vspace{0.4cm}'
        d.frame(Path(relative).name+' · '+str(start)+'–'+str(end)+'행',paras(relative+'를 열고 해당 구간을 직접 입력한다.')+panel)

def setup(d,p,project,config):
    cli=p['edition']=='opensource_cli'; continuation='\\' if cli else '`'
    d.frame('v2.0.0 템플릿을 새 이름으로 clone',paras(('Bash/Zsh/WSL' if cli else 'Windows PowerShell')+'에서 한 줄씩 실행한다.')+terminal('git clone --branch v2.0.0 '+continuation,'  https://github.com/Glaysia/fpga-lab-template.git '+continuation,'  '+p['student_folder'],'cd '+p['student_folder'],'git switch -c main','code LAB1.code-workspace'),'setup')
    d.frame('File → New Window',crop('01-file-menu',(37,28,332,106),1.4,True)+paras('Ctrl+Shift+N 또는 File → New Window. 새 창을 연다.')+crop('01-file-menu',(37,140,332,216),1.4,True)+paras('File → Open Workspace from File...을 누른다.'))
    d.frame('workspace와 추천 확장',steps(p['student_folder']+' 폴더에서 LAB1.code-workspace 선택 → Open.','Explorer에 PROJECT 하나와 src·sim·constraints·tools가 보이는지 확인.','Extensions → @recommended를 검색.','slang·VaporView·vscode-pdf의 Install을 누른다.','Python과 Icarus 실행 파일은 별도로 설치되어 있어야 한다.'))
    d.frame('시뮬레이션 도구 확인',steps('Terminal → Run Task... → 01 Check tools.','Git·Python·iverilog·vvp의 버전이 출력되는지 확인한다.','도구를 찾지 못하면 설치 경로를 PATH에 추가하고 VS Code를 다시 연다.')+terminal('git --version',('python3' if cli else 'python')+' --version','iverilog -V','vvp -V'))
    d.frame('빈 파일에서 시작',steps('src/design.v를 우클릭 → Rename. 첫 RTL 파일명으로 바꾼다.','추가 RTL은 src를 우클릭 → New File로 만든다.','sim/tb_design.v를 이번 TB 파일명으로 바꾼다.','constraints/pins.xdc를 이번 XDC 파일명으로 바꾼다.','뒤의 코드 화면을 보며 작성하고 File → Save All.'))
    files=[*config['sources'],config['testbench'],p['constraints']]
    for start in range(0,len(files),5):
        d.frame('이번 프로젝트에 작성할 파일',table(['역할','경로'],[(Path(f).parts[0],f) for f in files[start:start+5]]))
    d.frame('simulation.json의 세 항목',paras('sources: 앞 표의 src/ 파일 경로를 배열로 넣는다.','testbench: '+config['testbench'],'simulation_top: '+config['simulation_top'],'큰따옴표·대괄호·쉼표를 확인한다. module 이름에는 파일 확장자를 붙이지 않는다.'))
    code(d,project,'simulation.json')

def simulation(d,p,project,config):
    d.frame('VS Code에서 먼저 시뮬레이션',steps('File → Save All.','Terminal → Run Task... → 02 Simulate.','첫 오류가 있으면 파일 경로·행 번호와 이전 행의 세미콜론부터 확인.','LAB2_PASS 또는 LAB2_INTEGRATED_PASS와 검사 수·종료 시각 확인.','Terminal → Run Task... → 03 Open waveform.'),'simulation')
    d.frame('파형에서 확인할 신호',steps('clk·rst·제어 입력·저장값·출력을 파형에 추가한다.','상승 에지 직전 입력과 에지 뒤 상태를 비교한다.','리셋 우선·enable=0 유지·마지막 검사 시각을 확인한다.','출력만 본 화면과 전체 파형을 각각 저장한다.','새 실행 로그와 파형인지 확인한다. 이전 PASS를 재사용하지 않는다.'))
    proof=project/'evidence/standalone-simulation.json'
    if proof.exists():
        measured=json.loads(proof.read_text(encoding='utf-8'))
        assert all(hashlib.sha256((project/name).read_bytes()).hexdigest()==value for name,value in measured['input_sha256'].items()), 'Stale simulation evidence: '+str(project)
        marker=re.search(r'LAB2_(?:INTEGRATED_)?PASS[^\r\n]*',measured['simulation_log'])
        finish=re.search(r'\$finish called at (\d+) \(1ps\)',measured['simulation_log'])
        if marker and finish:
            d.frame('정상 실행의 기준',terminal(marker[0])+paras('Icarus 종료 시각: '+f'{int(finish[1])/1000:g}'+'ns. 로그가 ps로 표시되면 1,000으로 나눠 ns와 비교한다.','이 수치는 교안의 입력 순서·TB·파라미터에 대한 기준이다.','검사 수만 보지 말고 예상 상태와 실제 파형이 일치하는 이유를 설명한다.'))
    if p['top'] in EDITS:
        instruction=EDITS[p['top']][2]
    else: instruction='counter4.v의 증가량을 1에서 2로 바꾼다.'
    d.frame('수정 실험 · 실패와 복구',steps('정상 로그와 파형을 먼저 보관한다.',instruction+' TB 기대값은 유지한다.','Save All → 02 Simulate. LAB2_FAIL의 검사 이름·시각을 읽는다.','어떤 입력과 이전 상태에서 불일치가 발생했는지 계산한다.','RTL을 복구·저장·재실행하고 전체 PASS를 확인한다.'))
    d.frame('실험 전 레포트',steps('동작 표·상태 전이·타이밍을 예상한다.','RTL·TB·XDC·설정의 역할을 설명한다.','정상/변경/복구 3행 비교표와 실행 로그를 넣는다.','VS Code 파형을 확대해 입력·이전 상태·다음 상태를 설명한다.','장비 클록·핀·예상 LED 동작을 정리한 뒤 Vivado/CLI로 진행한다.'),'reports')

def gui(d,p,config):
    d.frame('Vivado GUI에서 이어서 진행',paras('사전 시뮬레이션과 실험 전 레포트를 마친 뒤 Vivado를 연다.','다음 클릭 화면은 기존 LAB1의 실제 캡처를 재사용한다. 화면 속 과거 폴더·파일명 대신 이 교안에 적힌 값을 사용한다.','설계 top: '+p['board_top'],'TB top: '+config['simulation_top']),'implementation')
    d.frame('새 프로젝트 시작',crop('40-new-project-menu',(8,32,442,153),2.2)+steps('File → Project → New... → Next.','Project name: '+p['board_top'],'Project location: 자신의 '+p['student_folder']+'/vivado.','Create project subdirectory를 해제하고 Next.'))
    d.frame('RTL Project',crop('42-rtl-project',(230,328,799,429),2.2)+paras('RTL Project와 Do not specify sources at this time을 선택한다.','Next를 눌러 부품 선택으로 간다.'))
    d.frame('정확한 S75 부품 선택',crop('43-select-part',(233,332,773,521),2.8)+paras('Parts 검색란에 xc7s75fgga484-1을 입력한다.','같은 part 행 선택 → Next. Spartan-7·fgga484·-1 확인 → Finish.'))
    for title,name,words in [
        ('Design Sources 추가','46-design-kind',['Add Sources → Add or create design sources → Next.','Add Files에서 앞 목록의 src/ RTL 파일을 모두 선택한다.','Copy sources into project 해제 → Finish. 같은 원본 파일을 참조한다.']),
        ('Simulation Sources 추가','50-simulation-kind',['Add Sources → Add or create simulation sources → Next.','Add Files → '+config['testbench']+' 선택.','sim_1 유지. Include all design sources for simulation 선택.','Copy sources into project 해제 → Finish.']),
        ('Constraints 추가','53-constraints-kind',['Add Sources → Add or create constraints → Next.','Add Files → '+p['constraints']+' 선택.','Copy constraints files into project 해제 → Finish.'])]:
        d.frame(title,crop(name,(344,362,795,461),2.0)+steps(*words))
    d.frame('설계 top과 TB top 지정',steps('Sources에서 Design Sources의 계층을 펼친다.',p['board_top']+' 우클릭 → Set as Top.','Simulation Sources → sim_1의 계층을 펼친다.',config['simulation_top']+' 우클릭 → Set as Top.','이름이 이미 굵게 표시되면 해당 top이 선택된 상태다.'))
    d.frame('Run Behavioral Simulation',crop('58-run-behavioral',(12,422,467,636),2.7)+paras('Flow Navigator → Run Simulation → Run Behavioral Simulation.','컴파일과 elaboration을 기다린다. Tcl Console의 자기검사 PASS와 종료 시각을 확인한다.'))
    d.frame('VS Code 결과와 비교',steps('같은 RTL·TB로 실행했는지 Sources를 확인한다.','clk·rst·입력·상태·출력의 파형을 추가하고 Zoom Fit.','상승 에지 전후를 확대해 VS Code 결과와 대조한다.','검사 이름·검사 수·종료 시각·파형의 차이를 기록한다.','File → Close Simulation → OK로 돌아간다.'))
    d.frame('핀과 클록 확인',paras('RTL Analysis → Open Elaborated Design → I/O Ports.','이번 XDC의 PACKAGE_PIN과 LVCMOS33을 포트마다 대조한다.','B6 주 클록은 1 kHz, XDC 주기는 1,000,000ns다.','실제 장비의 클록 선택도 1 kHz로 맞춘다. 버튼을 클록으로 연결하지 않는다.'))
    for title,image_name,box,words in [
        ('Run Synthesis','62-run-synthesis',(10,604,260,704),['Flow Navigator → Run Synthesis.','Launch runs on local host, PC 자원에 맞는 jobs → OK.','합성 오류가 없으면 완료 창에서 Run Implementation → OK.']),
        ('Run Implementation','64-synthesis-complete',(558,302,918,491),['구현 Launch Runs의 위치·jobs 확인 → OK.','완료 창에서 Generate Bitstream → OK.','실패하면 Messages의 첫 오류부터 수정한다.'])]:
        d.frame(title,crop(image_name,box,2.3)+steps(*words))
    d.frame('Generate Bitstream',steps('Generate Bitstream의 Launch Runs에서 OK.','완료 창에서 Open Implemented Design으로 결과를 확인한다.','vivado/'+p['board_top']+'.runs/impl_1/'+p['board_top']+'.bit 확인.','타이밍·DRC 경고를 읽고 원인과 장비 설정을 기록한다.','bit 생성과 실제 보드 기록은 별도 단계다.'))

def cli(d,p):
    d.frame('Vivado 없이 S75 구현',paras('macOS에서는 해당 ARM64 배포, Windows에서는 WSL Linux 배포를 사용한다.','제작 검증은 WSL Linux x86-64에서 수행했다. Mac에서 실행했다는 뜻이 아니다.','실행한 도구는 APIO 1.5.1, OSS CAD Suite 2026.08.19, openXC7 2026.08.20이다.'), 'implementation')
    d.frame('APIO 도구 설치',terminal('python3 -m venv ~/.local/share/fpga-apio','~/.local/share/fpga-apio/bin/pip install apio==1.5.1','~/.local/share/fpga-apio/bin/apio packages install','export PATH="$HOME/.apio/packages/oss-cad-suite/bin:$PATH"','export PATH="$HOME/.apio/packages/openxc7/bin:$PATH"','yosys -V','nextpnr-xilinx --version')+paras('패키지 기본 버전은 바뀔 수 있다. 재현할 때는 앞 표의 고정 릴리스를 사용하고 버전을 기록한다.'))
    d.frame('S75 준비 도구 받기',terminal('mkdir -p ~/fpga-cli/lab2-tools','cd ~/fpga-cli/lab2-tools','base=https://raw.githubusercontent.com/Glaysia','base="$base/fpga-lab-example-opensource-cli-integrated"','base="$base/v2.0.1/tools"','curl --fail --location "$base/prepare_s75.py" \\','  -o prepare_s75.py','curl --fail --location \\','  "$base/xc7s75fgga484-1-package-pins.csv" \\','  -o xc7s75fgga484-1-package-pins.csv'))
    d.frame('정확한 S75 DB와 chipdb 준비',terminal('python3 prepare_s75.py')+paras('준비 도구는 ~/fpga-cli/lab1-s75에 공통 장비 데이터를 만든다. LAB1과 같은 S75 DB이므로 디렉터리 이름을 유지한다.','prepared.json의 xc7s75fgga484-1·338핀·DB 고정 커밋·chipdb 해시를 확인한다.','실패하면 export.log·bbasm.log를 읽는다. 완료 후 자신의 '+p['student_folder']+' 프로젝트 루트로 돌아간다.'))
    d.frame('synth.ys 직접 작성',terminal('read_verilog src/*.v','synth_xilinx -family xc7 -top lab2_integrated','write_json build/cli/design.json','stat')+paras('TB를 합성 파일에 포함하지 않는다. 프로젝트 루트에 synth.ys로 저장한다.'))
    d.frame('합성과 배치배선',terminal('mkdir -p build/cli','yosys -l build/cli/synthesis.log -s synth.ys','chip="$HOME/fpga-cli/lab1-s75/xc7s75fgga484-1.bin"','db="$HOME/fpga-cli/lab1-s75/prjxray-db/spartan7"','part=xc7s75fgga484-1','nextpnr-xilinx --chipdb "$chip" \\','  --xdc constraints/lab2_integrated.xdc \\','  --json build/cli/design.json --fasm build/cli/design.fasm \\','  --freq 0.001 --log build/cli/place-route.log'))
    d.frame('프레임과 bit 생성',terminal('fasm2frames --db-root "$db" --part "$part" \\','  build/cli/design.fasm build/cli/design.frames','xc7frames2bit --part_file "$db/$part/part.yaml" \\','  --part_name "$part" --frm_file build/cli/design.frames \\','  --output_file build/cli/lab2_integrated.bit')+paras('각 단계 종료 코드와 로그를 확인한다. 이전 bit 파일을 새 실행 결과로 쓰지 않는다.'))
    d.frame('openFPGALoader 설치',paras('macOS에서는 Homebrew로 설치한다. Linux에서는 배포 패키지 또는 공식 설치 안내를 따른다.')+terminal('brew install openfpgaloader')+paras('WSL은 USB JTAG 장치가 Linux 쪽에 전달되어 있어야 한다. 보드 전원·케이블·운영체제의 장치 인식을 먼저 확인한다.')+r'\href{https://trabucayre.github.io/openFPGALoader/guide/install.html}{공식 운영체제별 설치 안내}')
    d.frame('bit 읽기와 실제 기록',terminal('bitread --part_file "$db/$part/part.yaml" -C -z -y \\','  -o build/cli/bits.txt build/cli/lab2_integrated.bit','openFPGALoader --list-cables','openFPGALoader --detect','openFPGALoader -c MY_CABLE build/cli/lab2_integrated.bit')+paras('MY_CABLE은 실제 연결 케이블 식별자로 바꾼다. SRAM 기록이며 Flash 옵션 -f는 넣지 않는다.'))
    d.frame('CLI 검증 범위',paras('현재 S75 bit 생성·IDCODE·9,104프레임 읽기 결과는 예시의 evidence/openxc7에 있다.','nextpnr는 set_false_path를 무시한다. 이 예외는 Vivado 쪽 비동기 입력 타이밍 분석에만 적용된다.','파일 검사 성공은 실제 버튼·LCD·장치 프로그래밍 성공과 구분한다.'))

def legacy(d,p):
    slug=Path(p['path']).name
    _,first,last=LEGACY_SOURCES[slug]
    d.frame('원본 교안과 대조',paras('이후에는 원본의 사진·문구·순서를 그대로 보존했다.','원본의 파일명·버튼 클록·핀·TB 시간과 현재 실습을 대조한다. 현재 프로젝트에는 앞서 작성한 RTL·TB·XDC를 사용한다.','원본의 전용 클록 배선 검사 해제나 비동기 데이터 로드를 현재 코드에 그대로 옮기지 않는다.'))
    for number in range(first,last+1):
        image=f'assets/legacy-{slug}/page-{number:03}.png'
        d.pages.append('\\begin{frame}[plain]\n\\begin{tikzpicture}[remember picture,overlay]\n'
            '\\node[inner sep=0pt] at (current page.center) {\\includegraphics[width=\\paperwidth,height=\\paperheight,keepaspectratio]{'+image+'}};\n'
            '\\node[anchor=west] at ([xshift=0.65cm,yshift=0.52cm]current page.south west) {\\labonehome};\n'
            '\\node[anchor=east,text=gray,font=\\scriptsize] at ([xshift=-0.57cm,yshift=0.52cm]current page.south east) {\\insertframenumber};\n'
            '\\end{tikzpicture}\n\\end{frame}\n')

def main():
    inventory=[]
    projects=json.loads((LAB/'projects.json').read_text(encoding='utf-8'))
    for p in projects:
        project=LAB/p['path']; config=json.loads((project/'simulation.json').read_text(encoding='utf-8'))
        d=Deck(p['id'])
        d.frame('LAB 2 · '+p['title'],paras('VS Code에서 직접 작성·검증한 다음 장비로 확인한다.','작성일 2026. 09. 10. · 이해리','레거시 원본 비교' if p['edition']=='legacy' else ('오픈소스 CLI 통합' if p['edition']=='opensource_cli' else 'Vivado 실습')))
        related=[other for other in projects if other['top']==p['top'] and other['id']!=p['id']]
        cross='\\par\\vspace{0.3cm}'+''.join('\\href{'+other['pdf']+'}{'+esc('대응 '+('레거시판' if other['edition']=='legacy' else ('CLI판' if other['edition']=='opensource_cli' else 'Vivado판')))+'}\\quad' for other in related)
        d.frame('목차',r'\navlink{setup}{프로젝트 시작}\par\vspace{0.3cm}\navlink{code}{RTL·TB·XDC 직접 작성}\par\vspace{0.3cm}\navlink{simulation}{VS Code 시뮬레이션과 수정}\par\vspace{0.3cm}\navlink{implementation}{구현과 장치 기록}\par\vspace{0.3cm}\navlink{reports}{레포트}\quad\href{05.LAB2_00_START.pdf}{공통 예습}\quad\href{05.LAB2_00_CONTENTS.pdf}{전체 목차}'+cross, 'lab2-contents')
        setup(d,p,project,config)
        if p.get('legacy_differences'):
            d.frame('원본과 현재 실습의 차이',paras(p['legacy_differences'],'original/은 비교 자료로 보존한다. 현재 src/·sim/·XDC로 직접 작성·검증한다.'))
        d.frame('이번 회로의 관찰 방법',paras(p.get('controls','K4 초기화, N8 모드 변경, N4 회로 한 단계 실행. 새 모드로 넘어갈 때 회로 상태를 초기화한다.'),'입력 스위치를 먼저 정한 다음 버튼을 누른다.'),'code')
        for name in config['sources']:
            code(d,project,name)
        code(d,project,config['testbench'])
        d.frame('XDC를 직접 작성한다',steps('constraints 폴더의 XDC를 열고 전체 내용을 입력한다.','get_ports의 이름과 비트 번호를 board top 선언과 대조한다.','같은 핀을 서로 다른 포트에 중복 지정하지 않는다.','File → Save All. Icarus 기능 시뮬레이션은 XDC를 사용하지 않는다.'))
        code(d,project,p['constraints'])
        simulation(d,p,project,config)
        if p['edition']=='opensource_cli': cli(d,p)
        else: gui(d,p,config)
        if p['edition']=='legacy': legacy(d,p)
        if p['edition']=='opensource_cli':
            d.frame('장치에서 동작 확인',steps('보드 전원·JTAG·주 클록 1 kHz 설정을 확인한다.','앞 장의 openFPGALoader --detect로 연결된 FPGA를 확인한다.','실제 케이블 이름으로 MY_CABLE을 바꾸고 방금 생성한 bit를 SRAM에 기록한다.','종료 코드와 기록 로그를 확인한 뒤 리셋 버튼을 누른다.','모드 버튼으로 8개 모드를 순회하며 LCD 이름과 회로 출력을 예상과 비교한다.'))
        else:
            d.frame('장치에서 동작 확인',steps('보드 전원·JTAG·주 클록 1 kHz 설정을 확인한다.','Vivado: Open Hardware Manager → Open target → Auto Connect.','Program Device에서 방금 생성한 bit 파일을 선택한다.','초기화 뒤 입력·버튼·출력을 관찰하고 예상과 비교한다.','CLI판은 앞 장의 openFPGALoader 명령으로 기록한다.'))
        d.frame('실험 후 레포트와 GitHub',steps('도구 버전·source commit·XDC·bit 해시·타이밍과 경고를 적는다.','실제 기록 화면과 보드 전체 사진을 포함한다.','버튼 누름과 출력 변화가 함께 보이는 영상을 찍는다.','통합판은 8개 모드 번호·LCD 이름·회로 출력을 보여 준다.','소스·실험 전후 레포트·사진·영상 링크를 GitHub에서 연결한다.'))
        inventory.append(d.write(p['pdf'].replace('.pdf','.tex'),p['title']))
    (BASE/'series-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (BASE/'required-code-captures.json').write_text(json.dumps(list(CAPTURES.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    overview=Deck('contents')
    overview.frame('LAB 2 · 전체 목차',paras('순차논리 8개 · 레거시 비교 8개 · 통합 2개','작성일 2026. 09. 10. · 이해리','현재는 개별 원고를 제작 중이다. 코드 화면을 채우고 PDF 전체 검수 후 배포 ZIP을 만든다.'))
    overview.frame('자료 사용법',paras('ZIP 전체를 같은 폴더에 풀고 PDF를 연다.','각 PDF 좌하단 목차는 해당 PDF의 2쪽으로 돌아간다.','먼저 공통 예습을 읽고 자신의 실험 PDF를 연다.')+r'\href{05.LAB2_00_START.pdf}{공통 예습 26쪽}', 'lab2-contents')
    for edition,label in [('vivado_2026_1','Vivado'),('legacy','레거시 비교'),('opensource_cli','CLI')]:
        selected=[p for p in projects if p['edition']==edition]
        for first in range(0,len(selected),5):
            overview.frame(label+' · 매뉴얼', '\n'.join('\\href{'+p['pdf']+'}{'+esc(p['title'])+'}\\par\\vspace{0.3cm}' for p in selected[first:first+5]))
    overview.write('05.LAB2_00_CONTENTS.tex','전체 목차')
    print('18 manuscripts;',len(CAPTURES),'unique real code captures required;',sum(x['pages'] for x in inventory),'draft pages')

if __name__=='__main__': main()
