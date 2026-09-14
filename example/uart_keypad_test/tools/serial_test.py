"""Physical USB-UART test and keypad monitor (9600 8N1)."""
from pathlib import Path
import argparse,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'build/python'))
import serial

parser=argparse.ArgumentParser()
parser.add_argument('--port',default='COM4')
parser.add_argument('--monitor',type=float,default=0)
args=parser.parse_args()
records=[]
with serial.Serial(args.port,9600,timeout=.15,write_timeout=2) as port:
    time.sleep(.2);port.reset_input_buffer()
    if args.monitor:
        print(f'KEYPAD_MONITOR_READY {args.port} 9600 8N1 for {args.monitor:g}s',flush=True)
        deadline=time.monotonic()+args.monitor
        while time.monotonic()<deadline:
            data=port.readline()
            if data:
                record={'time':time.time(),'rx_hex':data.hex(),'text':data.decode('ascii','backslashreplace')}
                records.append(record);print(json.dumps(record),flush=True)
    else:
        cases=[(b'BLABLA\n',b'LB|BLABLA\n'),(b'\n',b'LB|\n'),
               (b'hello 123\r\n',b'LB|hello 123\n'),
               (b'A\nB\n',b'LB|A\nLB|B\n'),
               (b'x'*128+b'\n',b'LB|'+b'x'*128+b'\n'),
               (b'y'*129+b'\n',b'ERR|LINE_TOO_LONG\n'),(b'OK\n',b'LB|OK\n')]
        for sent,expected in cases:
            port.write(sent);port.flush();got=b'';deadline=time.monotonic()+3
            while len(got)<len(expected) and time.monotonic()<deadline:got+=port.read(len(expected)-len(got))
            record={'tx_hex':sent.hex(),'expected_hex':expected.hex(),'rx_hex':got.hex(),'pass':got==expected}
            records.append(record);print(json.dumps(record),flush=True)
            if got!=expected:break
out=ROOT/'evidence'/('keypad-monitor.json' if args.monitor else 'serial-loopback.json')
out.write_text(json.dumps(records,indent=2)+'\n')
if not args.monitor and (len(records)!=7 or not all(r['pass'] for r in records)):sys.exit(1)
