#!/usr/bin/python

import sys
import os
import time
import random
import subprocess
from bs4 import BeautifulSoup
import re

def get_parcel_details(parcel, parcel_dir):
    quiet = True

    cmd = "wget "
    if quiet == True:
        cmd = cmd + "--quiet "
    #endif
    cmd = cmd + "--secure-protocol=auto --delete-after --cookies=on --keep-session-cookies --save-cookies=cookie2.txt qpublic5.qpublic.net/ga_display_dw.php\?county=sc_aiken\&KEY=" + parcel + " -O parcel.html"
       
    cmd = cmd + "; wget "
    if quiet == True:
        cmd = cmd + "--quiet "
    #endif
    
    cmd = cmd + "--secure-protocol=auto --load-cookies=cookie2.txt --keep-session-cookies --save-cookies=cookie2.txt qpublic5.qpublic.net/ga_display_dw.php\?county=sc_aiken\&KEY="+ parcel + " -O parcel.html"
    
    cmd = cmd + "; mv parcel.html " + parcel_dir + parcel + "-details.html"

#    print cmd

    os.system(cmd)

    avg_one_and_half = random.randint(0,3)
    time.sleep(avg_one_and_half) #sleep for 1.5 seconds - so don't ddos the server

#enddef

def get_parcel_page(parcel, parcel_dir):       
    quiet = True

    cmd = "wget "
    if quiet == True:
        cmd = cmd + "--quiet "
    #endif
    cmd = cmd + "--secure-protocol=auto --delete-after --cookies=on --keep-session-cookies --save-cookies=cookie.txt https://acwebegs.aikencountysc.gov/EGSV2Aiken/RPSearch.do "

    cmd = cmd + "; wget "
    if quiet == True:
        cmd = cmd + "--quiet "
    #endif
    cmd = cmd + "--secure-protocol=auto --referer=https://acwebegs.aikencountysc.gov/EGSV2Aiken/RPSearch.do --cookies=on --load-cookies=cookie.txt --keep-session-cookies --save-cookies=cookie.txt "
    cmd = cmd + "--post-data 'dispatch=PrclSrch&srchprcl=&srchprclnew=" + parcel + "&srchstno=&srchstnm=' https://acwebegs.aikencountysc.gov/EGSV2Aiken/RPResult.do "
    cmd = cmd + "; mv RPResult.do " + parcel_dir + parcel + ".html"

#    print cmd

    os.system(cmd)
#enddef

#get the data in one row        
def get_data(row):       
    data = []
    cols = row.find_all('td')
    for col in cols:
        val = col.get_text()
        val = val.replace(" ", "_")
        val = val.replace(",", "")
        val = val.strip()
        data.append(val)
    #endfor
    return data
#enddef

def has_error(parcel, parcel_dir, year):
    error = False
    #open parcel_page
    source = parcel_dir + parcel + ".html"
    sfo    = open(source,'r')
    contents = sfo.read()
    sfo.close()

    #get contents - looking for year
    contents = contents.decode('windows-1252')
    soup   = BeautifulSoup(contents,"lxml")
    text = soup.body.get_text() #find_all('form')
    loc = text.find("real property search")
    if loc == -1:
        error = True

        #endif
    #endfor
    return error
#enddef

    
def is_delinquient(parcel, parcel_dir, year):
    #open parcel_page
    source = parcel_dir + parcel + ".html"
    sfo    = open(source,'r')
    contents = sfo.read()
    sfo.close()

    #get contents - looking for year
    contents = contents.decode('windows-1252')
    soup   = BeautifulSoup(contents,"lxml")
    tables = soup.find_all('table')

    #find the "Tax Year" table
    tax_info_table = 0
    for table in tables:
        obj = table.tr
        obj = str(obj)
        if obj == "None":
            print "not found"
        else:
            data00 = table.tr.get_text().strip()
            if "Tax Year" in data00:
                break
            elif "Parcel Number not found" in data00:
                return True
            #endif
        #endif
        tax_info_table = tax_info_table+1
    #endfor

    #found it, look for the year row
    tax_info_table = tables[tax_info_table]
    rows = tax_info_table.find_all('tr')
    r = 0
    for row in rows:
        cols  = row.find_all('td')
        if len(cols) > 0:
            cyear = str(cols[0].get_text().strip())
            if cyear == year:
                #print "found " + year + " row: " + str(r)
                break
            #endif
        #endif
        r = r + 1
    #endfor

    row = rows[r]
    data = get_data(row)

    tax_year      = data[0]
    receipt_num   = data[1]
    assessed_val  = float(data[2])
    base_amt      = float(data[3])
    total_tax_owed= float(data[4])
    collection_amt= float(data[5])

    #print tax_year, receipt_num, assessed_val, base_amt, total_tax_owed, collection_amt

    #if collection amount is 0.00, then taxes are delinquient
    delinquient = False
    if collection_amt == 0:
        delinquient = True
    #endif
    return delinquient
