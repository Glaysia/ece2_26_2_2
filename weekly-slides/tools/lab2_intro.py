"""Author LAB2's common pre-lab primer in the existing 4:3 TeX style."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'weekly-slides/weekly-slides/LAB2_FPGA_0921'
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def esc(s):
    return ''.join({'\\':r'\textbackslash{}','_':r'\_','&':r'\&','%':r'\%','$':r'\$','#':r'\#','{':r'\{','}':r'\}','~':r'\textasciitilde{}'}.get(c,c) for c in s)

def paras(*lines): return r'\par\vspace{0.26cm}'.join(esc(line) for line in lines)+r'\par'

def steps(*lines): return '\\begin{enumerate}\n'+''.join('\\item '+esc(s)+'\n' for s in lines)+'\\end{enumerate}'

def terminal(*lines): return '\\terminalbox{'+r'\\'.join(esc(s) for s in lines)+'}'

def table(headers, rows):
    return '\\begin{center}\\renewcommand{\\arraystretch}{1.55}\\begin{tabular}{'+('l'*len(headers))+'}\n'+' & '.join(map(esc,headers))+r'\\\hline'+'\n'+''.join(' & '.join(map(esc,row))+r'\\'+'\n' for row in rows)+'\\end{tabular}\\end{center}'

def main():
    BASE.mkdir(parents=True,exist_ok=True)
    (BASE/'shared').mkdir(exist_ok=True)
    preamble=(BASE.parent/'LAB1_FPGA_0914/shared/lab1_preamble.tex').read_text(encoding='utf-8')
    preamble=preamble.replace('LAB1','LAB2').replace('LAB 1. 조합회로 실습','LAB 2. 순차논리 실습').replace('lab1-contents','lab2-contents')
    preamble=preamble.replace('LAB2 조합회로 실습 — 레거시 01','LAB2 순차논리 실습')
    preamble=preamble[preamble.index('\\documentclass'):]
    preamble='% !TEX program = xelatex\n% LAB2 common 4:3 course style; build into an isolated output directory.\n'+preamble
    (BASE/'shared/lab2_preamble.tex').write_text(preamble,encoding='utf-8')
    pages=[]
    def frame(title, body, label=None):
        pages.append('\\begin{frame}'+('[label='+label+']' if label else '')+'{'+esc(title)+'}\n\\small\n'+body+'\n\\end{frame}\n')

    frame('LAB 2 · 순차논리 예습',paras('전자전기컴퓨터설계실험Ⅱ','클록·저장·상태 전이를 파형으로 설명한다.','9월 21일 실습을 위한 공통 안내','작성일 2026. 09. 10. · 이해리'))
    frame('목차',paras('01 · 이번 주 실험과 프로젝트 시작','02 · 클록·리셋·이전 값·버튼 입력','03 · 8개 회로에서 반드시 확인할 것','04 · 시뮬레이션·수정 실험·실험 전후 레포트')+r'\vspace{0.2cm}\navlink{start}{시작}\quad\navlink{clock}{공통 개념}\quad\navlink{circuits}{회로별 검사}\quad\navlink{reports}{레포트}', 'lab2-contents')
    manifest=json.loads((LAB/'circuits.json').read_text(encoding='utf-8'))
    for offset in (0,4):
        frame('이번 주 필수 실험 · '+('1–4' if offset==0 else '5–8'),table(['교육 번호','실험'],[(str(x['education_number']),x['title']) for x in manifest[offset:offset+4]])+paras('8개 모두 예습한다. 실습에서는 지정된 회로를 설명하고 시연한다.'), 'circuits' if offset==0 else None)
    frame('한 회로를 끝내는 순서',steps('태그 고정 템플릿 clone → 새 VS Code 창에서 workspace 열기.','RTL·TB·설정을 직접 입력 → 저장 → VS Code 시뮬레이션.','정상·변경·복구 로그와 파형을 실험 전 레포트에 정리.','Vivado GUI에서 RTL·TB·XDC 등록 → 시뮬레이션 → bit 생성.','실제 보드 관찰·사진·영상·GitHub 링크를 실험 후 레포트에 정리.'),'start')
    frame('같은 템플릿, 다른 폴더 이름',paras('Windows PowerShell에서 한 줄씩 실행한다. 줄 끝의 `는 이어 쓰기다.')+terminal('git clone --branch v2.0.0 `','  https://github.com/Glaysia/fpga-lab-template.git `','  lab2_01_counter','cd lab2_01_counter','git switch -c main','code LAB1.code-workspace')+paras('다음 실험은 마지막 폴더 이름만 바꾼다. LAB1.code-workspace는 공통 템플릿 파일명이므로 그대로 연다.'))
    frame('VS Code 새 창에서 시작',steps('File → New Window를 누른다. 단축키는 Ctrl+Shift+N.','File → Open Workspace from File...을 누른다.','clone한 폴더에서 LAB1.code-workspace를 선택하고 Open.','Explorer의 PROJECT 아래 src·sim·constraints·tools를 확인한다.','Extensions에서 @recommended를 검색해 추천 확장을 설치한다.'))
    frame('직접 작성할 파일',table(['위치','역할'],[('src/','FPGA에 구현할 모듈'),('sim/','입력 자극·기대값·종료 조건을 가진 TB'),('constraints/','장비 핀과 전기 규격을 지정할 XDC'),('simulation.json','RTL 경로·TB 경로·TB 모듈명')])+paras('빈 파일에 교안의 전체 코드를 입력한다. 파일명과 module 이름은 서로 다른 항목이다.'))
    frame('시간을 읽는 기준',paras('이번 TB의 클록 주기는 10ns다. 상승 에지는 5, 15, 25, … ns에 온다.','입력을 바꿔도 레지스터는 다음 상승 에지에서 갱신된다.','TB는 상승 에지 뒤 1ns 기다린 다음 결과를 비교한다. nonblocking 갱신 전의 값을 잘못 검사하지 않기 위해서다.','시뮬레이션의 10ns와 실제 장비의 클록 설정은 별개다.'),'clock')
    frame('동기 리셋과 enable',table(['조건','다음 상승 에지의 동작'],[('rst = 1','초기값으로 변경'),('rst = 0, enable = 1','회로가 정한 상태 갱신'),('rst = 0, enable = 0','이전 상태 유지')])+paras('리셋을 올린 순간과 그 다음 상승 에지를 파형에서 구분한다.','각 모듈의 리셋 우선순위를 읽는다. Mealy의 조합 출력은 입력에도 의존한다.'))
    frame('nonblocking은 이전 값을 전달한다',paras('두 레지스터 A와 B가 있고, 같은 에지에서 A에 입력을 저장하고 B에 A를 전달한다고 하자.')+table(['에지 직전','입력','에지 직후'],[('A = 0xA, B = 0','3','A = 3, B = 0xA'),('A = 3, B = 0xA','3','A = 3, B = 3')])+paras('0xA는 16진수 표기다. B는 같은 에지에서 갱신되기 전 A를 받는다.','순차회로의 저장값은 <=로 갱신한다. 조합 계산은 별도 always @*에서 =를 사용한다.'))
    frame('버튼을 클록으로 쓰기 전에',paras('기계식 버튼은 한 번 눌러도 접점이 여러 번 튈 수 있다. FPGA 클록과도 동기화되어 있지 않다.','최신판의 입력 처리 순서는 동기화 → 안정 시간 확인 → 한 클록 펄스다.','동기화 플립플롭 두 단계는 메타안정성이 전달될 위험을 낮춘다. 디바운스는 접점의 반복 변화를 걸러낸다.','시뮬레이션은 메타안정성의 아날로그 현상 자체를 검증하지 않는다. 버튼 잡음 자극과 펄스 수를 검사한다.'))
    frame('clock-enable과 분주 출력',paras('분주 출력은 느린 주기를 LED나 파형으로 관찰할 때 사용한다.','다른 회로의 저장소는 공통 clk를 유지하고, tick이 1인 상승 에지에서만 동작시킨다.','DIVISOR = 10이면 tick이 열 클록마다 한 번 소비된다. tick은 소비할 에지 직전부터 1이다.','실제 클록 주파수와 분주 수의 비가 원하는 속도인지 계산한다.'))
    frame('11 · 업/다운 카운터',table(['자극','기대 결과'],[('증가 16회','0 → … → 15 → 0'),('0에서 감소','15'),('enable = 0','값 유지'),('rst와 enable 모두 1','리셋 우선')])+paras('수정 실험: 증가량을 1에서 2로 바꾼다. 첫 증가 에지의 기대값과 실제값을 비교한 뒤 복구한다.'))
    frame('12 · 클록 분주',table(['DIVISOR = 10','관찰'],[('리셋 해제 뒤 1–4번째 에지','출력 0'),('5번째 에지','출력 1'),('10번째 에지','출력 0, 주기 반복'),('30클록','enable 소비 3회')])+paras('수정 실험: 첫 전이를 한 클록 늦춘다. 주기가 같더라도 듀티와 첫 전이가 달라졌는지 확인한다.'))
    frame('13 · 레지스터 저장과 이동',table(['제어','기대 결과'],[('load만 1','stored에 입력 저장'),('transfer만 1','value에 stored 전달'),('둘 다 1','value는 이전 stored를 받음'),('둘 다 0','두 저장값 유지')])+paras('수정 실험: 전달 대상을 stored에서 현재 data_in으로 바꾼다. 입력과 저장값이 다른 경우를 관찰한다.'))
    frame('14 · 시프트 레지스터',table(['순서대로 넣는 입력','저장값'],[('1','1000'),('0','0100'),('1','1010'),('0','0101')])+paras('새 입력은 bit 3으로 들어오고 기존 값은 bit 0 방향으로 이동한다.','수정 실험: 이동 방향을 반대로 바꾸고 첫 불일치 위치를 찾는다.'))
    frame('15 · PISO',paras('1010을 병렬 로드하면 직렬 출력은 먼저 최상위 비트 1이다.')+table(['읽는 시점','직렬 출력'],[('로드 뒤, 첫 shift 전','1'),('한 번 shift 뒤','0'),('두 번 shift 뒤','1'),('세 번 shift 뒤','0')])+paras('네 번째 shift 뒤 저장값은 0000이다. load와 enable이 동시에 1이면 load가 우선한다.'))
    frame('16 · Moore 상태 머신',table(['현재 상태','advance = 1인 유효 에지 뒤'],[('00','01'),('01','10'),('10','00')])+paras('enable과 advance가 모두 1일 때만 전이한다.','출력은 상태다. 클록 사이에 advance만 바꿔도 출력은 바뀌지 않는다.','수정 실험: 01의 다음 상태를 00으로 바꾸고 원래 전이표와 비교한다.'))
    frame('17 · Mealy 상태 머신',table(['상태','입력 0 출력','입력 1 출력'],[('S0','00','10'),('S1','00','01')])+paras('유효 에지에서 입력이 1이면 S0↔S1로 전이한다. 입력이 0이면 유지한다.','출력은 현재 상태와 현재 입력에 의존한다. 입력 1을 유지한 채 전이하면 에지 뒤 출력도 바뀐다.','enable = 0은 상태만 멈춘다. 입력에 따른 조합 출력 변화는 계속된다.'))
    frame('18 · 7세그먼트 자리 스캔',paras('8자리 중 한 자리만 켜고 순서대로 반복한다. 눈에는 여러 자리가 함께 보인다.','자리 전환 사이에는 모든 자리 선택을 0으로 하는 blank 구간을 둔다. 다음 자리 데이터가 안정될 시간을 확보한다.','기능 코어는 active-high 논리값을 낸다. 실제 보드의 선택·세그먼트 극성은 핀 연결 모듈에서 맞춘다.','수정 실험: blank 구간을 제거하고 자기검사가 어떤 조건에서 실패하는지 찾는다.'))
    frame('VS Code 시뮬레이션 실행',steps('File → Save All로 RTL·TB·설정을 저장한다.','Terminal → Run Task... → 02 Simulate를 누른다.','Terminal에서 LAB2_PASS와 검사 수, 종료 시각을 확인한다.','Terminal → Run Task... → 03 Open waveform을 누른다.','clk·rst·제어 입력·상태·출력을 추가하고 상승 에지를 확대한다.'))
    frame('오류를 읽는 순서',steps('문법 오류: 파일 경로와 행 번호를 확인한다. 이전 행의 세미콜론도 확인한다.','자기검사 실패: LAB2_FAIL 뒤 검사 이름과 시각을 읽는다.','그 시각 직전의 입력과 현재 상태로 기대값을 다시 계산한다.','RTL만 수정하고 TB 기대값을 임의로 바꾸지 않는다.','복구·저장·재실행 후 새 PASS 로그와 새 파형을 보관한다.'))
    frame('실험 전 레포트',steps('회로의 상태표·리셋·enable·출력 시점을 설명한다.','주요 RTL과 TB의 역할을 자기 말로 설명한다.','정상/변경/복구의 3행 비교표에 로그와 결과를 정리한다.','상승 에지 전후를 확대한 VS Code 파형으로 예상값을 설명한다.','Vivado에 등록할 RTL·TB·XDC·top·장비 클록 조건을 적는다.'),'reports')
    frame('실험 후 레포트',steps('Vivado 기능 시뮬레이션과 VS Code 결과를 비교한다.','합성·구현 결과, 경고 해석, 핀과 타이밍 조건, bit 파일을 기록한다.','장치 프로그램 화면과 실제 입출력 사진·영상을 첨부한다.','통합판은 버튼 모드 전환·LCD 모드명·회로 출력을 함께 보여 준다.','GitHub에 소스·레포트·관찰 자료를 연결하고 미수행 항목을 구분한다.'))
    frame('CLI 통합판의 구현 경로',paras('기능 검증까지는 동일한 빈 템플릿과 Icarus를 사용한다.','이후 Yosys 합성 → nextpnr 배치배선 → 프레임 변환 → S75 bit 생성·검사 순서다.','장치에 기록할 때 openFPGALoader로 연결 장치를 확인하고 생성한 bit를 지정한다.','장치 모델·패키지·핀 제약·bit 대상이 일치해야 한다. 도구 실행 성공과 실제 보드 동작 성공을 구분해 기록한다.'))
    header=r'''% !TEX program = xelatex
\input{shared/lab2_preamble.tex}
\renewcommand{\legacySource}[1]{}
\hypersetup{pdftitle={LAB2 순차논리 공통 예습}}
\newcommand{\terminalbox}[1]{\par\vspace{0.15cm}{\setlength{\fboxsep}{7pt}\colorbox{black}{\parbox{\dimexpr\textwidth-14pt\relax}{\color{white}\ttfamily\fontsize{7}{9}\selectfont #1}}}\par\vspace{0.15cm}}
\begin{document}
\renewcommand{\small}{\fontsize{9}{12}\selectfont}
\setlength{\leftmargini}{1.4em}
'''
    (BASE/'05.LAB2_00_START.tex').write_text(header+'\n'.join(pages)+'\\end{document}\n',encoding='utf-8')
    print('LAB2 common primer:',len(pages),'pages')

if __name__=='__main__': main()
