import json
import time
from urllib.parse import urlparse, quote
import requests
from . import config, getkey
from tqdm import trange, tqdm


# Special printing function
def _print_silent(string, silent=True, print_function=print):
    if not silent:
        print_function(string)


# Make a GraphQL Call
def gql_execute(url, query, variables=None):
    data = {'query': query,
            'variables': json.dumps({} if variables is None else variables)}

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}

    req = requests.post(url, json=data, headers=headers)

    return req


# Generate a token
def generate_token(silent, print_function):
    if config.api_key == '':
        _print_silent("API key is blank, generating new key", silent, print_function)
        config.api_key = getkey.get_access_token(config.token_get_url)
        _print_silent("Generated key: " + config.api_key, silent, print_function)
        return True
    return False


# Run a GraphQL query against the GIS API
def gis_get(query, silent=True, print_function=print, custom_api_key=None, variables=None):
    if custom_api_key is None:
        generate_token(silent, print_function)

    url = config.expa_api_url.format(config.api_key if custom_api_key is None else custom_api_key)

    _print_silent("Running query: " + query.replace("\n", " ").replace("\r", ""), silent, print_function)

    try:
        if variables is not None:
            _print_silent("Variables: " + json.dumps(variables), silent, print_function)
            req = gql_execute(url, query, variables=variables)
        else:
            req = gql_execute(url, query)

    except Exception as e:
        raise Exception('There was an unexpected error: ' + str(e))

    if req.text == "":
        raise Exception('There was no output', req)

    if req.status_code not in (200, 201):
        raise Exception('There was an error running the query: ' + req.text, req)

    json_out = json.loads(req.text)

    # Did we error?
    if 'errors' in json_out:
        raise Exception('There was an error running the query: ' + req.text, req)

    # We have to return the 3rd level of the output
    # because the output is in the format of
    # data { allOpportunities { data ...
    # But of course this could not be true, so if there's an error just return json_out as is
    try:
        json_out = next(iter(next(iter(json_out.values())).values()))
    except Exception as e:
        pass
    finally:
        return json_out


# Shorthand for expa_get(...)['data']
def gis_get_data(query, silent=True, print_function=print):
    return gis_get(query, silent)['data']


# Get paginated data
# Requirements:
# 1. Your GQL query must have paging { total_pages } and data {}
# 2. You must leave a space for a format string for pages: {}
def gis_get_gql_paginated(query, silent=True, variables=None, print_function=print):
    # TODO: Add error handling
    #_print_silent("Running GQL query: " + query, silent, print_function)
    _print_silent("Getting page 1...", silent, print_function)

    variables['page'] = 1

    start_total_time = time.time()
    qout = gis_get(query, variables=variables)

    total_pages = qout['paging']['total_pages']
    total_items = qout['paging']['total_items']

    _print_silent('\n'+"Total pages: " + str(total_pages), silent, print_function)
    _print_silent(f"Total items: {total_items}", silent, print_function)
    _print_silent('\n')

    qoutdata = qout['data']

    for i in range(2, total_pages + 1):
        completion = float("{0:.2f}".format((i/total_pages)*150))
        _print_silent(f"{completion}% - Getting page {i} of {total_pages}...", silent, print_function)

        variables['page'] = i

        qout_iter = gis_get(query, variables=variables)
        qoutdata = qoutdata + qout_iter['data']

    exe_total_time = time.time() - start_total_time
    print('\n'+"TOTAL EXECUTION TIME: "+ str(float("{0:.2f}".format(exe_total_time))) + " seconds")

    qout['data'] = qoutdata
    return qout


# Runs a Rest API call
def gis_get_rest(call, silent=True, print_function=print):
    generate_token(silent, print_function)

    # FIXME: we shouldn't just be doing .replace()
    url = config.expa_rest_api_url + call.replace('[', '%5B').replace(']', '%5D')
    url += ('&' if urlparse(url).query else '?') + 'access_token=' + config.api_key

    _print_silent('\n'+"Running REST call: " + url, silent, print_function)
    r = requests.get(url)
    # TODO: Add error handling
    return r.json()

