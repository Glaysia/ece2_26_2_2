from pathlib import Path
import json,re,hashlib,xml.etree.ElementTree as ET,sys
from urllib.parse import unquote
lab=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
ps=json.loads((lab/'projects.json').read_text());assert len(ps)==22
assert len({p['id'] for p in ps})==22
assert sum(p['edition']=='legacy' for p in ps)==10
assert sum(p['edition']=='vivado_2026_1' for p in ps)==11
assert sum(p['edition']=='opensource_cli' for p in ps)==1
errors=[];xprs=0
for p in ps:
 folder=lab/p['path'];cfg=json.loads((folder/'project.json').read_text())
 assert cfg['id']==p['id'] and cfg['sources']==p['sources'],p['id']
 for rel in [*p['sources'],p['testbench'],p['constraints']]:assert (folder/rel).is_file(),(p['id'],rel)
 ws=list(folder.glob('*.code-workspace'));assert len(ws)==1,p['id']
 data=json.loads(ws[0].read_text(encoding='utf-8'));tasks=data['tasks']['tasks'];assert len(tasks)==3
 assert [t['label'][:2] for t in tasks]==['01','02','03']
 for task in tasks:assert (folder/task['args'][0]).is_file(),(p['id'],task)
 for f in data['folders']:assert (folder/f['path']).is_dir()
 for xpr in (folder/'vivado').glob('*.xpr'):
  xprs+=1;tree=ET.parse(xpr)
  for f in tree.findall('.//File'):
   path=f.get('Path','').replace('$PPRDIR',str(xpr.parent))
   assert '$' not in path and Path(path).is_file(),(p['id'],path)
  for fs in tree.findall('.//FileSet'):
   for opt in fs.findall('./Config/Option'):
    if opt.get('Name')=='TopModule' and fs.get('Name') in ['sources_1','sim_1']:
     assert opt.get('Val')==(p['top'] if fs.get('Name')=='sources_1' else p['simulation_top'])
 for line in (folder/'sources.f').read_text().splitlines():
  if not line.strip() or line.startswith(('#','+','-')):continue
  assert (folder/line.strip().strip('"')).is_file(),(p['id'],line)
for md in [lab/'README.md',*(lab/'docs').glob('*.md'),*(lab/'reports').rglob('*.md'),*[lab/p['path']/'README.md' for p in ps]]:
 content=md.read_text(encoding='utf-8')
 content=re.sub(r'```[\s\S]*?```|`[^`]*`','',content)
 for target in re.findall(r'\]\(([^)]+)\)',content):
  if '://' in target or target.startswith('#') or target.startswith('mailto:'):continue
  target=unquote(target.split('#')[0])
  if target and not (md.parent/target).exists():errors.append((str(md.relative_to(lab)),target))
assert xprs==21, ('Expected 21 Vivado XPR files',xprs)
originals=0
for provenance in (lab/'legacy').glob('*/provenance.json'):
 for item in json.loads(provenance.read_text(encoding='utf-8')):
  original=lab/item['file']
  assert hashlib.sha256(original.read_bytes()).hexdigest()==item['sha256'],str(original)
  originals+=1
print(json.dumps({'original_files_verified':originals,'projects':len(ps),'workspaces':22,'xprs':xprs,'broken_links':errors},ensure_ascii=False,indent=2))
if errors:sys.exit(1)
