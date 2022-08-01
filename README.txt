get tax sale *pdf
open pdf
copy paste into taxsale_list.txt
run clean_taxlist.py (save as chk_parcels.txt)

edit get_parcels.py and change "year" to last year (ie if it is 2015, then change "year" to 2014)

check that aikencoutysc.gov address is still valid

run get_parcels.py -
    download the parcel tax information

    if still a delinquient parcel
        download the parcel location information
    
    creates text files of
    delinquient parcels (parcel_got.txt)
    paid off parcels (parcel_paid.txt)
    parcels with an error in the listing (parcel_error.txt)

make_data.py - creates an html file of the parcels in parcel_got

need to get the address from the parcels
then create a document with a link to googlemaps (get_addresses should do that)
and possibly with the bid_data

