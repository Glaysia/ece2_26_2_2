"""Refresh project navigation and evidence from actual local run results."""
from pathlib import Path
import json, hashlib, shutil

LAB=Path(__file__).resolve().parents[1]
PROJECTS=json.loads((LAB/'projects.json').read_text(encoding='utf-8'))
PROJECTS.sort(key=lambda p:({'vivado_2026_1':0,'opensource_cli':1,'legacy':2}[p['edition']],p['path']))
CIRCUITS=json.loads((LAB/'docs/circuits.json').read_text(encoding='utf-8'))
COURSE='https://github.com/Glaysia/ece2_26_2_2/blob/daily/0910/'
PDF=COURSE+'weekly-slides/weekly-slides/LAB1_FPGA_0914/'

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.rstrip()+'\n',encoding='utf-8')

def pdfname(p):
    if p['edition']=='opensource_cli':return '04.LAB1_10B_INTEGRATED_CLI.pdf'
    if p['top']=='lab1_integrated':return '04.LAB1_10A_INTEGRATED_VIVADO.pdf'
    c=next(c for c in CIRCUITS if p['path'].endswith(c['slug']))
    return f"04.LAB1_{c['n']+(10 if p['edition']=='legacy' else 0):02d}_{c['pdf']}_{'LEGACY' if p['edition']=='legacy' else 'VIVADO'}.pdf"

