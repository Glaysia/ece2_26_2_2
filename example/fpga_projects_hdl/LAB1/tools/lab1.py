#!/usr/bin/env python3
"""Portable LAB1 task runner. Each run owns a fresh directory and explicit result."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,datetime,uuid,re
LAB=Path(__file__).resolve().parents[1]
def tool(name):
    roots=[os.environ.get('VIVADO_BIN',''),os.environ.get('OSS_CAD_BIN','')]
    for root in filter(None,roots):
        for suffix in (['.bat','.exe',''] if os.name=='nt' else ['']):
            p=Path(root)/(name+suffix)
            if p.is_file(): return str(p)
    p=shutil.which(name)
    if p:return p
    raise RuntimeError(f'Missing {name}. Read LAB1/docs/setup.md; set VIVADO_BIN or OSS_CAD_BIN and restart VS Code.')
def execute(args,cwd,log,timeout=600,acceptable=(0,)):
    print('RUN',subprocess.list2cmdline([str(x) for x in args]),flush=True)
    with log.open('w',encoding='utf-8') as f:
        r=subprocess.run([str(x) for x in args],cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
    output=log.read_text(encoding='utf-8',errors='replace')
    print(output[-3500:],flush=True)
    if r.returncode not in acceptable: raise RuntimeError(f'Exit {r.returncode}: {log}')
    return output
def q(p):return '{'+str(p).replace('\\','/')+'}'
def source_paths(project,cfg):return [(project/s).resolve() for s in cfg['sources']]
def create_tcl(project,cfg):
    # The committed file resolves all sources relative to itself, never to the author machine.
    commands=['set project_dir [file dirname [file normalize [info script]]]',
        f'create_project {cfg["top"]} [file join $project_dir vivado] -part {cfg["part"]} -force',
        'set_property target_language Verilog [current_project]']
    for s in cfg['sources']:commands.append(f'add_files [file normalize [file join $project_dir {q(s)}]]')
    commands += [f'add_files -fileset sim_1 [file normalize [file join $project_dir {q(cfg["testbench"])}]]',
        f'add_files -fileset constrs_1 [file normalize [file join $project_dir {q(cfg["constraints"])}]]',
        f'set_property top {cfg["top"]} [get_filesets sources_1]',
        f'set_property top {cfg["simulation_top"]} [get_filesets sim_1]',
        'set_property xsim.simulate.runtime all [get_filesets sim_1]',
        'update_compile_order -fileset sources_1','update_compile_order -fileset sim_1','close_project']
    (project/'create_project.tcl').write_text('\n'.join(commands)+'\n',encoding='utf-8')
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('action',choices=['check','simulate','wave','create','vivado-sim','build','original-sim'])
    ap.add_argument('--project',default='.')
    ap.add_argument('--simulator',choices=['xsim','iverilog'],default=os.environ.get('LAB1_SIMULATOR','xsim'))
    args=ap.parse_args();project=Path(args.project).resolve()
    cfg=json.loads((project/'project.json').read_text(encoding='utf-8'))
    action=args.action
    if action=='wave':
        wave=project/'build/vscode/wave.vcd'
        if not wave.is_file():raise RuntimeError('Run 02 Simulate successfully before opening the waveform.')
        subprocess.run([tool('code'),'--reuse-window',str(wave)],check=True)
        print('If opened as text: right-click tab > Reopen Editor With... > VaporView.');return
    stage='vscode' if action=='simulate' else action
    out=project/'build'/stage;out.mkdir(parents=True,exist_ok=True)
    run=out/('run-'+uuid.uuid4().hex);run.mkdir()
    result={'project':cfg['id'],'action':action,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RUNNING','run':run.name}
    result_path=out/'result.json'
    result_path.write_text(json.dumps(result,indent=2))
    for filename in ['wave.vcd','simulation.log','design.bit']:
        (out/filename).unlink(missing_ok=True)
    try:
        if action=='check':
            versions={}
            for name,flag in [('git','--version'),('code','--version'),('vivado','-version')]:
                if name=='vivado' and args.simulator=='iverilog':continue
                versions[name]=execute([tool(name),flag],run,run/(name+'.txt'),120,acceptable=(0,1)).strip()
            if args.simulator=='iverilog':
                versions['iverilog']=execute([tool('iverilog'),'-V'],run,run/'iverilog.txt',120)
                versions['yosys']=execute([tool('yosys'),'-V'],run,run/'yosys.txt',120)
            else:
                for name in ['xvlog','xelab','xsim']:
                    versions[name]=execute([tool(name),'--version'],run,run/(name+'.txt'),120,acceptable=(0,1))
            
            for name,value in versions.items():
                if not re.search(r'\d+\.\d+',value): raise RuntimeError(f'Unrecognized version output: {name}')
            result['versions']=versions
        elif action in ['simulate','original-sim']:
            sources=source_paths(project,cfg)
            if action=='original-sim':
                sources.append((project/cfg['original_testbench']).resolve());top='testbench'
            else:
                sources.append((project/cfg['testbench']).resolve());top=cfg['simulation_top']
            if args.simulator=='iverilog':
                if action=='original-sim':raise RuntimeError('Use XSim for bounded original testbench replay.')
                execute([tool('iverilog'),'-g2012','-s',top,'-o','sim.vvp',*sources],run,run/'compile.log')
                output=execute([tool('vvp'),'sim.vvp'],run,run/'simulation.log')
            else:
                execute([tool('xvlog'),'--sv',*sources],run,run/'compile.log')
                execute([tool('xelab'),top,'--debug','typical','--snapshot','lab1_sim'],run,run/'elaborate.log')
                simargs=['--runall']
                if action=='original-sim':
                    script=run/'replay.tcl'
                    script.write_text('open_vcd wave.vcd\nlog_vcd /testbench/*\nrun 2000 ns\nclose_vcd\nquit\n')
                    simargs=['--tclbatch',str(script)]
                output=execute([tool('xsim'),'lab1_sim',*simargs],run,run/'simulation.log')
            shutil.copy2(run/'simulation.log',out/'simulation.log')
            if action=='simulate':
                marker=f'LAB1_PASS {cfg["top"]} cases={cfg["cases"]}'
                if marker not in output or re.search(r'\b(Fatal|FATAL|FAIL)\b',output):
                    raise RuntimeError('Required self-check PASS missing. Inspect simulation.log.')
            wave=run/'wave.vcd'
            if not wave.is_file() or wave.stat().st_size==0:raise RuntimeError('No fresh VCD')
            shutil.copy2(wave,out/'wave.vcd')
            result.update(simulator=args.simulator,cases=cfg['cases'] if action=='simulate' else None)
        elif action in ['create','vivado-sim','build']:
            create_tcl(project,cfg)
            xpr=project/'vivado'/(cfg['top']+'.xpr')
            if action=='create' or not xpr.is_file():
                execute([tool('vivado'),'-mode','batch','-notrace','-source',project/'create_project.tcl'],run,run/'create.log',1200)
            if action!='create':
                commands=[f'open_project {q(xpr)}']
                if action=='vivado-sim':
                    commands+=['launch_simulation','close_sim','close_project']
                else:
                    commands += ['reset_run synth_1','launch_runs impl_1 -to_step write_bitstream -jobs 4','wait_on_run impl_1',
                        'if {[get_property PROGRESS [get_runs impl_1]] ne "100%"} {error "Implementation did not complete"}',
                        'open_run impl_1','report_timing_summary -file timing_summary.txt','report_drc -file drc.txt','close_project']
                script=run/'task.tcl';script.write_text('\n'.join(commands)+'\n')
                output=execute([tool('vivado'),'-mode','batch','-notrace','-source',script],run,run/'vivado.log',3600)
                if action=='vivado-sim':
                    logs=list((project/'vivado').glob('*.sim/sim_1/behav/xsim/simulate.log'))
                    marker=f'LAB1_PASS {cfg["top"]} cases={cfg["cases"]}'
                    if not logs or marker not in logs[0].read_text(errors='replace'):raise RuntimeError('Vivado simulation PASS missing')
                    shutil.copy2(logs[0],out/'simulation.log')
                    wave=logs[0].parent/'wave.vcd'
                    if wave.exists():shutil.copy2(wave,out/'wave.vcd')
                else:
                    bit=project/'vivado'/(cfg['top']+'.runs')/'impl_1'/(cfg['top']+'.bit')
                    if not bit.is_file():raise RuntimeError('No bitstream')
                    shutil.copy2(bit,out/'design.bit')
            result['vivado_version']=execute([tool('vivado'),'-version'],run,run/'version.log',120,acceptable=(0,1)).splitlines()[0]
        result['status']='PASS'
    except Exception as e:
        result.update(status='FAIL',error=str(e));raise
    finally:
        result['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        result_path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
    try:main()
    except Exception as exc:print('ERROR:',exc,file=sys.stderr);sys.exit(1)
