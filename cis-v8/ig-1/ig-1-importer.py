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
parser = argparse.ArgumentParser(description='Atlasity parser for the CIS Version 8 IG-1')
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
# url_login = "https://atlas-dev.c2labs.com/login"

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
    "title": "CIS Controls Version 8 - Implementation Group 1",
    "description": "The CIS Controls are a recommended set of actions for cyber defense that provide specific and actionable ways to thwart the most pervasive attacks. The CIS Controls are a relatively short list of high-priority, highly effective defensive actions that provide a 'must-do, do-first' starting point for every enterprise seeking to improve their cyber defense."
    + "<br />IG1 is the definition of basic cyber hygiene and represents a minimum standard of information security for all enterprises. IG1 assists enterprises with limited cybersecurity expertise thwart general, non-targeted attacks.",
    "datePublished": "5/18/2021",
    "lastRevisionDate": "5/18/2021",
    "url": "https://www.cisecurity.org/controls/cis-controls-navigator/",
    "abstract": "The Center for Internet Security (CIS) controls are a relatively short list of high-priority, highly effective defensive actions that provide a “must-do, do-first” starting point for every enterprise seeking to improve their cyber defense.<br/>Initially developed by the SANS Institute and known as the SANS Critical Controls, these best practices are indispensable to organizations both large and small. By adopting these sets of controls, organizations can prevent the majority of cyberattacks.",
    "keywords": "CIS; Version 8; cybersecurity",
    "createdById": "52f86957-eb18-4ec5-bddd-ae54d93bfcce",
    "lastUpdatedById": "52f86957-eb18-4ec5-bddd-ae54d93bfcce" }

# create the catalog and printe success result
response = requests.request("POST", url_cats, headers=headers, json=cat)
jsonResponse = response.json()
print("\n\nAtlasity Output\n")
print(response.text.encode('utf8'))
print("\nCatalog ID: " + str(jsonResponse["id"]))

# get the catalog ID
intCat = jsonResponse["id"]

# load local json
f = open('cis_v8_ig-1.json', 'r', encoding='utf-8-sig')
data = json.load(f)

# create controls array
controls = []

# create a counter for records created
intTotal = 0

# your Atlasity URL
url_sc = "https://atlas-dev.c2labs.com/api/securitycontrols"

#loop through and print the results
for i in data["CIS Controls Version 8 Implementation Group 1"]:
    mappings = ""
    if ("NIST CSF Mappings" in i):
        mappings = "NIST CSF Mappings: " + i["NIST CSF Mappings"]

    # create each security control
    # NOTE: Use your user ID in Atlasity which you can find under your user profile
    sc = {
    "controlID": i["ControlId"],
    "title": i["Title"],
    "description": i["Full Description"],
    "references": i["References"],
    "relatedControls": "",
    "subControls": "",
    "enhancements": "",
    "family": i["Family"],
    "mappings": mappings,
    "assessmentPlan": "",
    "weight": 0,
    "practiceLevel": "",
    "isPublic": True,
    "controlType": "Stand-Alone",
    "catalogueID": intCat,
    "createdById": "52f86957-eb18-4ec5-bddd-ae54d93bfcce",
    "lastUpdatedById": "52f86957-eb18-4ec5-bddd-ae54d93bfcce" }

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