#enddef


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    #endif
    return int(result.strip().split()[0])
#enddef

#-------------------------------------------
# MAIN CODE HERE
#-------------------------------------------

"""
parcel = '004-16-07-009'
print parcel
parcel_dir = 'parcels/'
year = str(2015)
#get_parcel_page(parcel, parcel_dir)

delinquient = is_delinquient(parcel, parcel_dir, year)
if delinquient == True:
    print 'oh my'
#endif
sys.exit()
"""

parcel_dir = 'parcels/'
year = str(2016)

infile = 'chk_parcels.txt'
ifo = open(infile,'r')

xlast = file_len(infile)

x=1
for line in ifo:
    print "Getting parcel " + str(x) + " of " + str(xlast)

    parcel = line.strip()
    if os.path.isfile(parcel_dir + parcel + ".html") == True:  #got it
        print "\tGot parcel"
    else:
        print "Getting parcel " + str(parcel)
   
        get_parcel_page(parcel, parcel_dir)
      
        avg_one_and_half = random.randint(2,5) #actually 2.5 (X>=1.5)
        time.sleep(avg_one_and_half) #sleep for X seconds - so don't ddos the server
    #endif
    x = x + 1
#endfor
ifo.close()
os.system('rm -f cookie.txt')

#process parcels
outfile1= 'parcel_paid.txt'
ofo1 = open(outfile1,'w+')

outfile2= 'parcel_error.txt'
ofo2 = open(outfile2,'w+')

outfile3= 'parcel_got.txt'
ofo3 = open(outfile3,'w+')

data1 = set(ofo1.read().splitlines())
data2 = set(ofo2.read().splitlines())
data3 = set(ofo3.read().splitlines())


ifo = open(infile,'r')
x = 1
for line in ifo:
    parcel = line.strip()
    print "Processing parcel " + str(x) + " of " + str(xlast) + " (" + parcel + ")"
    skip = False
    res1 = parcel in data1
    res2 = parcel in data2
    res3 = parcel in data3
    if res1 == True:
        skip = True
    if res2 == True:
        skip = True
    if res3 == True:
        skip = True
    #endif

    if skip == False:
        if has_error(parcel, parcel_dir, year) == True:
            ofo2.write(parcel + '\n')
        elif is_delinquient(parcel, parcel_dir, year) == False: #not delinquient, so get rid of it
            ofo1.write(parcel + '\n')
        else: #not an error and not paid off, then parcel is a candidate
            ofo3.write(parcel + '\n')

            if os.path.isfile(parcel_dir + parcel + "-details.html") == True:  #got it
                print "\tGot parcel details"
            else:
                print "Getting parcel " + str(parcel) + " details"
   
                get_parcel_details(parcel, parcel_dir)
            #endif            
        #endif
    #endif
    x = x + 1
#endfor
ifo.close()

ofo1.close()
ofo2.close()
ofo3.close()     

#could put a check here where get file_len of ofo1-3 and make sure it equals xlen..
numerr  = file_len(outfile2)
numpaid = file_len(outfile1)
numrest = file_len(outfile3)

numtot = numpaid + numerr + numrest

print "Input ("+ str(xlast) + ") vs Total parcels in 3 files: " + str(numtot) + "- Paid (" + str(numpaid) + ") Error (" + str(numerr) + ") Rest (" + str(numrest) + ")"

if xlast == numtot:
    a = 1
    #mv input file to org_inp file
    #loop over parcel_got and remove from parcels
#endif


sys.exit()
