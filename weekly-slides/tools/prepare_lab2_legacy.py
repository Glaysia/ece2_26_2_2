"""Pair executable LAB2 lessons with untouched original legacy reference files."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'
OLD=ROOT/'legacy/notebook/cpp/verilog'
ORIGINALS={
 '01_counter':['W5/16_Counter/src/top.v','W5/16_Counter/src/tb.v','W5/16_Counter/src/pin.xdc'],
 '02_clock_divider':['W5/17_ClkDiv/src/top.v','W5/17_ClkDiv/src/tb.v','W5/17_ClkDiv/src/pin.xdc'],
 '03_register':['W6/Srcs/26top.v','W6/Srcs/26const.xdc'],
 '04_shift_register':['W6/Srcs/27top.v','W6/Srcs/27tb.v','W6/Srcs/27const.xdc'],
 '05_piso':['W6/Srcs/28top.v','W6/Srcs/28const.xdc'],
 '06_moore':['W8/srcs/29mooreTop.v','W8/srcs/29mooreTb.v','W8/srcs/29mooreConst.xdc'],
 '07_mealy':['W8/srcs/30mealyTop.v','W8/srcs/30mealyTb.v','W8/srcs/30mealyConst.xdc'],
 '08_segment_scan':['W4/12_seg_decoder_array/seg_decoder_array.v','W4/12_seg_decoder_array/tb.v','W4/12_seg_decoder_array/pin.xdc']
}
NOTES={
 '01_counter':'원본 updn=1은 증가다. 현재 core의 down=1은 감소다. 원본은 비동기 리셋과 blocking 할당을 사용하며 현재 회로는 동기 리셋·enable·nonblocking을 사용한다.',
 '02_clock_divider':'원본은 100 Hz 입력의 /2·/10·/50 출력을 관찰한다. 현재 보드는 1 kHz로 통일해 같은 비율과 /1000=1 Hz 기준을 함께 보여 준다. 원본의 서로 다른 always 블록에 있는 blocking 갱신은 실행 순서에 따른 시뮬레이션 경쟁을 일으킬 수 있다.',
 '03_register':'원본은 저장과 전달 버튼 각각을 클록으로 사용한다. 현재 회로는 단일 clk에서 load와 transfer를 사용하며, 둘이 동시에 1일 때 이전 저장값 전달을 검사한다.',
 '04_shift_register':'원본과 현재 회로 모두 입력을 MSB로 넣고 LSB로 이동한다. 현재 회로는 초기 상태를 정하는 reset, 한 단계 실행 enable, 자동 검사와 종료 조건을 추가했다. 원본 TB는 종료 조건 없이 클록을 계속 생성한다.',
 '05_piso':'원본은 shldn의 상승 에지와 clk의 상승 에지를 한 always 블록에 묶고 데이터에 의존하는 비동기 로드를 사용한다. 현재 회로는 하나의 clk와 동기 load 우선순위를 사용한다. 원본을 그대로 현대 FPGA의 일반 플립플롭에 합성할 수 있다고 가정하지 않는다.',
 '06_moore':'원본은 x를 버튼 클록으로 사용하고 전용 클록 배선 검사를 해제한다. 현재 회로는 실제 주 클록과 디바운스된 enable을 쓴다. Moore와 Mealy의 구분은 출력이 상태에만 의존하는지, 상태와 입력 모두에 의존하는지다. 원본 주석의 다음 상태 설명만으로 둘을 구분하면 안 된다.',
 '07_mealy':'원본은 x를 클록과 조합 출력 입력으로 함께 사용한다. 현재 회로는 clk·enable·bit_in을 나눠 입력 변경과 상태 전이를 따로 관찰한다. 원본의 CLOCK_DEDICATED_ROUTE FALSE를 현재 XDC에 옮기지 않는다.',
 '08_segment_scan':'원본 실습 12는 sel로 한 자리를 수동 선택하는 조합회로다. LAB2에서는 이를 시간 순서로 자동 선택하는 순차회로로 확장한다. 현재 코드는 8자리 순환·blanking·극성 변환을 포함한다. 원본의 bcd/sel 핀과 현재 sw/clk 핀 이름을 혼용하지 않는다.'
}

def main():
    circuits=json.loads((LAB/'circuits.json').read_text(encoding='utf-8'))
    manifest=[]
    for entry in circuits:
        source=LAB/entry['path']; target=LAB/'legacy'/source.name
        target.mkdir(parents=True,exist_ok=True)
        for directory in ['src','sim','constraints','tools']:
            shutil.copytree(source/directory,target/directory,dirs_exist_ok=True)
        for name in ['LAB1.code-workspace','simulation.json','simulation-board.json','board.json','.gitignore']:
            shutil.copyfile(source/name,target/name)
        (target/'original').mkdir(exist_ok=True); (target/'evidence').mkdir(exist_ok=True)
        archive=[]
        for name in ORIGINALS[source.name]:
            original=OLD/name; copied=target/'original'/original.name
            shutil.copyfile(original,copied)
            archive.append({'file':copied.relative_to(target).as_posix(),'source':original.relative_to(ROOT).as_posix(),
                            'sha256':hashlib.sha256(copied.read_bytes()).hexdigest()})
        shutil.copyfile(source/'evidence/board-pin-provenance.json',target/'evidence/board-pin-provenance.json')
        (target/'evidence/legacy-provenance.json').write_text(json.dumps({'files':archive,'differences':NOTES[source.name],
            'execution_files':'src/, sim/, constraints/ are the corrected single-clock lesson; original/ is preserved for comparison'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        readme=f'''# {entry['title']} · 레거시 자료와 비교

이 프로젝트는 원본 교안의 화면과 설계 의도를 읽고, 단일 클록으로 정리한 회로를 직접 작성·실행하는 실습이다. `original/`은 원본 파일을 바이트 그대로 보존한다. `src/`, `sim/`, `constraints/`가 실제 수업에서 실행할 파일이다.

{NOTES[source.name]}

학생은 `git clone --branch v2.0.0 https://github.com/Glaysia/fpga-lab-template.git lab2_legacy_{source.name}`으로 빈 프로젝트를 만들고 직접 작성한다. `LAB1.code-workspace`를 열어 추천 확장과 01/02/03 작업을 사용한다.

Vivado 설계 top: `{entry['board_top']}`. FPGA: `xc7s75fgga484-1`. 주 클록: 1 kHz. 실습 파일에는 원본과 달리 버튼 입력 동기화·디바운스가 포함된다.

{entry['controls']}

시뮬레이션은 `python tools/lab1.py simulate`. 원본 TB는 자동 PASS나 종료가 없을 수 있으므로 `original/`을 자동 컴파일 목록에 추가하지 않는다. 원본 GUI 화면에 나온 파일명·핀·클록 조건은 현재 프로젝트의 `board.json`·XDC·포트 표와 대조한다.

[원본 파일 해시와 차이](evidence/legacy-provenance.json). 실제 실행 결과는 별도 standalone 검증 기록으로 확인한다.
'''
        (target/'README.md').write_text(readme,encoding='utf-8')
        for edition,project in [('vivado_2026_1',source),('legacy',target)]:
            number=int(source.name[:2]); suffix=source.name.split('_',1)[1].upper()
            pdfnum=number if edition=='vivado_2026_1' else number+8
            manifest.append({**entry,'path':project.relative_to(LAB).as_posix(),'edition':edition,
                'id':edition+'_'+source.name,'pdf':f'05.LAB2_{pdfnum:02d}_{suffix}_'+('VIVADO' if edition=='vivado_2026_1' else 'LEGACY')+'.pdf',
                'student_folder':'lab2_'+('legacy_' if edition=='legacy' else '')+source.name,
                'status':'source-prepared','legacy_differences':NOTES[source.name] if edition=='legacy' else None})
    for edition in ['vivado_2026_1','opensource_cli']:
        project=LAB/edition/'09_integrated'
        manifest.append({'path':project.relative_to(LAB).as_posix(),'edition':edition,'id':edition+'_09_integrated',
            'title':'8모드 버튼·LCD 통합','top':'lab2_integrated','board_top':'lab2_integrated',
            'constraints':'constraints/lab2_integrated.xdc','student_folder':'lab2_integrated'+('_cli' if edition=='opensource_cli' else ''),
            'pdf':'05.LAB2_08'+('B_INTEGRATED_CLI' if edition=='opensource_cli' else 'A_INTEGRATED_VIVADO')+'.pdf','status':'source-prepared'})
    for project in manifest:
        (LAB/project['path']/'.gitattributes').write_text('* text=auto eol=lf\nsimulation*.json -text\nsrc/** -text\nsim/** -text\nconstraints/** -text\noriginal/** -text\n*.code-workspace -text\ntools/*.py -text\ntools/*.sh text eol=lf\n',encoding='utf-8')
    (LAB/'projects.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('18 project entries; 8 legacy source archives prepared')

if __name__=='__main__': main()
