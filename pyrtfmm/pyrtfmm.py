import re
from rich import print,box
from rich.markdown import Markdown
from rich.table import Table

desp = """
# Usage
+ The parameters shoule look like :  
```
input parameters=[
  override             = 0
  P                    = 16
  n                    = 24000
  ncrit                = 16
  images               = 1
  cycle                = 6.2832
  rega                 = 0.0500
  ewald_ksize          = 11
  (f,d,e)              = (1,1,1)
  num_compare          = 24000
  th_num               = 8
  seed                 = 123
  check_tree           = 0
  timing               = 1
  verbose              = 0
  use_fft              = 1
  use_precompute       = 1
  use_simd             = 1
  dipole_correction    = 1
  zero_netcharge       = 1
  print_body_number    = 3
  divide_4pi           = 0
  setting_t            = 0
  reg_image0_type      = d
  [x0,y0,z0]           = [0.000000,0.000000,0.000000] for body[-1], check body[0]
]
```

+ The result should look like :  
```
-----------------------------FMM vs Direct------------------------------[24000]
L2  (p)  : 7.29738e-14   L2  (f)  : 5.28167e-13   L2  (e)  : 2.25971e-13
Rms (p)  : 1.77738e-12   Rms (f)  : 7.25382e-11
p-energy1 : -1.387562119493e+03
p-energy2 : -1.387562119493e+03

------------------------------FMM vs Ewald------------------------------[24000]
L2  (p)  : 2.52782e+00   L2  (f)  : 1.57043e-03   L2  (e)  : 7.48177e-03
Rms (p)  : 2.19206e+01   Rms (f)  : 2.15689e-01
p-energy1 : -1.387562119493e+03
p-energy2 : -1.377257796841e+03

----------------------------Direct vs Ewald-----------------------------[24000]
L2  (p)  : 2.52782e+00   L2  (f)  : 1.57043e-03   L2  (e)  : 7.48177e-03
Rms (p)  : 2.19206e+01   Rms (f)  : 2.15689e-01
p-energy1 : -1.387562119493e+03
p-energy2 : -1.377257796841e+03
```
"""

def usage():
    print(Markdown(desp))
    
def parse_comparison(label : str, txt : str, sort : bool) -> list:
    settings1 = re.findall(r'  P                    = (.*)', txt)
    settings2 = re.findall(r'  images               = (.*)', txt)
    
    comparison = re.findall(f'{label}.*\nL2  \(p\)  : (.*)L2  \(f\)  : (.*)L2  \(e\)  : (.*)\n',txt)

    ps = [eval(fmm) for fmm in settings1]
    imgs = [eval(fmm) for fmm in settings2]
    
    l2ps = [eval(res[0]) for res in comparison]
    l2fs = [eval(res[1]) for res in comparison]
    l2es = [eval(res[2]) for res in comparison]
    
    data = [[p,i,l2p,l2f,l2e] for p,i,l2p,l2f,l2e in zip(ps,imgs,l2ps,l2fs,l2es)]
    if sort:
        data = sorted(data, key=lambda x: x[0])
    return data
    
def parse(txt : str, sort = True) -> dict:
    '''
    return [[P,l2p,l2f,l2e],...] data sorted by P
    '''
    
    fvd = parse_comparison('FMM vs Direct', txt, sort)
    fve = parse_comparison('FMM vs Ewald', txt, sort)
    dve = parse_comparison('Direct vs Ewald', txt, sort)
    
    return {
        "fvd" : fvd, 
        "fve" : fve, 
        "dve" : dve
    }

def make_table(data, title):
    table = Table(title=title,box=box.HORIZONTALS)
    table.add_column("P", justify="center", style="yellow")
    table.add_column("img", justify="center", style="yellow")
    table.add_column("l2p", justify="center", style="cyan")
    table.add_column("l2f", justify="center", style="cyan")
    table.add_column("l2e", justify="center", style="cyan")
    for d in data:
        table.add_row(*[f"{x}" for x in d])
    return table
