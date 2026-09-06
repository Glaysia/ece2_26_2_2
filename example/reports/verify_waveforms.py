"""Check observed VCD behavior against independent arithmetic/state expectations."""
from pathlib import Path
import bisect
import json

ROOT = Path(__file__).resolve().parent

def read_vcd(path):
    scopes, names, values = [], {}, {}
    now = 0
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith('$scope'):
            scopes.append(line.split()[2])
        elif line.startswith('$upscope'):
            scopes.pop()
        elif line.startswith('$var'):
            p = line.split()
            names['.'.join(scopes + [p[4]])] = p[3]
        elif line.startswith('#'):
            now = int(line[1:])
        elif line and line[0] in '01xzXZbB' and not line.startswith('$'):
            if line[0] in 'bB':
                bits, code = line[1:].split()
            else:
                bits, code = line[0], line[1:]
            value = None if any(c in bits.lower() for c in 'xz') else int(bits, 2)
            values.setdefault(code, []).append((now, value))
    return {name: values[code] for name, code in names.items()}, now

TIME_CACHE = {}

def at(events, t):
    key = id(events)
    if key not in TIME_CACHE:
        TIME_CACHE[key] = [e[0] for e in events]
    i = bisect.bisect_right(TIME_CACHE[key], t) - 1
    return events[i][1] if i >= 0 else None

def verify(n):
    TIME_CACHE.clear()
    raw, end = read_vcd(ROOT / 'simulation' / f'exp{n}' / 'top_main.vcd')
    s = {k.removeprefix('tb_top_main.'): v for k, v in raw.items() if k.count('.') == 1}
    rises = [t for t,v in s['clk'] if v == 1 and t > 20000]
    assert end == 101020000
    assert all(b-a == 10000 for a,b in zip(rises, rises[1:]))
    assert at(s['rst'], 0) == 1 and at(s['rst'], 20000) == 0
    result = {'experiment': n, 'end_ns': end/1000, 'clock_ns': 10, 'active_edges': len(rises)}
    if n == 16:
        q = 0
        for t in rises:
            q = (q + (1 if at(s['up'],t) else -1)) % 16
            assert at(s['q'],t) == q, (n,t,q)
        result.update(checked='all counter rising edges, increment/decrement and wrap', final_q=q)
    elif n == 17:
        for i,t in enumerate(rises,1):
            for name,half in [('o_50',1),('o_10',5),('o_2',25)]:
                assert at(s[name],t) == (i//half)%2, (n,t,name)
            assert at(s['o_100'],t) == 1
        result.update(periods_ns={'o_100':10,'o_50':20,'o_10':100,'o_2':500})
    elif n == 18:
        for i,t in enumerate(rises,1):
            assert at(s['phase'],t) == [3,6,12,9][i%4]
        result.update(sequence_hex=['3','6','c','9'], cycle_ns=40)
    elif n in (19,20):
        count, sound = 0, 0
        for t in rises:
            key = at(s['key'],t)
            half = 1701 if n == 19 else {128:1908,64:1701}.get(key,0)
            if half == 0:
                count, sound = 0,0
            elif count >= half-1:
                count, sound = 0,1-sound
            else:
                count += 1
            assert at(s['sound'],t) == sound, (n,t)
        result.update(sound_transitions_ns=[(t/1000,v) for t,v in s['sound']])
        if n == 19:
            result['nominal_hz'] = 1000000/(2*1701)
        else:
            result['nominal_hz_by_key'] = {'80':1000000/(2*1908), '40':1000000/(2*1701)}
    elif n == 21:
        segs=[0xfc,0x60,0xda,0xf2,0x66,0xb6,0xbe,0xe0,0xfe,0xf6]
        for i,t in enumerate(rises,1):
            seconds=(i//1000)%3600
            digits=[seconds//600,(seconds//60)%10,(seconds//10)%6,seconds%10]
            for name,v in zip(['min_tens','min_ones','sec_tens','sec_ones'],digits):
                assert at(s[name],t)==v,(n,t,name)
            scan=i%4
            assert at(s['seg_com'],t)==[0xf7,0xfb,0xfd,0xfe][scan]
            assert at(s['seg_data'],t)==segs[digits[scan]]
        result.update(final_display='00:10', simulated_second_ns=10000, unchecked='minute carry and 59:59 wrap; hardware')
    result['status']='PASS'
    return result

if __name__ == '__main__':
    results=[verify(n) for n in range(16,22)]
    out=ROOT/'simulation'/'verification.json'
    out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
