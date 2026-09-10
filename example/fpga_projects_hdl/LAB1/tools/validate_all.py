"""Optional maintainer check; student workspaces still expose only three tasks."""
from pathlib import Path
import argparse,json,subprocess,sys,concurrent.futures

def main():
 lab=Path(__file__).resolve().parents[1]
 parser=argparse.ArgumentParser()
 parser.add_argument('--simulator',choices=['xsim','iverilog'],default='xsim')
 parser.add_argument('--edition',choices=['all','legacy','vivado_2026_1','opensource_cli'],default='all')
 parser.add_argument('--jobs',type=int,default=1)
 args=parser.parse_args()
 if args.jobs<1:parser.error('--jobs must be positive')
 def run(p):
  logfile=lab/p['path']/('build/batch-'+args.simulator+'.log');logfile.parent.mkdir(parents=True,exist_ok=True)
  with logfile.open('w',encoding='utf-8') as f:
   r=subprocess.run([sys.executable,str(lab/'tools/lab1.py'),'simulate','--project',str(lab/p['path']),'--simulator',args.simulator],stdout=f,stderr=subprocess.STDOUT)
  result={'id':p['id'],'exit':r.returncode,'log':logfile.relative_to(lab).as_posix()}
  print(p['id'],r.returncode,flush=True)
  return result
 projects=[p for p in json.loads((lab/'projects.json').read_text()) if args.edition=='all' or p['edition']==args.edition]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:results=list(pool.map(run,projects))
 output=lab/'build'/('validation-batch-'+args.simulator+'.json');output.parent.mkdir(exist_ok=True)
 output.write_text(json.dumps(results,indent=2)+'\n')
 return 0 if all(r['exit']==0 for r in results) else 1

if __name__=='__main__':sys.exit(main())
