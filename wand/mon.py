import time

def read(filename):
    with open(filename, 'r') as fd:
        return fd.readline().rstrip()

c0 = []
c1 = []
with open('/tmp/capacity.txt','w') as fo:
    fo.write("time,c0,c1,v0,v1,i0,i1\n")

while True:
    try:
        with open('/tmp/capacity.txt','a') as fo:
            c0 = read('/sys/class/power_supply/BAT0/capacity')
            c1 = read('/sys/class/power_supply/BAT1/capacity')
            v0 = read('/sys/class/power_supply/BAT0/voltage_now')
            v1 = read('/sys/class/power_supply/BAT1/voltage_now')
            i0 = read('/sys/class/power_supply/BAT0/current_now')
            i1 = read('/sys/class/power_supply/BAT1/current_now')
            fo.write("{},{},{},{},{},{},{}\n".format(time.time(),c0,c1,v0,v1,i0,i1))
    except:
        continue
        
    time.sleep(1)
