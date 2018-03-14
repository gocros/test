#!/usr/bin/python
import time

def read(filename):
    with open(filename, 'r') as fd:
        s = fd.readline().rstrip()
        return int(s) if s.isdigit() else s

with open('/tmp/mon.csv','w') as fo:
    fo.write("time,c0,c1,v0,v1,i0,i1\n")

    while True:
        s0 = read('/sys/class/power_supply/BAT0/status')
        c0 = read('/sys/class/power_supply/BAT0/capacity')
        v0 = read('/sys/class/power_supply/BAT0/voltage_now')
        i0 = read('/sys/class/power_supply/BAT0/current_now')
        
        i0 = -i0 if s0=='Charging' else i0   
        
        try:
            v1 = read('/sys/class/power_supply/BAT1/voltage_now')        
            s1 = read('/sys/class/power_supply/BAT1/status')
            i1 = read('/sys/class/power_supply/BAT1/current_now')
            c1 = read('/sys/class/power_supply/BAT1/capacity')
            i1 = -i1 if s1=='Charging' else i1
        except:
            v1 = 0
            s1 = -9999
            i1 = 0
            c1 = -9999

        rec = "{},{},{},{},{},{},{}\n".format(time.time(),c0,c1,v0,v1,i0,i1)
        print rec
        fo.write(rec)
        fo.flush()
        time.sleep(1)
