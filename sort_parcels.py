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
        
def get_data(row):       
    cols = row.find_all('td')
    data = cols[1].get_text()
    data = data.replace(" ","_")
    return data
#enddef

parcel_dir = 'parcels'

files = [ f for f in listdir(parcel_dir) if isfile(join(parcel_dir, f)) ]

x=0
for file in files:
    source   = parcel_dir + '/' + file    
    fo       = open(source,'r')
    contents = fo.read()

    soup   = BeautifulSoup(contents,'lxml')
    tables = soup.find_all('table')

    #find the "Ownership & Location Information" table
    tax_info_table = 0
    for table in tables:
        obj = table.tr
        obj = str(obj)
        if obj == "None":
            print "not found"
        else:
            data00 = table.tr.get_text().strip()
            if "Parcel Number" in data00:
                break
        #endif
        tax_info_table = tax_info_table+1
    #endfor
    
    rows   = tables[tax_info_table].find_all('tr')


    classification_row = rows[19]
    num_buildings_row  = rows[12]
    tax_district_row   = rows[10]
    fire_district_row  = rows[9]

    classification = get_data(classification_row).lower()
    num_buildings  = int(get_data(num_buildings_row))
    tax_district   = get_data(tax_district_row).lower()
    fire_district  = get_data(fire_district_row).lower()

    print file, classification, num_buildings, tax_district, fire_district
    
    if num_buildings > 1 :
        num_buildings = '1plus'
    #endif

    if classification != "residential" and classification != "commercial" and classification != "agricultural":
        classification = "other"
    #endif

    if len(fire_district) < 1:
        fire_district = "other"
    #endif

    dest_dir = 'sorted_parcels/' + fire_district + '/' + classification + '/' + str(num_buildings)
    dest     = dest_dir + '/' + file

    cmd = "mkdir -p " + dest_dir + " && cp " + source + " " + dest
#    print cmd

    os.system(cmd)

    #x = x + 1
    #if x > 0:
    #   sys.exit()
#endfor
    

sys.exit()


