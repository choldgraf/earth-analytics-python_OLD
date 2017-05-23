

```python
import nbformat as nf
import nbconvert as nc
import os
import subprocess
from glob import glob
from datetime import datetime
```


```python
files = glob('../live/*/*/*.ipynb')
```


```python
datetime.
```


```python
run_keys = {'modified': lambda a: a.format(datetime.today())}
```


```python
tmp_file = './tmp.ipynb'
```


```python
for ifile in files:
    ntbk = nf.read(ifile, nf.NO_CONVERT)
    meta = ntbk['cells'][0]
    if meta['cell_type'] != 'raw':
        continue
    metalines = meta['source'].split('\n') 
    for ii, ln in enumerate(metalines):
        if '---' in ln:
            continue
        split = ln.split(': ')
        if len(split) < 2:
            continue
        if len(split) > 2:
            ln_type = split[0]
            ln_val = ': '.join(split[1:])
        else:
            ln_type, ln_val = split     
        if ln_type not in run_keys.keys():
            continue
        new_val = eval(run_keys[ln_type](ln_val))
        metalines[ii] = ': '.join([ln_type, new_val])
    meta['source'] = '\n'.join(metalines)
    ntbk['cells'][0] = meta
    
    # Write the file
    nf.write(ntbk, tmp_file)
    
    # Call nbconvert
    subprocess.call()
nc.
```


```python

```




    ['---',
     'layout: single',
     'title: "Work with Precipitation Data in R - 2013 Colorado Floods"',
     'excerpt: "This lesson provides students wiht an example of a data driven report to emphsize the importance of connecting data, documentation and results."',
     "authors: ['Leah Wasser', 'NEON Data Skills', 'Mariela Perignon']",
     'modified: 2017-05-11',
     'category: [course-materials]',
     "class-lesson: ['co-floods-1-intro']",
     'permalink: /course-materials/earth-analytics/week-1/co-floods-data-example-r/',
     "nav-title: 'CO Floods Data Example'",
     'week: 1',
     'sidebar:',
     '  nav:',
     'author_profile: false',
     'comments: true',
     'order: 2',
     '---',
     '']


