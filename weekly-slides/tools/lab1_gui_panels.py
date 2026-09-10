"""Crop only actual Vivado screenshots; retain hashes and the GUI run they show."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB1'
ASSETS=ROOT/'weekly-slides/weekly-slides/LAB1_FPGA_0914/assets/latest-gui'
def main():
 from PIL import Image
 records=[]
 circuits=json.loads((LAB/'docs/circuits.json').read_text(encoding='utf8'))
 for c in circuits:
  number=c['n'];prefix=f'{number:02d}'
  evidence=LAB/f"vivado_2026_1/{c['slug']}/evidence/gui-simulation.json"
  if not evidence.exists():continue
  result=json.loads(evidence.read_text(encoding='utf8'));assert result['standalone_comparison']['status']=='PASS'
  for suffix,source,box in [('wave-crop','wave',[720,240,1468,275+28*len(c['signals'])]),('pass-crop','pass',[315,736,650,797]),('build-crop','project',[269,737,649,831])]:
   raw=ASSETS/f'{prefix}-{source}.png';out=ASSETS/f'{prefix}-{suffix}.png'
   if not raw.exists():continue
   im=Image.open(raw);assert im.size==(1486,943);im.crop(box).save(out)
   records.append({'image':out.name,'original':raw.name,'crop_box':box,'original_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'gui_evidence':evidence.relative_to(ROOT).as_posix(),'method':'Actual Vivado 2026.1 GUI; crop only','signals_top_to_bottom':c['signals'] if source=='wave' else None,'date':'2026-09-10'})
 (ASSETS/'provenance.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (ASSETS/'README.md').write_text('# 개별 회로의 실제 Vivado GUI 화면\n\n각 프로젝트를 열고 Behavioral Simulation을 직접 실행했습니다. 파형과 PASS 로그를 캡처한 후 시뮬레이터를 정상 종료하여 최종 VCD를 비교했습니다. project 화면은 기존 배치 빌드의 구현 완료 상태를 GUI에서 확인한 기록입니다. [크롭·원본 해시·GUI 실행 증거](provenance.json). 새 PNG는 추적하지 않고 PDF에 포함합니다.\n',encoding='utf8')
 print('Prepared',len(records),'actual individual GUI panels')
if __name__=='__main__':main()
