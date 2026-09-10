"""Build the 22 LAB1 manuals, contents, and setup guides in an isolated output folder.

MiKTeX may read old auxiliary files from the source cwd before the output folder.
Refuse that ambiguous state; preserve or move those generated files before building.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse, json, subprocess

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'weekly-slides/weekly-slides/LAB1_FPGA_0914'

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('names',nargs='*')
 ap.add_argument('--output',type=Path,default=ROOT/'tmp/manual-v2-review')
 args=ap.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
 names=args.names or [p['file'] for p in json.loads((BASE/'series-inventory.json').read_text(encoding='utf-8'))]+['04.LAB1_00_CONTENTS','01.vivado_2026_1_설치_매뉴얼','02.vscode_verilog_환경설정_매뉴얼']
 if len(set(names))!=len(names):raise ValueError('Duplicate PDF names')
 stale=[str(BASE/(n+ext)) for n in names for ext in ['.aux','.nav','.snm','.toc','.out','.vrb'] if (BASE/(n+ext)).exists()]
 if stale:raise RuntimeError('Move stale source-directory build auxiliaries before building: '+', '.join(stale))
 def build(name):
  for attempt in range(2):
   result=subprocess.run(['xelatex','-interaction=batchmode','-halt-on-error','-output-directory='+str(out),name+'.tex'],cwd=BASE,capture_output=True)
   if result.returncode:return {'file':name,'status':'FAIL','pass':attempt+1,'exit':result.returncode}
  log=(out/(name+'.log')).read_text(errors='replace')
  problems={k:log.count(v) for k,v in [('overfull','Overfull'),('missing_characters','Missing character')]}
  return {'file':name,'status':'PASS' if not any(problems.values()) else 'LAYOUT_REVIEW',**problems}
 results=[]
 with ThreadPoolExecutor(max_workers=2) as pool:
  for future in as_completed([pool.submit(build,n) for n in names]):
   result=future.result();results.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
   (out/'current-build-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 if any(r['status']!='PASS' for r in results):raise SystemExit(1)

if __name__=='__main__':main()