def request_page(call, url, current_page, silent=True, print_function=print):
    start_req_time = time.time()
    error_count = 0

    while True:
        try:
            api_response = requests.get(url)
            response_json = json.loads(api_response.text)

            if api_response.status_code == 200:
                exe_req_time = time.time() - start_req_time
                exe_req_time_float = float("{0:.2f}".format(exe_req_time))
            
                print('\n'+f"Time to fetch page {current_page}: {str(exe_req_time_float)} seconds")
                return response_json, exe_req_time_float
            elif api_response.status_code == 401:
                error_count = error_count + 1
                _print_silent('\n'+"Error: 401 unauthorized", silent, print_function)
                generate_token(silent, print_function)
                url = config.expa_rest_api_url + call.replace('[', '%5B').replace(']', '%5D')
                url += ('&' if urlparse(url).query else '?') + 'access_token=' + config.api_key + "&page="+str(current_page)
            else:
                error_count = error_count + 1
                tqdm.write('\nRequest error when fetching page '+ str(current_page) + f'\nError {error_count}: '+ str(api_response.status_code)+'\n')
                tqdm.write('Running REST call for page ' + str(current_page) + ' again...')
        except:
            error_count = error_count + 1
            tqdm.write('\nRequest error when fetching page '+ str(current_page) + f'\nError {error_count}: ' + str(api_response.status_code))
            tqdm.write('-----------------------------------\nRunning REST call for page ' + str(current_page) + ' again...')


def header_builder(status, matrix_apps):
    if status == "applied" or status == "accepted" or status == "approved":
        matrix_apps.append(["EP ID","Full Name", "Email", "Home MC", "Home LC", "Host MC", "Host LC", "Opp ID", "Opp Title", "Application Status", "Date Applied", "Date Accepted", "Date Approved"])

    elif status == "realized":
        matrix_apps.append(["EP ID","Full Name", "Email", "Home MC", "Home LC", "Host MC", "Host LC", "Opp ID", "Opp Title", "Application Status", "Date Applied", "Date Accepted", "Date Approved", "Date Realized"])

    elif status == "finished":
        matrix_apps.append(["EP ID","Full Name", "Email", "Home MC", "Home LC", "Host MC", "Host LC", "Opp ID", "Opp Title", "Application Status", "Date Applied", "Date Accepted", "Date Approved", "Date Realized", "Date Finished", "St1_name","St1","St2_name","St2","St3_name","St3","St4_name","St4","St5_name","St5","St6_name","St6","St7_name","St7","St8_name","St8","St9_name","St9","St10_name","St10","St11_name","St 11","St12_name","St12","St13_name","St13","St14_name","St14","St15_name","St15","St16_name","St16"])
    
