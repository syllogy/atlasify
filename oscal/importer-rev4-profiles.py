#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse

# setup parser for command line arguments
parser = argparse.ArgumentParser(description='Atlasity parser for NIST 800-53 OSCAL Profiles')
parser.add_argument('--user', metavar='path', type=str, help='Atlasity username')
parser.add_argument('--pwd', metavar='path', type=str, help='Atlasity password')
parser.add_argument('--catalog', metavar='path', type=int, help='Atlasity ID for imported catalog', required=True)

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
intAtlasityCat = args.catalog

# set the catalog URL for your Atlasity instance
url_login = "http://localhost:5000/api/authentication/login"

# setup the authentication object
auth = {
    "username": strUser,
    "password": strPWD,
    "oldPassword": ""
}

# create the catalog and print success result
response = requests.request("POST", url_login, json=auth)
authResponse = response.json()
userId = authResponse["id"]
jwt = "Bearer " + authResponse["auth_token"]
headers = {
   'Authorization': jwt
}

# retrieve full list created
url_controlsByCatalog = "http://localhost:5000/api/SecurityControls/filterSecurityControlsByCatalogueWithDetails/" + str(intAtlasityCat)

headers = {
   "Accept": "application/json",
   'Authorization': jwt
}

allcats = requests.request(
   "GET",
   url_controlsByCatalog,
   headers=headers,
)
atlasity = allcats.json()

with open("rev4artifacts/fullAtlasityCatalog.json", "w") as outfile: 
    outfile.write(json.dumps(atlasity, indent=4)) 

# create array of profiles to iterate through
profiles = [
    {
        "title": "NIST 800-53 Rev. 4 - Security and Privacy Controls for Information Systems and Organizations - HIGH Baseline",
        "fileName": "nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_HIGH-baseline_profile.json",
    },
    {
        "title": "NIST 800-53 Rev. 4 - Security and Privacy Controls for Information Systems and Organizations - MODERATE Baseline",
        "fileName": "nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_MODERATE-baseline_profile.json",
    },
    {
        "title": "NIST 800-53 Rev. 4 - Security and Privacy Controls for Information Systems and Organizations - LOW Baseline",
        "fileName": "nist.gov/SP800-53/rev4/json/NIST_SP-800-53_rev4_LOW-baseline_profile.json",
    }
]

# set the catalog URL for your Atlasity instance
url_cats = "http://localhost:5000/api/catalogues"

# assign catalog object
controls = atlasity["securityControls"]

# loop over the profiles to load each one
for p in profiles:
    # setup catalog data
    cat = {
        "title": p["title"],
        "description": atlasity["description"],
        "datePublished": atlasity["datePublished"],
        "lastRevisionDate": atlasity["lastRevisionDate"],
        "url": atlasity["url"],
        "abstract": atlasity["abstract"],
        "keywords": atlasity["keywords"],
        "createdById": userId,
        "lastUpdatedById": userId }

    # create the catalog and print success result
    response = requests.request("POST", url_cats, headers=headers, json=cat)
    jsonResponse = response.json()
    print("\n\nAtlasity Output\n" + p["title"])
    print("\nCatalog ID: " + str(jsonResponse["id"]))

    # get the catalog ID
    intCat = jsonResponse["id"]

    # load translated Excel file (cleaned and converted to JSON)
    oscal = open(p["fileName"], 'r', encoding='utf-8-sig')
    oscalData = json.load(oscal)

    # create a counter for records created
    intTotal = 0

    # your Atlasity URL
    url_sc = "http://localhost:5000/api/securitycontrols"

    #parse the OSCAL Profile JSON to get the controls to load 
    arrL1 = oscalData["profile"]
    imports = arrL1["imports"]
    obj = imports[0]
    include = obj["include"]
    ctrls = include["calls"]

    # array to hold controls for this profile
    upload = []

    #loop through controls in the baseline
    for c in ctrls:
        # find the control
        lookup = next((item for item in controls if item["controlId"] == c["control-id"]), None)
        print(lookup)

        # make sure something was returned
        if (lookup == None):
            print(p["title"] + " - " + c["control-id"] + " not found.")
        else:
            #update catalog ID
            lookup["catalogueID"] = intCat
            
            #add control to this baseline
            upload.append(lookup)

            # create a new security control
            sc = {
            "title": lookup["title"],
            "controlType": lookup["controlType"],
            "controlId": lookup["controlId"],
            "description": lookup["description"],
            "references": lookup["references"],
            "relatedControls": lookup["relatedControls"],
            "subControls": lookup["subControls"],
            "enhancements": lookup["enhancements"],
            "family": lookup["family"],
            "mappings": lookup["mappings"],
            "assessmentPlan": lookup["assessmentPlan"],
            "weight": lookup["weight"],
            "practiceLevel": lookup["practiceLevel"],
            "catalogueID": intCat,
            "createdById": userId,
            "lastUpdatedById": userId }

        #increment the total processed in this baseline
        intTotal += 1

        # attempt to create the security control
        if (lookup != None):
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

    # retrieve full list created
    url_allcats = "http://localhost:5000/api/SecurityControls/filterSecurityControlsByCatalogue/" + str(intCat)

    allcats = requests.request(
    "GET",
    url_allcats,
    headers=headers,
    )
    catsArray = allcats.json()

    # loop through and compare arrays, see if anything is missing (validation check)
    intMatch = 0
    for y in upload:
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
    else:
        print("ERROR: Some controls were not created successfully.")




