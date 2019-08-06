with open('/proc/meminfo') as fd:
    for line in fd:
        if line.startswith('MemTotal'):
            total = line.split()[1]
            continue
        if line.startswith('MemFree'):
            free = line.split()[1]
            break
FreeMem = int(free)/(1024.0*1024)
TotalMem = int(total)/(1024.0*1024)
print "FreeMem:"+"%.2f" % FreeMem+'G'
print "TotalMem:"+"%.2f" % TotalMem+'G'
print "FreeMem/TotalMem:"+"%.2f" % ((FreeMem/TotalMem)*100)+'%'