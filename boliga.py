#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 11:15:33 2021

@author: sara
"""

import requests
import json
import time
from datetime import datetime

def pull_listings(zipcode=4581, propertyType=4, minyear = None, category = 'listings', write = False, date = True, silent = False):
    """
    Calls relevant API at boliga.dk (registry of properties in Denmark)
    "https://api.boliga.dk/api/v2/search/results" for properties currently for sale
    "https://api.boliga.dk/api/v2/sold/search/results" for all properties and their last sale since 1992
    
    Parameters
    ----------
    zipcode : integer, optional
        Search for properties with this zipcode. 
        The default is 4581.
    propertyType : integer, optional
        Search for properties of this type. Use None for all types. 
        The default is 4 (holiday homes).
    minyear : integer, optional
        Minimum year for search, None for no minimum. If not None, then write to file is switched off. 
        The default is None.
    category : string, optional
        'listings' (properties currently listed for sales), 
        'sold' (properties sold since 1992 with last date of sale), or 
        'bbrsearch' (all properties in area with last date of sale (date 0001-01-01 if no sale since 1992)). 
        The default is 'listings'.
    write : Boolean, optional
        Writes to file too if write = True. 
        The default is False.
    date : Boolean, optional
        Includes date in filename when writing to file (when write = True). 
        The default is True.
    silent : Boolean, optional
        Outputs progress if silent = False. 
        The default is False.
    """
    if category == 'listings':
        apiurl = "https://api.boliga.dk/api/v2/search/results"
    elif category == 'sold' or category == 'bbrsearch':
        apiurl = "https://api.boliga.dk/api/v2/sold/search/results"
    else:
        print('Nonvalid category - use "listings", "sold" or "bbrsearch"')
        return None
    results = []
    page = 1
    totalpages = 1
    parameters = {'sort': 'date-d',
                  'zipcodeFrom': zipcode,
                  'zipcodeTo': zipcode,
                  'street': ''}
    if category == 'bbrsearch':
        parameters['bbrsearch'] = 1
        parameters['sort'] = 'date-a'
    else:
        parameters['searchTab'] = 1
    if propertyType != None:
        parameters['propertyType'] = propertyType
    if minyear != None:
        parameters['salesDateMin'] = minyear
        write = False
    while page <= totalpages:
        parameters['page'] = page
        response = requests.get(apiurl, params=parameters)
        if response.status_code != 200:
            print("Page {}: status_code {} - aborting!".format(page, response.status_code))
            break
        totalpages = response.json()['meta']['totalPages']
        if not silent:
            print("Page {} of {}\n{}".format(page, totalpages, response.url))
        if totalpages >= 3600:
            print('Totalpages {}, aborting!'.format(totalpages))
            break
        results.extend(response.json()['results'])
        page += 1
        time.sleep(1)
    if write:
        if date:
            filename = category + '/' + category + str(datetime.now().strftime('%Y%m%d')) + '.txt'
        else:
            filename = category + '.txt'
        with open(filename, 'w') as file:
            file.write(json.dumps(results))
    return results

def get_totalcount(zipcodeFrom = None, zipcodeTo = None, bbrsearch = False, propertyType = 4, saleType = None):
    apiurl = "https://api.boliga.dk/api/v2/sold/search/results"
    parameters = {'sort': 'date-d',
                  'zipcodeFrom': zipcodeFrom,
                  'zipcodeTo': zipcodeTo,
                  'propertyType': propertyType,
                  'street': '',
                  'page': 1}
    if saleType == 1 or saleType == 2 or saleType == 3 or saleType == 4:
        parameters['saleType'] = saleType
        bbrsearch = False
    if bbrsearch:
        parameters['bbrsearch'] = 1
    response = requests.get(apiurl, params=parameters)
    if response.status_code != 200:
        print('Status code: {}'.format(response.status_code))
        return None
    else:
        totalcount = response.json()['meta']['totalCount']
        return totalcount

def get_soldinfo(soldlist, write = False):
    apiurl = "https://api.boliga.dk/api/v2/sold/info/{municipalityCode}/{estateCode}/{guid}"
    results = {}
    errors = []
    counter = 0
    for item in soldlist:
        counter += 1
        if item['soldDate'][0]=='0': # if soldDate in year 0001, so never sold
            print("Skipping property no. {}".format(counter))
            continue
        if counter % 100 == 0:
            print("Pulling property no. {}".format(counter))
        guid = item['guid']
        response = requests.get(apiurl.format(municipalityCode=item['municipalityCode'], estateCode=item['estateCode'], guid=guid))
        if response.status_code != 200:
            print('Something went wrong with {}.'.format(guid))
            errors.append(guid)
        else:
            results[guid] = response.json()
        time.sleep(1)
    if write:
        with open('soldinfo.txt', 'w') as file:
            file.write(json.dumps(results))
    return results, errors

def get_bbrinfo(soldlist, write = False):
    apiurl = "https://api.boliga.dk/api/v2/bbrinfo/bbr"
    results = {}
    errors = []
    counter = 0
    for item in soldlist:
        counter += 1
        if counter % 100 == 0:
            print("Pulling property no. {}".format(counter))
        guid = item['guid']
        response = requests.get(apiurl, params = {'id': guid})
        if response.status_code != 200:
            print('Something went wrong with {}.'.format(guid))
            errors.append(guid)
        else:
            bbrinfo = response.json()
            bbrinfo.pop('esrOwnershipInfo')
            results[guid] = bbrinfo
        time.sleep(1)
    if write:
        with open('bbrinfo.txt', 'w') as file:
            file.write(json.dumps(results))
    return results, errors


def update_soldinfo(zipcode=4581, propertyType=4, minyear = 2021, write = True, silent = True):
    returns = pull_listings(zipcode=zipcode, propertyType=propertyType, minyear = minyear, category = 'sold', write = False, date = True, silent = silent)
    results, errors = get_soldinfo(returns, write = False)
    if len(errors) != 0:
        print("Total of {} errors:\n{}".format(len(errors), errors))
    with open('soldinfo.txt', 'r') as file:
        soldinfo = json.load(file)
    soldinfo.update(results)
    if write:
        with open('soldinfo.txt', 'w') as file:
            file.write(json.dumps(soldinfo))
    return soldinfo, errors

def update_bbrinfo(bbrsearchlist, write = True):
    with open('bbrinfo.txt', 'r') as file:
        bbrinfo = json.load(file)
    missing = [item for item in bbrsearchlist if item['guid'] not in bbrinfo]
    results, errors = get_bbrinfo(missing, write=False)
    bbrinfo.update(results)
    if write:
        with open('bbrinfo.txt', 'w') as file:
            file.write(json.dumps(bbrinfo))
    return bbrinfo, errors


def update_sold(zipcode=4581, propertyType=4, minyear = 2021, write = True, silent = True):
    returns = pull_listings(zipcode=zipcode, propertyType=propertyType, minyear = minyear, category = 'sold', write = False, date = True, silent = silent)
    if returns == None:
        print('{} Something went wrong...')
        return None
    else:
        with open('sold.txt', 'r') as file:
            currentsold = json.load(file)   
        allsold = currentsold
        actuallynew = []
        for newitem in returns:
            new = True
            for item in currentsold:
                if item['guid'] == newitem['guid']:
                    if item['soldDate'] == newitem['soldDate']:
                        new = False
                        break
            if new:
                allsold.append(newitem)
                actuallynew.append(newitem)
                print('Appending new property at {} sold on {}'.format(newitem['address'], newitem['soldDate']))
        if write:
            with open('sold.txt', 'w') as file:
                file.write(json.dumps(allsold))
        return allsold, actuallynew

# update_soldinfo()

# pull_listings(category='bbrsearch', write=True, date=False)