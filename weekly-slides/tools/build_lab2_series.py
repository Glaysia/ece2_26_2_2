"""Build existing LAB2 TeX sources into a separate directory, twice each."""
from pathlib import Path
import argparse
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'weekly-slides/weekly-slides/LAB2_FPGA_0921'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('names',nargs='*')
    parser.add_argument('--output',type=Path,default=ROOT/'tmp/lab2-build')
    args=parser.parse_args()
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    names=args.names or [p.stem for p in sorted(BASE.glob('*.tex'))]
    results=[]
    for name in names:
        if Path(name).name!=name or not (BASE/(name+'.tex')).is_file():
            raise ValueError('Expected an existing local TeX stem: '+name)
        for extension in ['.aux','.nav','.snm','.toc','.out','.vrb']:
            if (BASE/(name+extension)).exists():
                raise RuntimeError('Move stale source-folder auxiliary first: '+name+extension)
        for attempt in range(2):
            run=subprocess.run(['xelatex','-interaction=batchmode','-halt-on-error',
                                '-output-directory='+str(out),name+'.tex'],cwd=BASE,capture_output=True,timeout=180)
            if run.returncode:
                raise RuntimeError(f'{name}: TeX pass {attempt+1} failed; inspect {out/(name+".log")}')
        log=(out/(name+'.log')).read_text(encoding='utf-8',errors='replace')
        problems={key:log.count(pattern) for key,pattern in [('overfull','Overfull'),('missing_characters','Missing character')]}
        results.append({'file':name,**problems})
        if any(problems.values()): raise RuntimeError(f'{name}: {problems}')
        print(name,'built; visual review required',flush=True)
    (out/'build-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
