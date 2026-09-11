"""Plot measured VCD values for the wiki; these are data plots, not UI screenshots."""
from pathlib import Path
import json,re,bisect,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

LAB=Path(__file__).resolve().parents[1]
WINDOWS={1:(0,40),2:(0,80),3:(280,350),4:(140,210),5:(140,200),6:(320,360),7:(70,160),8:(0,50),9:(0,80),10:(60,110)}

def read_vcd(path,top,signals):
 text=path.read_text(encoding='utf-8');scale=re.search(r'\$timescale\s+(\d+)\s*(fs|ps|ns|us|ms|s)',text)
 factor=int(scale[1])*{'fs':1e-6,'ps':1e-3,'ns':1,'us':1e3,'ms':1e6,'s':1e9}[scale[2]]
 scope=[];ids={};history={};time=0
 for line in text.splitlines():
  line=line.strip();parts=line.split()
  if line.startswith('$scope'):scope.append(parts[2])
  elif line.startswith('$upscope'):scope.pop()
  elif line.startswith('$var'):
   name='.'.join(scope+[''.join(parts[4:-1])]);ids[name]=(parts[3],int(parts[2]));history.setdefault(parts[3],[])
  elif line.startswith('#'):time=int(line[1:])*factor
  elif len(line)>1 and line[0] in '01xXzZ':history.setdefault(line[1:],[]).append((time,line[0]))
  elif line[:1] in ['b','B']:
   value,code=line[1:].split();history.setdefault(code,[]).append((time,value))
 return {s:(ids[top+'.'+s][1],history[ids[top+'.'+s][0]]) for s in signals}

def main():
 ps=json.loads((LAB/'projects.json').read_text(encoding='utf-8'));cs=json.loads((LAB/'docs/circuits.json').read_text(encoding='utf-8'))
 plt.rcParams.update({'svg.fonttype':'path','font.size':11})
 for p in ps:
  if p['top']=='lab1_integrated':continue
  c=next(c for c in cs if p['path'].endswith(c['slug']));folder=LAB/p['path'];vcd=folder/'build/vscode/wave.vcd'
  if not vcd.exists():continue
  a,b=WINDOWS[c['n']];signals=read_vcd(vcd,p['simulation_top'],c['signals'])
  fig,ax=plt.subplots(figsize=(11,0.7*len(signals)+1.3));fig.set_facecolor('white')
  for row,(name,(width,events)) in enumerate(signals.items()):
   y=len(signals)-row-1;times=[e[0] for e in events]
   def value(t):
    idx=bisect.bisect_right(times,t)-1
    return events[idx][1] if idx>=0 else 'x'
   boundaries=sorted(set([a,b]+[t for t,_ in events if a<t<b]))
   if width==1:
    xx=boundaries;yy=[y+.6*(1 if value(t)=='1' else 0) for t in xx]
    ax.step(xx,yy,where='post',color='#005eb8',lw=1.8)
   else:
    for left,right in zip(boundaries,boundaries[1:]):
     val=value((left+right)/2);label=hex(int(val,2))[2:].upper().zfill((width+3)//4) if set(val)<=set('01') else val
     dx=min(.6,(right-left)*.08)
     ax.plot([left,left+dx,right-dx,right],[y+.3,y+.58,y+.58,y+.3],color='#168777',lw=1.4)
     ax.plot([left,left+dx,right-dx,right],[y+.3,y+.02,y+.02,y+.3],color='#168777',lw=1.4)
     ax.text((left+right)/2,y+.3,label,ha='center',va='center',fontsize=10)
  ax.set_yticks([len(signals)-i-1+.3 for i in range(len(signals))],list(signals))
  ax.set_xlim(a,b);ax.set_ylim(-.3,len(signals));ax.set_xticks(list(range(a,b+1,10)));ax.set_xlabel('Time (ns) · bus labels in hex')
  ax.grid(axis='x',alpha=.2);ax.tick_params(axis='y',length=0)
  for edge in ['top','right','left']:ax.spines[edge].set_visible(False)
  ax.set_title(p['top']+' · measured XSim VCD',loc='left',color='#005eb8',pad=12)
  fig.tight_layout();out=folder/'evidence';out.mkdir(exist_ok=True)
  fig.savefig(out/'waveform.svg');fig.savefig(folder/'build/waveform-preview.png',dpi=120);plt.close(fig)
  (out/'waveform-source.vcd').write_bytes(vcd.read_bytes())
  (out/'waveform-plot.json').write_text(json.dumps({'project':p['id'],'source':'waveform-source.vcd','source_sha256':hashlib.sha256(vcd.read_bytes()).hexdigest(),'interval_ns':[a,b],'signals':list(signals),'kind':'plot of measured VCD, not a VS Code screenshot'},indent=2)+'\n')
  print(p['id'],flush=True)

if __name__=='__main__':main()
