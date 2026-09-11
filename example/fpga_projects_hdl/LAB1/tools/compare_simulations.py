"""Compare standalone VS Code and Vivado project VCDs, excluding date/version metadata."""
from pathlib import Path
import json,re,hashlib,sys
LAB=Path(__file__).resolve().parents[1]
def canonical(path):
 text=path.read_text(encoding='utf-8')
 text=re.sub(r'\$(date|version)\b.*?\$end','',text,flags=re.S)
 return ' '.join(text.split()).encode()
def main():
 rows=[]
 for p in json.loads((LAB/'projects.json').read_text(encoding='utf-8')):
  if p['edition']!='vivado_2026_1':continue
  folder=LAB/p['path'];a=folder/'build/vscode/wave.vcd';b=folder/'build/vivado-sim/wave.vcd'
  if p['path']=='vivado_2026_1/01_logic_gates':b=folder/'evidence/template-gui-wave.vcd'
  row={'project':p['id'],'standalone':a.relative_to(LAB).as_posix(),'vivado':b.relative_to(LAB).as_posix(),'method':'All VCD declarations, timestamps and value changes; whitespace normalized; date/version blocks excluded.'}
  if not a.exists() or not b.exists():row['status']='NOT_RUN'
  else:
   va,vb=canonical(a),canonical(b)
   row.update(status='PASS' if va==vb else 'FAIL',standalone_sha256=hashlib.sha256(va).hexdigest(),vivado_sha256=hashlib.sha256(vb).hexdigest())
  rows.append(row)
 (LAB/'docs/simulation-comparison.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(rows,indent=2))
 if any(r['status']!='PASS' for r in rows):sys.exit(1)
if __name__=='__main__':main()
