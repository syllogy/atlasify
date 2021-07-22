#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse

class Logger:
    OK = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'

# setup parser for command line arguments
parser = argparse.ArgumentParser(description='Atlasity parser for CMMC with Objectives')
parser.add_argument('--user', metavar='path', type=str, help='Atlasity username')
parser.add_argument('--pwd', metavar='path', type=str, help='Atlasity password')

# get the argument from the command line
args = parser.parse_args()
if (args.user == ''):
    print('ERROR: No username provided.')
    exit
else:
    strUser = args.user
if (args.pwd == ''):
    print('ERROR: No password provided.')
    exit
else:
    strPWD = args.pwd

# login to your Atlasity instance
url_login = "https://atlas-dev.c2labs.com/api/authentication/login"

# set the catalog URL for your Atlasity instance
url_cats = "https://atlas-dev.c2labs.com/api/catalogues"

# setup the authentication object
auth = {
    "username": strUser,
    "password": strPWD,
    "oldPassword": ""
}

# login and get token
response = requests.request("POST", url_login, json=auth)
authResponse = response.json()
userId = authResponse["id"]
jwt = "Bearer " + authResponse["auth_token"]
headers = {
   'Authorization': jwt
}

# setup catalog data
cat = {
    "title": "Standardized Architecture for CIS AWS Foundations Benchmark, Version 1.2",
    "description": "This document describes the CIS Amazon Web Services Foundations Security Requirements that are directly addressed by this AWS Quick Start package.",
    "datePublished": "5/23/2018",
    "lastRevisionDate": "5/23/2018",
    "url": "https://www.cisecurity.org/benchmark/amazon_web_services/",
    "abstract": "Securing Amazon Web Services - an objective, consensus-driven security guideline for the AWS cloud providers.",
    "keywords": "CIS; AWS; Benchmarks; Security Controls;",
    "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "master": False }

# create the catalog and printe success result
response = requests.request("POST", url_cats, headers=headers, json=cat)
jsonResponse = response.json()
print("\n\nAtlasity Output\n")
print("\nCatalog ID: " + str(jsonResponse["id"]))

# get the catalog ID
intCat = jsonResponse["id"]

# load local json
f = open('cis-aws.json', 'r', encoding='utf-8-sig')
data = json.load(f)

# create controls array
controls = []

# create a counter for records created
intTotal = 0

# your Atlasity URL
url_sc = "https://atlas-dev.c2labs.com/api/securitycontrols"

#loop through and print the results
for i in data["CIS Checklist"]:

    # parse optional fields
    strDescription = ""
    strGuidance = ""
    strResponsibility = ""
    if "Description" in i:
        strDescription = i["Description"]
    if "Guidance" in i:
        strGuidance = i["Guidance"]
    if "Responsibility" in i:
        strResponsibility = "Responsibility: " + i["Responsibility"]

    # create each security control
    sc = {
    "controlID": i["Control ID"],
    "title": i["Title"],
    "description": strDescription,
    "references": strResponsibility,
    "relatedControls": "",
    "subControls": "",
    "enhancements": "",
    "family": i["Family"],
    "mappings": "",
    "assessmentPlan": strGuidance,
    "weight": 0,
    "practiceLevel": "",
    "isPublic": True,
    "controlType": "Stand-Alone",
    "catalogueID": intCat,
    "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14" }

    #append the result
    controls.append(sc)

    # increment the count
    intTotal += 1

    # attempt to create the security control
    try:
        response = requests.request("POST", url_sc, headers=headers, json=sc)
        jsonResponse = response.json()
        print("\n\nSuccess - " + sc["title"])
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        print("\n\nError - " + sc["title"])
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        print("\n\nError - " + sc["title"])
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        print("\n\nError - " + sc["title"])
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        print("\n\nError - " + sc["title"])

# output total controls created
print(intTotal)

#artifacts for troubleshooting/verifications
with open("atlasity-cis-aws.json", "w") as outfile: 
    outfile.write(json.dumps(controls, indent=4)) 

# retrieve full list created
url_allcats = "https://atlas-dev.c2labs.com/api/SecurityControls/filterSecurityControlsByCatalogue/" + str(intCat)

headers_allcats = {
   "Accept": "application/json",
   'Authorization': jwt
}

allcats = requests.request(
   "GET",
   url_allcats,
   headers=headers_allcats,
)
catsArray = allcats.json()

# loop through and compare arrays, see if anything is missing (validation check)
intMatch = 0
for y in controls:
    bMatch = False
    # make sure each control in the raw JSON was returned from Atlasity
    for z in catsArray:
        if z["title"] == y["title"] :
            bMatch = True
            break
    #make sure they match or throw error in console if missing
    if bMatch == True :
        intMatch += 1
    else:
        # ones that didn't upload
        print("ERROR: " + y["title"] + " is missing.")
        # see if it was length related
        print(len(y["title"] ))

# validate all were loaded
if intMatch == intTotal :
    print("SUCCESS: Verified all controls were successfully created.")