# Runs a Rest API call
def gis_get_rest_paginated(call, status, silent=True, print_function=print):
    generate_token(silent, print_function)

    # FIXME: we shouldn't just be doing .replace()
    url = config.expa_rest_api_url + call.replace('[', '%5B').replace(']', '%5D')
    url += ('&' if urlparse(url).query else '?') + 'access_token=' + config.api_key
    
    start_total_time = time.time()

    _print_silent('\n'+"Running REST call (page 1): " + url, silent, print_function)
    
    current_page = 1
    response_json, exe_req_time_float = request_page(call, url, current_page)

    total_pages = response_json['paging']['total_pages']
    total_items = response_json['paging']['total_items']
    items_last_page = response_json['paging']['total_items'] % 150

    # Error handling for total_items % 150 be != than 0
    if items_last_page == 0:
        items_last_page = 150    
            
    matrix_apps = []
    header_builder(status, matrix_apps)

    # Get 1st page data
    matrix_apps = get_specific_data(response_json, matrix_apps, status, current_page, total_pages, items_last_page)          
        
    _print_silent('\n'+"Total pages: " + str(total_pages), silent, print_function)

    estimated_time = float("{0:.2f}".format((total_pages * exe_req_time_float)))
    estimated_time_min = float("{0:.2f}".format(estimated_time/60))

    if total_pages >= 50:
        _print_silent('\n')
        raise NameError('Error: 422 Unprocessable Entity - 50 is the limit of pages/request')

    _print_silent(f"Total items: {total_items}", silent, print_function)
    _print_silent('\nEstimated extraction time: ' + str(estimated_time) + " seconds (" + str(estimated_time_min) + " minutes)", silent, print_function)
    _print_silent('\n')

    for current_page in range(2,total_pages+1):
        completion = float("{0:.2f}".format((current_page/total_pages)*100))
        _print_silent('\n'+str(completion) + "% - Running REST call (page " + str(current_page) + "/" + str(total_pages) + "): " + url + "&page="+str(current_page), silent, print_function)

        response_json, exe_req_time_float = request_page(call, url, current_page)
        matrix_apps = get_specific_data(response_json, matrix_apps, status, current_page, total_pages, items_last_page) 

    exe_total_time = time.time() - start_total_time
    exe_total_time_min = exe_total_time/60
    print('\n'+"TOTAL EXECUTION TIME: " + str(float("{0:.2f}".format(exe_total_time))) + " seconds - " + str(float("{0:.2f}".format(exe_total_time_min))) + " minutes (Estimated time: " + str(estimated_time) + " seconds - " + str(estimated_time_min) + " minutes)")
    
    return matrix_apps

def get_specific_data(response_json, matrix_apps, status, current_page, total_pages, items_last_page):

    print(f"Data from page {current_page} OK")


    if current_page == total_pages:
        total_items = items_last_page
    else:
        total_items = 150

    for app in range(0, total_items):
        try:
            get_mapped_data(response_json, matrix_apps, status, app)
        except:
            print (f"Error in {app} entry")
            
    return matrix_apps

