import json
import requests
import csv
import sys
import datetime as dt

from json2csv import json2csv
from gisconnector.lc_list import lc_list
from gisconnector.apicall import gis_get_rest
from gisconnector.apicall import gis_get_rest_paginated

def convert_programme(prog):
    if prog == 'GV':
        return 1
    elif prog == 'GT':
        return 2
    elif prog == 'GE':
        return 5
    else:
        print("Programme entered is invalid.")
        exit()

if __name__ == "__main__":

    csv_file_path = '/home/thales/Documents/workspace/aiesec-projects/Data-Extraction-GraphQL/Extractions/'
    csv_file_name = ''

    # Setting up LC list
    lcs = lc_list()

    # INPUTS:
    prog = str(input("Programme (GV, GT, GE): "))
    programme_decoded = convert_programme(prog)
    
    status = str(input("status (applied, accepted, approved, realized, finished, completed): "))

    completed_filter = ''

    if status == 'applied':
        date_type = 'created_at'
    elif status == 'accepted':
        date_type = 'date_matched'
    elif status == 'approved':
        date_type = 'date_approved'
    elif status == 'realized':
        date_type = 'date_realized'
    elif status == 'finished':
        date_type = 'experience_end_date'
    elif status == 'completed':
        date_type = 'experience_end_date'
        completed_filter = '&filters%5Bstatus%5D=completed'

    else:
        raise NameError('error: app_type argument is invalid.')

    start_date = input("Start Date (yyyy-mm-dd): ")
    end_date = input("End Date (yyyy-mm-dd): ")

    entity_name = input("LC name: ")

    for lc in lcs:
        if lc['name'] == entity_name:
            entity_id = lc['id']
    
    type_req = str(input("Type (ICX, OGX): "))

    print('\n'+"### DATA ###"+'\n')

    csv_file_name += "Data " + entity_name + " " + type_req + " " + prog + " " + status + " " + start_date + " " + end_date + '.csv'
    csv_file_path += csv_file_name

    # ICX Data
    if type_req == "ICX":
        basic = "opportunities"
        if prog == 'GV':
            print("Getting IGV Applications...")
        elif prog == 'GT':
            print("Getting IGT Applications...")
        elif prog == 'GE':
            print("Getting IGE Applications...")

        applications = gis_get_rest_paginated(f'applications?&filters%5B{date_type}%5Bfrom%5D%5D={start_date}&filters%5B{date_type}%5Bto%5D%5D={end_date}&filters%5Bprogrammes%5D%5B%5D={programme_decoded}&per_page=150&filters%5Bopportunity_committee%5D={entity_id}{completed_filter}',status, silent=False)

    # OGX Data
    if type_req == "OGX":
        basic = "people"
        if prog == 'GV':
            print("Getting OGV Applications...")
        elif prog == 'GT':
            print("Getting OGT Applications...")
        elif prog == 'GE':
            print("Getting OGE Applications...")

        applications = gis_get_rest_paginated(f'applications?&filters%5B{date_type}%5Bfrom%5D%5D={start_date}&filters%5B{date_type}%5Bto%5D%5D={end_date}&filters%5Bprogrammes%5D%5B%5D={programme_decoded}&per_page=150&filters%5Bperson_committee%5D={entity_id}{completed_filter}', status, silent=False)

    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(applications)

