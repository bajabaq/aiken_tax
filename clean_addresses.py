#!/usr/bin/python

import sys
import re

inf = 'addresses-x.csv'
out = 'addresses-y.csv'
ifo = open(inf,'r')
ofo = open(out,'w')

i = 1
next(ifo) #skip first line
for line in ifo:
    if i == 1:
        ofo.write(line)
    else:
        line  = line.rstrip('\n')
        aline = line.split(',')
        gmap2 =  aline[-1]
        gmap1 =  aline[-2]
        lng   =  float(aline[-3])
        lat   =  float(aline[-4])

        if 33.20 < lat and lat < 33.88 and -82.050 < lng and lng < -81.15:
            #this is a good one
            ofo.write(line + '\n')
        else:
            print "bad one:" + str(lat) + " " + str(lng)        
            len(line)
            nline = ''
            for a in aline[:-4]:
                nline = nline + a + ','
            #endfor
            nline.rstrip(',')
            ofo.write(nline + '\n')
        #endif
    #endif
    i = i + 1
#endfor

sys.exit()

