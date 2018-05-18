# CPU SKU Selection

Raw data from geekbench.com, spec.org, and ark.intel.com

Please unzip geek_data.tar.gz before use:

tar xzf geek_data.tar.gz

## Data format

### Geekbench
['model number', 'freq', 'L2', 'L3', 'memory', 'bench', 'single/multicore', 'score', 'perf']

### SPEC Perf
['bench', 'run time', 'score', 'model number', 'freq', 'memory type', 'memory size']

### Intel chips
 ['uarch','chip type','launch date','processor number','cache','bus speed','instruction set extensions','instruction     set',
     'max memory size','memory types','# of memory channels','max memory bandwidth','ecc memory supported',
      'processor graphics','graphics base frequency','graphics max dynamic frequency','graphics video max memory','# of d    isplays supported','graphics and imc lithography',
      'pci express revision','pci express lanes', 'lithography',
      '# of cores','# of threads','base frequency','turbo frequency','tdp-up frequency','tdp-up','tdp-down frequency','t    dp-down','tdp',
      'turbo boost technology','vpro','hyper-threading','(vt-x)','(vt-d)','tsx-ni','idle states','speedstep','thermal mo    nitoring','identity protection',
      'aes new instructions','secure key',
      'trusted execution','execute disable bit','anti-theft', 'price']
