"""Validate the nine modern LAB2 designs in Vivado batch mode (no GUI actions)."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'example/fpga_projects_hdl/LAB2'

def tclpath(path):
    value=path.resolve().as_posix()
    if any(c in value for c in '{}\n'): raise ValueError('Unsupported Tcl path')
    return '{'+value+'}'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('names',nargs='*')
    args=parser.parse_args()
    projects=sorted((LAB/'vivado_2026_1').glob('*/board.json'))
    if args.names: projects=[p for p in projects if p.parent.name in args.names]
    if not projects: raise RuntimeError('No matching projects')
    out=ROOT/'tmp/lab2-vivado'; out.mkdir(exist_ok=True)
    summary=LAB/'docs/vivado-batch-validation.json'
    records=json.loads(summary.read_text(encoding='utf-8')) if summary.exists() else []
    for boardfile in projects:
        project=boardfile.parent
        board=json.loads(boardfile.read_text(encoding='utf-8'))
        config=json.loads((project/'simulation.json').read_text(encoding='utf-8'))
        sources=[project/p for p in config['sources']]
        source_hashes={p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [*sources,project/board['constraints']]}
        run=out/(project.name+'-'+str(time.time_ns())); run.mkdir()
        lines=['set_param general.maxThreads 2','create_project -in_memory -part '+board['part']]
        lines+=['read_verilog '+tclpath(p) for p in sources]
        lines+=['read_xdc '+tclpath(project/board['constraints']),
                'synth_design -top '+board['top']+' -part '+board['part'],
                'opt_design','place_design','route_design',
                'report_utilization -file '+tclpath(run/'utilization.txt'),
                'report_timing_summary -file '+tclpath(run/'timing.txt'),
                'report_drc -file '+tclpath(run/'drc.txt'),
                'report_cdc -file '+tclpath(run/'cdc.txt'),
                'write_bitstream -force '+tclpath(run/(board['top']+'.bit')),
                'puts "LAB2_VIVADO_PASS '+board['top']+'"','close_project','exit']
        script=run/'implement.tcl'; script.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        started=time.time()
        with (run/'console.log').open('w',encoding='utf-8') as log:
            result=subprocess.run(['C:/AMDDesignTools/2026.1/Vivado/bin/vivado.bat','-mode','batch',
                                   '-source',str(script),'-nojournal','-log',str(run/'vivado.log')],cwd=run,
                                  stdout=log,stderr=subprocess.STDOUT,timeout=900)
        output=(run/'console.log').read_text(encoding='utf-8',errors='replace')
        bit=run/(board['top']+'.bit')
        record={'project':project.relative_to(LAB).as_posix(),'top':board['top'],'part':board['part'],
                'execution':'Vivado 2026.1 batch, no GUI','exit_code':result.returncode,
                'seconds':round(time.time()-started,2),'run_directory':run.relative_to(ROOT).as_posix(),
                'inputs_sha256':source_hashes}
        unchanged=all(hashlib.sha256((project/name).read_bytes()).hexdigest()==value for name,value in source_hashes.items())
        passed=result.returncode==0 and ('LAB2_VIVADO_PASS '+board['top']) in output and bit.is_file() and unchanged
        record['status']='PASS' if passed else 'FAIL'
        if passed:
            record['bitstream']={'file':bit.name,'bytes':bit.stat().st_size,'sha256':hashlib.sha256(bit.read_bytes()).hexdigest()}
            evidence=project/'evidence/vivado-batch'; evidence.mkdir(parents=True,exist_ok=True)
            for name in ['utilization.txt','timing.txt','drc.txt','cdc.txt']:
                (evidence/name).write_bytes((run/name).read_bytes())
            (evidence/'validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        records=[r for r in records if r['project']!=record['project']]+[record]
        records.sort(key=lambda r:r['project'])
        summary.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(project.name,record['status'],record['seconds'],'seconds',flush=True)
        if not passed: raise RuntimeError('Vivado failed; inspect '+str(run/'console.log'))

if __name__=='__main__': main()
