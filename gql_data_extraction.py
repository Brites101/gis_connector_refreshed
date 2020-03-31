from gisconnector.apicall import gis_get_gql_paginated
from gisconnector.lc_list import lc_list
from pkgutil import get_data

from json2csv import json2csv
import datetime as dt
import json
import csv
import sys

def convert_programme(prog):
    if prog == 'GV':
        return [1]
    elif prog == 'GT':
        return [2]
    elif prog == 'GE':
        return [5]
    elif prog == 'ALL':
        return [1,2,5]
    else:
        print("Programme entered is invalid.")
        exit()

if __name__ == "__main__":
    get_applications = "get_applications.gql"
    get_people = "get_people.gql"
    get_email = "get_email.gql"

    csv_file_path = '/home/thales/Documents/workspace/aiesec-projects/Data-Extraction-GraphQL/Extractions GraphQL/'
    csv_file_name = ''

    # Setting up LC list
    lcs = lc_list()

    print('\n'+"INITIALIZING SCRIPT..."+'\n')

    # INPUTS:
    prog = str(input("Programme (GV, GT, GE, ALL): "))
    programmes_decoded = convert_programme(prog)

    status = str(input("status (applications, accepted, approved, realized, finished, completed): "))

    if status == 'applications':
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

    start_date = start_date + "T00:00:00.000Z"
    end_date = end_date + "T23:59:59.999Z"

    # ICX Data
    if type_req == "ICX":
        if prog == 'GV':
            print("Getting IGV Applications...")
        elif prog == 'GT':
            print("Getting IGT Applications...")
        elif prog == 'GE':
            print("Getting IGE Applications...")
        elif prog == 'ALL':
            print("Getting ICX Applications...")

        applications = gis_get_gql_paginated(get_data("gql", get_applications).decode("utf-8"), silent=False, variables={
            "applied_at": True,
            "status": True,
            "experience_start_date": True,
            "tags": False,
            "opportunity": True,
            "applicant_name": True,
            "organization": True,
            "host_mc": False,
            "host_lc": False,
            "home_mc": False,
            "home_lc": False,
            "phone_number": False,
            "date_realized": False,
            "page": 1,
            "perPage": 200,
            "filters": {
                "opportunity_committee": entity_id,
                "programmes": programmes_decoded,
                date_type: {
                    "from": start_date,
                    "to": end_date
                },
                #"status": "completed",
                "nps_grade_value": {
                    "min": None,
                    "max": None
                }
            },
            "sort": ""
        })  

        raw_json_data = json.loads(json.dumps(applications))['data']
        #print(raw_json_data)
        json2csv(raw_json_data, csv_file_path)

    # OGX Data
    elif type_req == "OGX":
        if prog == 'GV':
            print("Getting OGV Applications...")
        elif prog == 'GT':
            print("Getting OGT Applications...")
        elif prog == 'GE':
            print("Getting OGE Applications...")
        elif prog == 'ALL':
            print("Getting OGX Applications...")

        people = gis_get_gql_paginated(get_data("gql", get_people).decode("utf-8"), silent=False, variables={
            "first_name": True,
            "last_name": True,
            "name": False,
            "managers": False,
            "date_of_birth": False,
            "status": True,
            "phone": True,
            "home_lc": True,
            "referral": False,
            "home_mc": True,
            "contacted_at": False,
            "contacted_by": False,
            "signed_up_at": False,
            "lc_alignment": False,
            "selected_programmes": True,
            "phone_number": True,
            "page": 1,
            "perPage": 30,
            "filters": {
                "home_committee": entity_id,
                "selected_programmes": programmes_decoded,
                date_type: {
                    "from": start_date,
                    "to": end_date
                }
            },
            "q": None,
            "sort": ""
        })

        raw_json_data = json.loads(json.dumps(people))['data']
        json2csv(raw_json_data, csv_file_path)
    
    else:
        print("Error: Type of application was not found.")
