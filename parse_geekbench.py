import numpy as np
import os
import itertools

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

check_units= ['',
 u'GHz',
 u'KB',
 u'KB',
 u'MB',
 u'GB/sec',
 u'GB/sec',
 u'MB/sec',
 u'GB/sec',
 u'MB/sec',
 u'GB/sec',
 u'MB/sec',
 u'MB/sec',
 u'MB/sec',
 u'MB/sec',
 u'MB/sec',
 u'MB/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'MB/sec',
 u'MB/sec',
 u'Mpairs/sec',
 u'Mpairs/sec',
 u'Mnodes/sec',
 u'Mnodes/sec',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Gflops',
 u'Mpairs/sec',
 u'Mpairs/sec',
 u'Mpixels/sec',
 u'Mpixels/sec',
 u'GB/sec',
 u'GB/sec',
 u'GB/sec',
 u'GB/sec',
 u'GB/sec',
 u'GB/sec',
 u'GB/sec',
 u'GB/sec']

geek_data = [] # model #, freq, L2, L3, memory, bench, single/multicore, score, perf

path = 'geekbench/geekbench/browser.primatelabs.com/geekbench3'
files = os.listdir(path)
for file in files:
    units = []
    for i in range(5):
        units.append(0)
    
    data = []
    if not isfloat(file.split('.')[0]):
        continue
    soup = BeautifulSoup(open(os.path.join(path, file)))
    tables = soup.find_all('table', attrs={'class':'table table-striped geekbench2-show system-information'})
    table_body = tables[1].find('tbody')
    rows = table_body.find_all('tr')
    data_t = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 0:
            cols = row.find_all('th')
        cols = [ele.text.strip() for ele in cols]
        data_t.append([ele.replace('\n',' ').replace('  ',' ') for ele in cols if ele]) 
    #print arch
    data.append(data_t)
    
    tables = soup.find_all('table', attrs={'class':'table table-striped geekbench2-show section-performance'})
    for table in tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        data_t = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 0:
                cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            data_t.append([ele.replace('\n',' ').replace('  ',' ') for ele in cols if ele]) 
        #print arch
        data.append(data_t)
    head = []
    head.append(0)
    head.append(0)
    head.append(0)
    head.append(0)
    head.append(0)

    for d in data[0]:
        if d[0] == 'Processor':
            head[0] = d[1].split('@')[0].strip(' ')
            head[1] = float(d[1].split('@')[1].strip(' ').split(' ')[0])
            
            units[0] = ''
            units[1] = d[1].split('@')[1].strip(' ').split(' ')[1]
            if 'M' in units[1]:
                head[1] = 0.001* float(d[1].split('@')[1].strip(' ').split(' ')[0])
                units[1] = d[1].split('@')[1].strip(' ').split(' ')[1].replace('M','G')

            
        elif d[0] == 'L2 Cache':
            head[2] = d[1]
            units[2] = d[1].split(' ')[1]
        elif d[0] == 'L3 Cache':
            if 'KB' in d[1]:
                head[3] = float(d[1].split(' ')[0])
                units[3] = d[1].split(' ')[1]

        elif d[0] == 'Memory':
            if 'MB' in d[1]:
                head[4] = float(d[1].split(' ')[0])
                units[4] = d[1].split(' ')[1]

  
    for i in range(1, len(data)):
        data_current = data[i]
        for d in data_current:
            data_t = []
            for t in head:
                data_t.append(t)

            if len(d[0].split(' ')) == 3:
                data_t.append(d[0].split(' ')[0] + ' ' + d[0].split(' ')[1])
            elif len(d[0].split(' ')) == 2:
                data_t.append(d[0].split(' ')[0])
            else:
                print d
            
            if 'Single' in d[0].split(' ')[-1]:
                data_t.append(0)
            elif 'Mult' in d[0].split(' ')[-1]:
                data_t.append(1)
                
            data_t.append(d[1].split(' ')[0])
            
            units.append(d[1].split(' ')[-1])
            if 'G' in check_units[len(units)-1] and 'M' in units[-1]:
                data_t.append(0.001*float(d[1].split(' ')[1]))
                units[-1] = d[1].split(' ')[-1].replace('M','G')
            elif 'M' in check_units[len(units)-1] and 'G' in units[-1]:
                data_t.append(1000*float(d[1].split(' ')[1]))
                units[-1] = d[1].split(' ')[-1].replace('G','M')
            elif 'M' in check_units[len(units)-1] and 'K' in units[-1]:
                data_t.append(0.001*float(d[1].split(' ')[1]))
                units[-1] = d[1].split(' ')[-1].replace('K','M')
            elif 'G' in check_units[len(units)-1] and 'K' in units[-1]:
                data_t.append(0.000001*float(d[1].split(' ')[1]))
                units[-1] = d[1].split(' ')[-1].replace('K','G')
            elif 'G' in check_units[len(units)-1] and 'T' in units[-1]:
                data_t.append(1000*float(d[1].split(' ')[1]))
                units[-1] = d[1].split(' ')[-1].replace('T','G')
            else:
                data_t.append(d[1].split(' ')[1])
                units[-1] = d[1].split(' ')[-1]
            geek_data.append(data_t)
            
    # check units
    for i in range(len(check_units)):
        if check_units[i] <> units[i]:
            print file, i, check_units[i], units[i]

import json
with open('geek_data.json','w') as outfile:
    json.dump(geek_data, outfile)

