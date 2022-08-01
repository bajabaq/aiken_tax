#!/usr/bin/python

import simplejson, urllib
import re
import sys
import os
import time
from bs4 import BeautifulSoup


def get_data(row):       
    cols = row.find_all('td')
    data = cols[1].get_text().strip()
    data = ' '.join(data.split())
    return data
#enddef


def get_addy(parcel, parcel_dir):
    #open parcel_page
    source   = parcel_dir + parcel + '.html'
    sfo    = open(source,'r')
    contents = sfo.read()
    sfo.close()

    #get contents
    contents = contents.decode('windows-1252')
    soup   = BeautifulSoup(contents, "lxml")
    tables = soup.find_all('table')
    owner_location_table = tables[10]
    rows   = owner_location_table.find_all('tr')

    prop_loc  = get_data(rows[1]).lower() #2nd row is address
    fire_dist = get_data(rows[4]).lower() #5th row is address
    tax_dist  = get_data(rows[5]).lower() #6th row is address

    tax_dist = "aiken"

    
    return prop_loc + "," + tax_dist
#    return prop_loc + "," + fire_dist + "," + tax_dist
    
"""
        tax = aline[2].replace("city of","")
        tax = aline[2].replace("city","")
        tax = tax.rstrip()
        tax = tax.replace("gregg","aiken")
        tax = tax.replace("lang bath clear", "aiken")
        tax = tax.replace("college acres", "aiken")

        fire = aline[3]
        fire = fire.replace("fire department","")
        fire = fire.replace("fire district","")
        fire = fire.rstrip()
        fire = fire.replace("center","aiken")
        fire = fire.replace("couchton","aiken")

           
        if tax == "unincorporated":
            addy = loc + ", " + fire + " sc"
        else:
            addy = loc + ", " + tax + " sc"
        #endif
        print addy
        addy = addy.replace(" ", "+")


"""

inf = 'parcel_got.txt'
out = 'addresses-x.csv'
ifo = open(inf,'r')
ofo = open(out,'w')
parcel_dir = './parcels/'
    
GEOCODE_BASE_URL = "http://maps.googleapis.com/maps/api/geocode/json"

inid= 0
start= False

nline = 'link,lat,lng,gmap'
ofo.write(nline + '\n')
for line in ifo:
    parcel = line.strip()
    print "Working on " + parcel
    link="<a href="+parcel_dir+parcel+".html>"+parcel+"</a>"
    addy = get_addy(parcel, parcel_dir)
 
#    print addy
#    sys.exit()

    #addy = "1600+Amphitheatre+Pkwy,+Mountain+View,+CA+94043"
    #addy = "41+rusty,+gregg+sc"

    url = GEOCODE_BASE_URL + "?address="+addy+"&sensor=false"
#    print url
    result = simplejson.load(urllib.urlopen(url))
#    print result
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']

    gmap = "https://maps.google.com/maps?q="+str(lat)+","+str(lng)

    nline = link + ',' + str(lat) + ',' + str(lng) + ',' + str(gmap)                

    ofo.write(nline + '\n')
#    time.sleep(1)

#endfor
ifo.close()
ofo.close()

sys.exit()

