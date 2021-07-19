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
    "title": "Cybersecurity Maturity Model (CMMC) - With Objectives, Version 1.0",
    "description": "The Office of the Under Secretary of Defense for Acquisition and Sustainment (OUSD(A&S)) recognizes that security is foundational to acquisition and should not be traded along with cost, schedule, and performance moving forward. The Department is committed to working with the Defense Industrial Base (DIB) sector to enhance the protection of controlled unclassified information (CUI) within the supply chain.",
    "datePublished": "3/18/2020",
    "lastRevisionDate": "3/18/2020",
    "url": "https://www.acq.osd.mil/cmmc/docs/CMMC_ModelMain_V1.02_20200318.pdf",
    "abstract": "CMMC stands for “Cybersecurity Maturity Model Certification” and is a unifying standard for the implementation of cybersecurity across the Defense Industrial Base (DIB). The CMMC framework includes a comprehensive and scalable certification element to verify the implementation of processes and practices associated with the achievement of a cybersecurity maturity level. CMMC is designed to provide increased assurance to the Department that a DIB company can adequately protect sensitive unclassified information, accounting for information flow down to subcontractors in a multi-tier supply chain.",
    "keywords": "CMMC; Supply Chain; DID; Cyber Security; Maturity Model;",
    "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14" }

# create the catalog and printe success result
response = requests.request("POST", url_cats, headers=headers, json=cat)
jsonResponse = response.json()
print("\n\nAtlasity Output\n")
print("\nCatalog ID: " + str(jsonResponse["id"]))

# get the catalog ID
intCat = jsonResponse["id"]

# load local json
f = open('cmmc_objectives.json', 'r', encoding='utf-8-sig')
data = json.load(f)

# create controls array
controls = []

# create a counter for records created
intTotal = 0

# your Atlasity URL
url_sc = "https://atlas-dev.c2labs.com/api/securitycontrols"

# initialize the base variables (used to handle merged rows with child objectives)
strCMMC = ""
strCUI = ""
strRequirement = ""

#loop through and print the results
for i in data["Controls2Objectives"]:
    # see if this is a parent level control
    if "CMMC" in i:
        # see if the CMMC ID changed
        if (i["CMMC"] != strCMMC):
            # reassign all parent values
            strCMMC = i["CMMC"]
            strCUI = i["CUI"]
            strRequirement = i["Practice Requirement"]

    # create each security control
    sc = {
    "controlID": i["Assessment Objective ID"],
    "title": i["Assessment Objective"],
    "description": strRequirement,
    "references": "CUI: " + strCUI,
    "relatedControls": "CMMC: " + strCMMC,
    "subControls": "",
    "enhancements": "",
    "family": "",
    "mappings": "",
    "assessmentPlan": "",
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
with open("atlasity-cmmc-objectives.json", "w") as outfile: 
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




