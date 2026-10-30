#!/usr/bin/env python3
"""Build the configured Spartan-7 design using Yosys and openXC7 only."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,uuid

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project',default='.')
    ap.add_argument('--chipdb',default=os.environ.get('OPENXC7_CHIPDB',str(Path.home()/'fpga-cli/xc7s75fgga484-1.bin')))
    ap.add_argument('--db-root',default=os.environ.get('XRAY_DB_ROOT',str(Path.home()/'fpga-cli/prjxray-db/spartan7')))
    args=ap.parse_args();project=Path(args.project).resolve()
    cfg=json.loads((project/'project.json').read_text())
    if cfg['part']!='xc7s75fgga484-1':raise ValueError('This flow is validated only against the configured S75 part.')
    out=project/'build/cli';out.mkdir(parents=True,exist_ok=True)
    run=out/('run-'+uuid.uuid4().hex);run.mkdir()
    published=out/(cfg['top']+'.bit');published.unlink(missing_ok=True)
    result={'project':cfg['id'],'part':cfg['part'],'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run':run.name,'status':'RUNNING','steps':[]}
    def save():
        (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    def tool(name):
        root=Path(os.environ.get('OSS_CAD_ROOT' if name=='yosys' else 'OPENXC7_ROOT',str(Path.home()/'.apio/packages'/('oss-cad-suite' if name=='yosys' else 'openxc7'))))
        candidate=root/'bin'/name
        found=str(candidate) if candidate.is_file() else shutil.which(name)
        if not found:raise RuntimeError('Missing '+name)
        return found
    def execute(name,argv):
        step={'name':name,'command':[str(x) for x in argv],'status':'RUNNING'};result['steps'].append(step);save()
        print(name,flush=True)
        with (run/(name+'.log')).open('w') as log:
            completed=subprocess.run(step['command'],cwd=run,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
        step.update(returncode=completed.returncode,status='PASS' if completed.returncode==0 else 'FAIL');save()
        if completed.returncode:raise RuntimeError(name+' failed: '+str(run/(name+'.log')))
    save()
    try:
        sources=[(project/s).resolve() for s in cfg['sources']]
        result['input_sha256']={s:hashlib.sha256((project/s).read_bytes()).hexdigest() for s in [*cfg['sources'],cfg['constraints']]}
        script=run/'synth.ys'
        script.write_text('read_verilog '+ ' '.join(json.dumps(str(s)) for s in sources)+'\n'+f"synth_xilinx -family xc7 -top {cfg['top']}\n"+'write_json design.json\nstat\n')
        execute('synthesis',[tool('yosys'),'-s',script])
        chipdb=Path(args.chipdb).expanduser().resolve();db=Path(args.db_root).expanduser().resolve()
        if not chipdb.is_file():raise RuntimeError('Exact S75 chipdb missing: '+str(chipdb))
        result['chipdb_sha256']=hashlib.sha256(chipdb.read_bytes()).hexdigest()
        execute('place-route',[tool('nextpnr-xilinx'),'--chipdb',chipdb,'--xdc',(project/cfg['constraints']).resolve(),'--json','design.json','--write','routed.json','--fasm','design.fasm','--report','route-report.json',*(['--freq','0.001'] if cfg['top']=='lab1_integrated' else [])])
        execute('frames',[tool('fasm2frames'),'--db-root',db,'--part',cfg['part'],'design.fasm','design.frames'])
        execute('bitstream',[tool('xc7frames2bit'),'--part_file',db/cfg['part']/'part.yaml','--part_name',cfg['part'],'--frm_file','design.frames','--output_file','design.bit'])
        bit=run/'design.bit'
        if not bit.is_file() or bit.stat().st_size==0:raise RuntimeError('No fresh bitstream')
        shutil.copy2(bit,published)
        result.update(status='PASS',bitstream=published.name,bitstream_size=published.stat().st_size,bitstream_sha256=hashlib.sha256(published.read_bytes()).hexdigest())
    except Exception as exc:
        result.update(status='FAIL',error=str(exc));raise
    finally:
        result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()

if __name__=='__main__':
    try:main()
    except Exception as exc:print(str(exc),file=sys.stderr);sys.exit(1)
