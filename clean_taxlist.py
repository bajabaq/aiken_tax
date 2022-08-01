#!/usr/bin/python

import sys
import re

inf = 'taxsale_list.txt'
out = 'chk_parcels.txt'
ifo = open(inf,'r')
ofo = open(out,'w')

for line in ifo:
    aline = re.split('\s+',line)
    for a in aline:
        if re.search('\d\d\d\-\d\d\-\d\d\-\d\d\d', a):
            ofo.write(a+'\n')
        #endif
    #endfor
#endfor

sys.exit()