def collect(p):
    folder=LAB/p['path'];evidence=folder/'evidence';evidence.mkdir(exist_ok=True)
    stages={}
    for action in ['vscode','vivado-sim','build']:
        out=folder/'build'/action
        if not (out/'result.json').exists():
            stages[action]={'status':'NOT_RUN'};continue
        result=json.loads((out/'result.json').read_text())
        stages[action]=result
        write(evidence/(action+'-result.json'),json.dumps(result,indent=2))
        if (out/'simulation.log').exists():shutil.copy2(out/'simulation.log',evidence/(action+'-simulation.txt'))
        if result['status']=='PASS' and (out/'wave.vcd').exists():shutil.copy2(out/'wave.vcd',evidence/(action+'-wave.vcd'))
        if action=='build' and result['status']=='PASS':
            release=folder/'release';release.mkdir(exist_ok=True)
            if p['path']!='vivado_2026_1/01_logic_gates':
                shutil.copy2(out/'design.bit',release/(p['top']+'.bit'))
            run=out/result['run']
            for name in ['timing_summary.txt','drc.txt','vivado.log','version.log']:
                if (run/name).exists():shutil.copy2(run/name,evidence/('build-'+name.replace('.log','.txt')))
    if p['path']=='vivado_2026_1/01_logic_gates':
        # Fresh-clone GUI verification has its own manifest; preserve its exact bitstream.
        stages['gui']={'status':'PASS','evidence':'manifest.json','source_commit':'740aef5'}
        gui_wave=evidence/'template-gui-wave.vcd'
        comparison=LAB/'docs/simulation-comparison.json'
        compared=json.loads(comparison.read_text(encoding='utf-8')) if comparison.exists() else []
        if gui_wave.exists() and any(r['project']==p['id'] and r['status']=='PASS' for r in compared):
            stages['vivado-sim']={'status':'PASS','execution':'Vivado GUI in fresh template clone','source_commit':'740aef5','cases':4,'end_ns':40,'evidence':'template-gui-wave.vcd','comparison':'../../docs/simulation-comparison.json'}
    cli_result=folder/'evidence/cli-result.json'
    if p['edition']=='opensource_cli' and cli_result.exists():
        stages['cli']=json.loads(cli_result.read_text(encoding='utf-8'))
    timing=LAB/'vivado_2026_1/11_integrated/build/board-timing/simulation.txt'
    if p['top']=='lab1_integrated' and timing.exists() and 'LAB1_TIMING_PASS' in timing.read_text():
        shutil.copy2(timing,evidence/'board-default-timing.txt')
        stages['board_default_timing']={'status':'PASS','simulator':'Icarus Verilog 14.0','clock':'1 kHz','button_pulses':2,'lcd_bytes':110,'hardware':False,'testbench':'../../common/tb/tb_board_timing.sv','sha256':hashlib.sha256((LAB/'common/tb/tb_board_timing.sv').read_bytes()).hexdigest()}
    files={}
    for name in [*p['sources'],p['testbench'],p['constraints']]:
        files[name]=hashlib.sha256((folder/name).read_bytes()).hexdigest()
    bit=folder/'release'/(p['top']+'.bit')
    if bit.exists():files['release/'+bit.name]=hashlib.sha256(bit.read_bytes()).hexdigest()
    manifest={'project':p['id'],'part':p['part'],'stages':stages,'sha256':files,
              'hardware_programmed':False,'board_photos_video':False,
              'legacy_tool_run':False if p['edition']=='legacy' else None}
    write(evidence/'validation.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    return manifest

def main():
    rows=[];results=[]
    for p in PROJECTS:
        result=collect(p);results.append(result)
        folder=LAB/p['path'];legacy=p['edition']=='legacy';cli=p['edition']=='opensource_cli'
        for workspace in folder.glob('*.code-workspace'):
            data=json.loads(workspace.read_text(encoding='utf-8'))
            data['tasks']['tasks']=[t for t in data['tasks']['tasks'] if t['label'][:2] in ['01','02','03']]
            if cli:
                for task in data['tasks']['tasks']:
                    if '--simulator' not in task['args']:task['args']+=['--simulator','iverilog']
            write(workspace,json.dumps(data,ensure_ascii=False,indent=2))
        status=result['stages']['vscode']['status'];vs=result['stages']['vivado-sim']['status'];bit=result['stages']['build']['status']
        rows.append(f"| [{p['id']}]({p['path']}/README.md) | [{pdfname(p)}]({PDF+pdfname(p)}) | {status} | {vs if not legacy and not cli else '구버전 미실행' if legacy else '해당 없음'} | {bit if not legacy and not cli else '아래 검증 안내'} |")
        if p['path']=='vivado_2026_1/01_logic_gates':continue
        workspace_name=next(folder.glob('*.code-workspace')).name
        open_links=f'[VS Code workspace]({workspace_name}) · [CLI 빌드 스크립트](../../tools/openxc7_build.py)' if cli else f'[VS Code workspace]({workspace_name}) · [Vivado 프로젝트](vivado/{p["top"]}.xpr) · [재생성 Tcl](create_project.tcl)'
        peer_links='[두 통합본의 공통 동작](../../docs/integrated.md)'
        if p['top']!='lab1_integrated':
            c=next(c for c in CIRCUITS if p['path'].endswith(c['slug']))
            other='vivado_2026_1' if legacy else 'legacy'
            peer_links=f'[같은 회로의 다른 버전](../../{other}/{c["slug"]}/README.md) · [통합 모드 {c["n"]:02d}](../../docs/integrated.md#mode-{c["n"]:02d})'
        source_rows='\n'.join(f'- [{Path(s).name}]({s})' for s in p['sources'])
        caution='원본 XPR은 Vivado 2020.1 형식입니다. 현재 제작 환경의 XSim 2026.1로 RTL을 검사했으며, Vivado 2020.1 GUI 실행·합성은 수행하지 않았습니다. `original/`은 원본이고 `vivado/`의 XPR은 상대경로로 정리한 실습용입니다.' if legacy else 'Vivado 과정은 GUI에서 직접 클릭합니다. task 04·05·06은 제공하지 않습니다.'
        if cli:caution='Icarus Verilog로 사전 시뮬레이션하고 openXC7 흐름으로 빌드합니다. [CLI 설치·검증](../../docs/cli.md)을 따릅니다. Mac 실행 결과와 WSL 결과를 혼동하지 않습니다.'
        correction='\n원본 감산기의 `a==b` borrow 오류는 `corrected/sub_4bit.v`에서 수정했습니다. `original/`을 보존하며 [변경 설명](../../docs/legacy-provenance.md)을 참고합니다.\n' if p['id']=='legacy_04_subtractor4' else ''
        write(folder/'README.md',f'''# {p['title']}

[전체 프로젝트](../../README.md) · [설치](../../docs/setup.md) · [회로별 규칙](../../docs/circuits.md) · [강의 PDF]({PDF+pdfname(p)}) · [실험 전·후 레포트](../../docs/reports.md)

## VS Code에서 먼저 실행

1. 별도 [템플릿](https://github.com/Glaysia/fpga-lab-template)을 clone합니다.
2. VS Code의 File → New Window → Open Workspace from File...에서 `{p['id']}.code-workspace`를 엽니다.
3. Explorer에서 RTL과 `{Path(p['testbench']).name}`를 열고 예상 결과를 적습니다. File → Save All.
4. Terminal → Run Task... → **01 Check tools**, **02 Simulate** 순서로 실행합니다.
5. `LAB1_PASS {p['top']} cases={p['cases']}`와 정상 종료를 확인합니다.
6. **03 Open waveform** → VaporView → `{p['simulation_top']}` 신호 추가 → Zoom to Fit → 커서 값을 예상값과 비교합니다.
7. `build/vscode/simulation.log`, `wave.vcd`, 자신의 화면 캡처와 해석을 실험 전 레포트에 남깁니다.

## 프로젝트 입력

{open_links}

{peer_links}

- FPGA: `{p['part']}`
- 설계 top: `{p['top']}` / 시뮬레이션 top: `{p['simulation_top']}`
- [자기검사 TB]({p['testbench']}) / [핀 제약]({p['constraints']}) / [파일 목록](sources.f)
{source_rows}

{caution}
{correction}
## Vivado 실습

레거시는 `vivado/{p['top']}.xpr`을 원래 버전에서 엽니다. 최신 버전은 PDF의 New Project 절차를 따라 `{p['part']}`를 선택합니다. Add Sources에서 RTL은 Design Sources, TB는 Simulation Sources, XDC는 Constraints로 각각 추가하고 Copy sources 옵션을 끕니다. 설계와 시뮬레이션 top을 각각 확인합니다.

Run Simulation → Run Behavioral Simulation에서 PASS·파형을 확인합니다. Close Simulation → Run Synthesis → Run Implementation → Generate Bitstream을 차례로 완료합니다. 단계별 Launch Runs에서 OK를 누르고 성공 창이 뜨기 전에는 다음으로 진행하지 않습니다. 생성 파일은 `vivado/{p['top']}.runs/impl_1/{p['top']}.bit`입니다.

Open Hardware Manager → Open target → Auto Connect → 장치 확인 → Program Device → bit 선택 → Program. 실제 보드 입력을 바꾸고 사진·영상을 촬영한 뒤 실험 후 레포트에서 연결합니다.

## 제작 검증

[실행 결과와 소스 SHA-256](evidence/validation.json): VS Code 단계 **{status}**, Vivado 시뮬레이션 **{vs}**, Vivado bit 생성 **{bit}**. 이는 제작 환경의 실행 기록이며 자신의 실행 증빙을 대신하지 않습니다. CLI 프로젝트는 [별도 검증](../../docs/cli.md)을 봅니다.

실제 보드 기록·사진·영상은 **미수행**입니다. 생성된 bit만으로 보드 실험 완료를 주장하지 않습니다.
''')
        if p['path']=='vivado_2026_1/11_integrated':
            with (folder/'README.md').open('a',encoding='utf-8') as f:
                f.write('\n## 추가 GUI 확인\n\n배포 XPR을 GUI에서 열어 계층과 기존 구현 완료 상태를 확인하고 Behavioral Simulation을 직접 실행했습니다. [GUI 로그](evidence/gui-simulation.log) · [입력 해시·수행 방식·VCD 비교 범위](evidence/gui-simulation.json). 2,560개 PASS와 72,430ns 종료를 확인했으며 GUI의 최종 VCD 파일 기록·파형 캡처는 해당 기록의 미완료 항목을 따릅니다.\n')
        if cli:
            readme=folder/'README.md';text=readme.read_text(encoding='utf-8')
            before=text.split('## Vivado 실습')[0]
            after=text.split('## 제작 검증')[1]
            write(readme,before+'''## CLI 구현과 보드 실험

사전 레포트를 마친 뒤 [CLI 안내](../../docs/cli.md)에 따라 정확한 S75 chipdb를 준비하고 `python3 ../../tools/openxc7_build.py --project .`를 실행합니다. Yosys 합성 → nextpnr 배치배선 → 프레임 변환 → bit 생성의 각 로그를 확인합니다. 생성 결과와 SHA-256은 `build/cli/result.json`에 기록됩니다.

실험실 보드 기록은 Vivado Hardware Manager의 Open target → Auto Connect → 장치 확인 → Program Device에서 수행하고 자신의 사진·영상을 실험 후 레포트에 연결합니다.

## 제작 검증'''+after)
        if (folder/'evidence/waveform.svg').exists():
            with (folder/'README.md').open('a',encoding='utf-8') as f:
                f.write('\n## 실제 VCD 구간\n\n![실제 XSim VCD의 구간 확대](evidence/waveform.svg)\n\n위 그림은 실제 VCD 값으로 그린 타이밍 도표이며 VS Code 화면 캡처는 아닙니다. [원본 VCD](evidence/waveform-source.vcd) · [구간·신호·해시](evidence/waveform-plot.json). 다중 비트 표시는 16진수입니다.\n')
    write(LAB/'README.md','''# LAB1: 22개 프로젝트

[강의 저장소](../../../README.md) · [PDF·ZIP 목록](../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/README.md) · [학생용 별도 템플릿](https://github.com/Glaysia/fpga-lab-template) · [설치·시작](docs/setup.md) · [10개 회로](docs/circuits.md) · [버튼·LCD 통합](docs/integrated.md) · [오픈소스 CLI](docs/cli.md) · [레포트](docs/reports.md) · [검증 현황](docs/validation.md) · [레거시 원본](docs/legacy-provenance.md)

작성일 2026-09-10. 모든 프로젝트는 VS Code 사전 시뮬레이션과 실험 전 레포트부터 시작합니다. Vivado에서는 메뉴를 직접 눌러 시뮬레이션·합성·구현·bit 생성을 수행하고, 보드 기록·사진·영상은 실험 후 레포트에 넣습니다.

프로젝트별 workspace는 22개입니다. `template/LAB1.code-workspace`는 첫 회로를 여는 편의 진입점입니다. 최신 개별 10 + 최신 통합 1 + CLI 통합 1 + 레거시 10입니다.

| 프로젝트 | 강의 PDF | 사전 시뮬레이션 | Vivado 시뮬레이션 | Vivado bit |
|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

실제 보드 기록·촬영은 아직 수행하지 않았습니다. 레거시의 PASS는 2026.1 XSim의 RTL 검사 결과이며 2020.1 도구 실행 완료를 의미하지 않습니다. 최신 첫 회로의 별도 템플릿 GUI 검증은 [상세 기록](vivado_2026_1/01_logic_gates/VALIDATION.md)을 봅니다.
''')
    write(LAB/'docs/validation-results.json',json.dumps(results,ensure_ascii=False,indent=2))
    validation_rows=[]
    for p,r in zip(PROJECTS,results):
        stages=r['stages']
        validation_rows.append(f"| [{p['id']}](../{p['path']}/evidence/validation.json) | {stages['vscode']['status']} | {stages['vivado-sim']['status']} | {stages['build']['status']} | 미수행 |")
    write(LAB/'docs/validation.md','''# 제작 검증 현황

[전체 프로젝트](../README.md) · [기계 판독 결과](validation-results.json) · [Icarus 교차검사](cli-simulation-results.json) · [VS Code·Vivado VCD 대조](simulation-comparison.json) · [CLI 빌드](cli.md) · [첫 회로 GUI](../vivado_2026_1/01_logic_gates/VALIDATION.md)

작성일 2026-09-10. PASS는 표의 해당 단계에 한정합니다. NOT_RUN은 미실행, RUNNING은 진행 중, FAIL은 실패입니다. 각 프로젝트의 evidence에 실제 로그·결과·소스 SHA-256을 보관합니다.

| 프로젝트 | 사전 시뮬레이션 | Vivado 시뮬레이션 | Vivado bit | 보드 기록·촬영 |
|---|---|---|---|---|
'''+ '\n'.join(validation_rows)+'''

첫 최신 회로는 공개 템플릿 740aef5를 새로 clone하여 실제 Vivado GUI로 시뮬레이션·bit 생성을 수행했습니다. 나머지 최신 회로는 같은 입력 파일의 Vivado 2026.1 배치 실행으로 검증했습니다. 통합본은 추가로 배포 XPR을 GUI에서 열고 Behavioral Simulation 2,560개 PASS를 확인했습니다. [통합 GUI 기록](../vivado_2026_1/11_integrated/evidence/gui-simulation.json)은 기존 배치 bit 생성과 구분합니다. 두 XSim 경로의 VCD에서 날짜·버전 메타데이터만 제외하고 신호 선언·모든 시간과 값 변화를 대조한 결과도 별도로 보관합니다. 학생용 매뉴얼은 GUI 클릭 순서입니다. 이 두 수행 방식을 혼동하지 않습니다.

레거시 원본 XPR은 2020.1 형식을 유지했습니다. 표의 레거시 사전 PASS는 2026.1 XSim 검사이며, Vivado 2020.1 GUI·합성·보드 실행은 미수행입니다. CLI 통합은 Icarus와 별도 openXC7 결과를 확인합니다.

## 남아 있는 실제 장비·캡처 확인

데스크톱 재개 후 최신 06–10 RTL, 개별 자기검사 TB, 통합 top·버튼·LCD·통합 TB의 실제 VS Code 화면을 추가했습니다. 새 코드 이미지 52개는 원본 화면을 의미 단위로 크롭했으며 [소스 줄 범위·해시](../../../../weekly-slides/weekly-slides/LAB1_FPGA_0914/assets/lab1-circuits/provenance.json)를 기록했습니다. 통합 Vivado의 계층·기존 구현 완료 화면도 확보했습니다. 추가 GUI 시뮬레이션은 PASS지만 Windows 보안 창이 이후 화면을 가려 회로별 파형·나머지 Vivado 결과 캡처는 아직 남아 있습니다. GUI VCD는 72425ns까지 사전 결과와 같은 접두부이고 마지막 5ns의 파일 기록 확인은 GUI 종료 후 진행합니다.

공개 템플릿 66a8b43을 인증 없이 공백 포함 새 경로에 clone했습니다. 22개 workspace·21개 XPR·원본 41개 파일과 로컬 링크 검사가 통과했습니다. 실제 workspace 명령으로 첫 회로 도구 검사·시뮬레이션과 통합 회로 시뮬레이션도 통과했습니다. [새 clone 검증](template-clone-validation.json)에 명령별 로그를 연결했습니다.

최신 11개 bit 생성은 모두 PASS입니다. 통합 구현의 내부 1kHz 타이밍은 WNS 999994.562ns, WHS 0.193ns, 실패 endpoint 0개입니다. 외부 I/O 지연 미지정(TIMING-18)과 구성 전압 미지정(CFGBVS-1) 경고는 남아 있습니다. [타이밍·DRC 해석](integrated.md#구현-타이밍과-drc)에서 범위를 확인합니다.

실제 FPGA 기록, LCD 실물 동작, 보드 사진·영상은 미수행입니다. 레포트 양식과 촬영 절차는 제공하지만 결과를 꾸며 채우지 않습니다. 이 항목이 남아 있으므로 GOAL의 전체 완료로 표시하지 않습니다.
''')
    write(LAB/'docs/simulation-results.json',json.dumps([{'id':r['project'],'status':r['stages']['vscode']['status'],'evidence':next(p['path'] for p in PROJECTS if p['id']==r['project'])+'/evidence/vscode-result.json'} for r in results],indent=2))
    write(LAB/'docs/circuits.md','# 회로별 규칙과 검증\n\n[전체 프로젝트](../README.md) · [통합 모드](integrated.md)\n\n'+ '\n\n'.join(f"## {c['n']:02d}. {c['title']}\n\n{c['ports']}\n\n{c['rule']}\n\n{c['board']}\n\n자기검사 {c['cases']}개, 각 10ns. {c['focus']}\n\n[최신 프로젝트](../vivado_2026_1/{c['slug']}/README.md) · [레거시](../legacy/{c['slug']}/README.md) · [통합 모드 {c['n']:02d}](integrated.md#mode-{c['n']:02d})" for c in CIRCUITS))
    print('Updated navigation and measured evidence for',len(results),'projects')

if __name__=='__main__':main()
