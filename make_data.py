#!/usr/bin/python

#loop over parcels
#look at each, sort by 
#classification: (commerical, residential, other)
#num of buildings: (0, 1, 1+)

import sys
import os
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import subprocess



def get_location(parcel, parcel_dir):
    #address and other details    
    source   = parcel_dir + '/' + parcel + '-details.html'
    sfo      = open(source,'r')
    contents = sfo.read()
    sfo.close()

    contents = contents.decode('windows-1252')
    soup   = BeautifulSoup(contents, "lxml")
    tables = soup.find_all('table')
    if len(tables) < 3:
        return ' '
    #endif
    
    owner_location_table = tables[2]
    rows   = owner_location_table.find_all('tr')

    location = ''
    this_row = False
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            val = col.get_text().strip()
            val = val.lower()
            if this_row == True:
                location = val
                break
            #endif
            if val == "location address":
                this_row = True
            #endif
        #endfor
        if this_row == True:
            break
        #endif
    #endfor

    return location
#enddef

def get_data(row):       
    cols = row.find_all('td')
    data = cols[1].get_text().strip()
    data = ' '.join(data.split())
    data = data.replace(' ','_')
    return data
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


#==================
#
# MAIN CODE HERE
#
#==================
tax_year = '2015'

outfile = 'data.html'

html = "<!DOCTYPE html\n"
html = html + "PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\n"
html = html + "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n"
html = html + "<html>\n"
html = html + "<head>\n"
html = html + "<title>Aiken Delinquent Tax Property</title>\n"
html = html + "<script src=\"sorttable.js\"></script>\n"
html = html + "</head>\n"
html = html + "<body>\n"
html = html + "<table class=\"sortable\">\n"
html = html + "<tr>\
    <th>Parcel Number</th>\
    <th>Property Location</th>\
    <th>Legal Description</th>\
    <th>Owner Name</th>\
    <th>Fire District</th>\
    <th>Tax District</th>\
    <th>Location Address</th>\
    <th>Base Tax</th>\
    <th>Total Tax Owed</th>\
    <th>Max Bid on Base</th>\
    <th>Max Bid on Total Tax Owed</th>\
</tr>\n"

ofo = open(outfile,'w')
ofo.write(html)

parcel_dir = 'parcels'

infile = 'parcel_got.txt'
ifo = open(infile,'r')

x=0
num_files = file_len(infile)

for line in ifo:
    parcel = line.strip()    
    print "Working on parcel " + parcel

    source   = parcel_dir + '/' + parcel + '.html'
    sfo      = open(source,'r')
    contents = sfo.read()
    sfo.close()
    
    contents = contents.decode('windows-1252')
    soup   = BeautifulSoup(contents, "lxml")
    tables = soup.find_all('table')
    owner_location_table = tables[10]
    rows   = owner_location_table.find_all('tr')

    html = "<tr>"
    html = "<tr><td>" + "<a href=./"+ parcel_dir +"/" + parcel + ".html>" +parcel + "</td>"

    for row in rows:
        if row == rows[-1]:  #last row has no data
            break
        if row == rows[0]:   #first row is parcel data
            continue
        col = get_data(row).lower()
        html = html + "<td>" + col + "</td>"        
    #endfor

    location = get_location(parcel, parcel_dir)
    
    html = html + "<td>" + location + "</td>"        
    
    
#    print html
#    sys.exit()
    
    tax_info_table = 0
    for table in tables:
        table = tables[tax_info_table]
        obj = table.tr
        obj = str(obj)
        if obj == "None":
            print "not found"
        else:
            data00 = table.tr.get_text().strip()
            if "Tax Year" in data00:
                break
        #endif
        tax_info_table = tax_info_table+1
    #endfor

    tax_info_table = tables[tax_info_table]

    year_row = ''
    for row in tax_info_table.find_all('tr'):
        for cell in row.find_all('td'):
            if cell.find(text=tax_year):
                year_row = row
                break
            #endif
        #endfor
        if year_row <> '':
            break
        #endif
    #endfor
#    print year_row

    data = []
    cols = year_row.find_all('td')

    for col in cols:
        val = col.get_text()
        val = val.replace(" ", "_")
        val = val.replace(",", "")    
        val = val.strip()
        #print y, val
        #y = y+1
        data.append(val)
    #endfor

    #tax_year      = data[0]
    base_amt      = float(data[3])
    total_tax_owed= float(data[4])
    max_bid_base  = (base_amt / 0.12)
    max_bid_total = (total_tax_owed / 0.12)

    #print tax_year
#    print base_amt
#    print total_tax_owed

    html = html + "<td>" + "{0:.2f}".format(base_amt)  + "</td>"
    html = html + "<td>" + "{0:.2f}".format(total_tax_owed) + "</td>"
    html = html + "<td>" + "{0:.2f}".format(max_bid_base)  + "</td>"
    html = html + "<td>" + "{0:.2f}".format(max_bid_total) + "</td>"
    html = html + "</tr>\n"

    if float(total_tax_owed) > 0:
#        print html
        ofo.write(html)
#    else:
        #print "deleting this file: " + parcel
#        os.remove(source)
    #endif

    
    x = x + 1
    percent_done = round((x/(num_files*1.0))*100)

#    print x, num_files,    (x/(num_files*1.0))*100, percent_done

    if 1 < percent_done and percent_done < 3:
        print "2% complete"
    elif 4 < percent_done and percent_done < 6:
        print "5% complete"
    elif 9 < percent_done and percent_done < 11:
        print "10% complete"
    elif 24 < percent_done and percent_done < 26:
        print "25% complete"
    elif 49 < percent_done and percent_done < 51:
        print "50% complete"
    elif 74 < percent_done and percent_done < 76:
        print "75% complete"
    #endif
    
#    if x > 10:
#        break
#endfor
ifo.close()
html = "</table>\n"
html = html + "</body>\n"
html = html + "</html>\n"

ofo.write(html)
ofo.close()
sys.exit()



