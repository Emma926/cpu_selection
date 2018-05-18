import numpy as np
import os
import itertools
import scipy.stats

def standardize_data(samples):
  n_benchmarks,n_counters = samples.shape
  counter_means = np.mean(samples,axis=0).reshape(1,n_counters)
  counter_stddevs = np.std(samples,axis=0).reshape(1,n_counters)
  print counter_means, counter_stddevs
  return (np.array(samples)-counter_means)/counter_stddevs

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def get_alpha(s):
    res = ''
    for i in s:
        if i.isalpha():
            res = res + i
        else:
            return res
    return res


benches_c=[u'400', u'401', u'403', u'410', u'416', u'429', u'433', u'434', u'435', u'436', u'437', u'444', u'445', u'450', u'453', u'454', u'456', u'458', u'459', u'462', u'464', u'465', u'470', u'471', u'473', u'481', u'482', u'483']
path = ["spec", "spec_fp"]
DDR4 = ['DDR4', 'PC4']
DDR3 = ['DDR3', 'PC3', 'CM3','TWIN3','M3']
DDR2 = ['DDR2', 'PC2','CL5','PC-5300','DRR2']

data = []
all_cpu = []
aggr_data = {}
for pa in path:
    dirs = os.listdir(os.path.join(pa,"www.spec.org/cpu2006/results"))
    for dir in dirs:
        if not os.path.isdir(os.path.join(pa, "www.spec.org/cpu2006/results", dir)):
            continue
        cwd = os.path.join(pa, "www.spec.org/cpu2006/results", dir)
        files = os.listdir(cwd)
        for f in files:
            fopen = open(os.path.join(cwd,f),'r')
            intel_chip = 0
            start = 0
            have_started = 0
            CPU_start = 0
            ag_flag = 0
            for line in fopen:
                if line[0] == ' ' and 'Intel' in line:
                    intel_chip = 1
                if line[0] <> ' ' and intel_chip == 0:
                    break
                if CPU_start == 1 and "CPU Name" in line:
                    s = line.split(':')[-1].strip('\n').strip(' ').strip('\t')
                    all_cpu.append(s)
                    data[-1].append(s)        
            
                    if not s in aggr_data:
                        aggr_data[s] = []
                    aggr_data[s].append(tmp_perf)
                    
                    if len(s.split('-')) > 1 and "-" in s:
                        s = s.split('-')[0]
                    elif len(s.split(' ')) > 2 and s.split(' ')[2][0].isalpha():
                        s = s.split(' ')[0] + ' ' + s.split(' ')[1] + ' ' + get_alpha(s.split(' ')[2])
                    elif len(s.split(' ')) > 2:
                        s = s.split(' ')[0] + ' ' + s.split(' ')[1]+ ' ' + s.split(' ')[2][0]  
                if CPU_start == 1  and "CPU MHz" in line:
                    data[-1].append(float(line.split(':')[-1].strip('\n').strip(' ')))
                if CPU_start == 1 and "Memory:" in line:
                    
                    s = line.split(':')[-1].strip('\n')
                    
                    t = ''
                    flag = False
                    for i in DDR4:
                        if i in s:
                            flag = True
                            t = 'DDR4'
                            break
                    if flag ==  False:
                        for i in DDR3:
                            if i in s:
                                flag = True
                                t = 'DDR3'
                                break
                    
                    if flag ==  False:
                        for i in DDR2:
                            if i in s:
                                t = 'DDR2'
                                flag = True
                                break
                    if flag == False:
                        t = 'DDR'
                    data[-1].append(t)
                    
                    if 'e3-1260l' in data[-1][-3].lower() and t == 'DDR':
                        print f
                    
                    if s == '':
                        data[-1].append(0)
                    else:
                        sz = float(s.strip(' ').split(' ')[0])
                        unit = s.strip(' ').split(' ')[1]

                        if 'TB' in unit:
                            sz = sz * 1000
                        elif not "GB" in unit:
                            print unit
                        if sz == '':
                            print line
                        data[-1].append(sz)
                
                if "SOFTWARE" in line and CPU_start == 1:
                    CPU_start = 0
                        
                if "HARDWARE" in line and have_started == 1:
                    CPU_start = 1
                if start == 1 and len(" ".join(line.split()).split(" ")) < 4:
                    s = " ".join(line.split()).split(" ")
                    if "SPEC" in s[0] and "2006" in s[0] and isfloat(s[-1]):
                        tmp_perf = float(s[-1])
                        ag_flag = 1
                    start = 0
                if start == 1:
                    
                    s = " ".join(line.split()).split(" ")
                    data.append([])
                    data[-1].append(s[0])
                    data[-1].append(s[2])
                    data[-1].append(s[3])
                        
                    have_started = 1
                #if CPU_start == 1 and len(data[-1]) > 6:
                #    print f
                if "====" in line and start == 0:
                    start = 1     

cpu = ''
hz = ''
ddr = ''
sz = ''
for d in reversed(data):
    if len(d) == 7:
        cpu = d[3]
        hz = d[4]
        ddr = d[5]
        sz = d[6]
    else:
        d.append(cpu)
        d.append(hz)
        d.append(ddr)
        d.append(sz)

for d in range(len(data)-1,-1,-1):
    if not "intel" in data[d][3].lower() or not data[d][0].split('.')[0] in benches_c:
        del data[d]
print len(data)

import json
with open('spec_speed.json', 'w') as outfile:
    json.dump(data, outfile)
print("spec_speed dumped")