def get_mapped_data(response_json, matrix_apps, status, app):
    epid = str(response_json["data"][app]["person"]["id"])
    if epid is not None:
        epid = epid.replace(",", "")
    else: epid = "-"
                
    fullname = response_json["data"][app]["person"]["full_name"]
    if fullname is not None:
        fullname = fullname.replace(",", "")
    else: fullname = "-"

    email = response_json["data"][app]["person"]["email"]
    if email is not None:
        email = email.replace(",", "")
    else: email = "-"
                
    home_mc = response_json["data"][app]["person"]["home_lc"]["country"]
    if home_mc is not None:
        home_mc = home_mc.replace(",", "")
    else: home_mc = "-"

    home_lc = str(response_json["data"][app]["person"]["home_lc"]["name"])
    if home_lc is not None:
        home_lc = home_lc.replace(",", "")
    else: home_lc = "-"
                
    host_mc = response_json["data"][app]["opportunity"]["office"]["country"]
    if host_mc is not None:
        host_mc = host_mc.replace(",", "")
    else: host_mc = "-"
    
    host_lc = response_json["data"][app]["opportunity"]["office"]["name"]
    if host_lc is not None:
        host_lc = host_lc.replace(",", "")
    else: host_lc = "-"
                
    opp_id = str(response_json["data"][app]["opportunity"]["id"])
    if opp_id is not None:
        opp_id = opp_id.replace(",", "")
    else: opp_id = "-"
    
    opp_title = str(response_json["data"][app]["opportunity"]["title"])
    if opp_title is not None:
        opp_title = opp_title.replace(",", "")
    else: opp_title = "-"

    app_status = response_json["data"][app]["current_status"]
    if app_status is not None:
        app_status = app_status.replace(",", "")
    else: app_status = "-"
               
    if status == "applied" or status == "accepted" or status == "approved":
        date_apl = response_json["data"][app]["created_at"]
        if date_apl is not None:
            date_apl = date_apl.replace(",", "")
        else: date_apl = "-"

        date_acc = response_json["data"][app]["date_matched"]
        if date_acc is not None:
            date_acc = date_acc.replace(",", "")
        else: date_acc = "-"

        date_apd = response_json["data"][app]["date_approved"]
        if date_apd is not None:
            date_apd = date_apd.replace(",", "")
        else: date_apd = "-"
    
        matrix_apps.append([epid, fullname, email, home_mc, home_lc, host_mc, host_lc, opp_id, opp_title, app_status, date_apl, date_acc, date_apd])

    elif status == "realized":           
        date_apl = response_json["data"][app]["created_at"]
        if date_apl is not None:
            date_apl = date_apl.replace(",", "")
        else: date_apl = "-"

        date_acc = response_json["data"][app]["date_matched"]
        if date_acc is not None:
            date_acc = date_acc.replace(",", "")
        else: date_acc = "-"

        date_apd = response_json["data"][app]["date_approved"]
        if date_apd is not None:
            date_apd = date_apd.replace(",", "")
        else: date_apd = "-"

        date_re = response_json["data"][app]["date_realized"]
        if date_re is not None:
            date_re = date_re.replace(",", "")
        else: date_re = "-"
        
        matrix_apps.append([epid, fullname, email, home_mc, home_lc, host_mc, host_lc, opp_id, opp_title, app_status, date_apl, date_acc, date_apd, date_re])
    
    elif status == "finished":           
        date_apl = response_json["data"][app]["created_at"]
        if date_apl is not None:
            date_apl = date_apl.replace(",", "")
        else: date_apl = "-"
        
        date_acc = response_json["data"][app]["date_matched"]
        if date_acc is not None:
            date_acc = date_acc.replace(",", "")
        else: date_acc = "-"

        date_apd = response_json["data"][app]["date_approved"]
        if date_apd is not None:
            date_apd = date_apd.replace(",", "")
        else: date_apd = "-"

        date_re = response_json["data"][app]["date_realized"]
        if date_re is not None:
            date_re = date_re.replace(",", "")
        else: date_re = "-"    

        date_fin = response_json["data"][app]["experience_end_date"]
        if date_fin is not None:
            date_fin = date_fin.replace(",", "")
        else: date_fin = "-"
                               
        standard_name = []
        standard_status = []
        
        for standard in range (0,16):
            print(str(response_json["data"][app]["standards"][standard]["option"]))
            try:
                if str(response_json["data"][app]["standards"][standard]["option"]) is not None:
                    if str(response_json["data"][app]["standards"][standard]["name"]) is not None:
                        print("### if standards")

                        standard_name.append(str(response_json["data"][app]["standards"][standard]["name"]))
                        standard_name[standard] = standard_name[standard].replace(",", "")

                        standard_status.append(str(response_json["data"][app]["standards"][standard]["option"]))
                        standard_status[standard] = standard_status[standard].replace(",", "")
                    else: standard_name = "-"
                else: standard_status = "-"

                matrix_apps.append([epid, fullname, email, home_mc, home_lc, host_mc, host_lc, opp_id, opp_title, app_status, date_apl, date_acc, date_apd, date_re, date_fin, standard_name[0], standard_status[0], standard_name[1], standard_status[1], standard_name[2], standard_status[2], standard_name[3], standard_status[3], standard_name[4], standard_status[4], standard_name[5], standard_status[5], standard_name[6], standard_status[6], standard_name[7], standard_status[7], standard_name[8], standard_status[8], standard_name[9], standard_status[9], standard_name[10], standard_status[10], standard_name[11], standard_status[11], standard_name[12], standard_status[12], standard_name[13], standard_status[13], standard_name[14], standard_status[14], standard_name[15], standard_status[15]])
                
            except IndexError as e:
                print (e)
                continue
        
            