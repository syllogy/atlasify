#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse
import datetime

class Logger:
    OK = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'

# setup parser for command line arguments
parser = argparse.ArgumentParser(description='Atlasity parser for Wiz.io')
parser.add_argument('--user', metavar='path', type=str, help='Atlasity username')
parser.add_argument('--pwd', metavar='path', type=str, help='Atlasity password')
parser.add_argument('--planID', metavar='path', type=str, help='Security Plan ID # in Atlasity')

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
if (args.planID == ''):
    print('ERROR: No security plan ID # provided.')
    exit
else:
    intPlan = args.planID

# login to your Atlasity instance
url_login = "http://atlas-dev.c2labs.com/api/authentication/login"

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

# master list of controls
ctrlList = []

# get all security controls for the plan provided
url_getPlans = "https://atlas-dev.c2labs.com/api/controlImplementation/getAllByPlan/" + intPlan
responseSC = requests.request("GET", url_getPlans, headers=headers)
scDict = json.loads(responseSC.text)

#loop through the security controls
for sc in scDict:
    # new model for controls
    ctrlModel = {
        "atlasID": 0,
        "title": '',
        "wizID": '',
        "wizParentID": '',
        "wizParentName": ''
    }
    ctrlModel["atlasID"] = sc["id"]
    ctrlModel["title"] = sc["controlTitle"]
    ctrlList.append(ctrlModel)

#loop through the NIST CSF controls
nistCSF = open('wiz-results/frameworks_result_file.json', 'r', encoding='utf-8-sig')
nistCSFData = json.load(nistCSF)

#loop through the Wiz security controls
for sc in nistCSFData["securityFrameworks"]["nodes"]:
    if sc["name"] == 'NIST CSF':
        for cat in sc["categories"]:
            parentName = cat["name"]
            parentID = cat["id"]
            # get the substring with just the abbreviation between parenthesis
            intStart = cat["name"].index('(') + 1
            intEnd = cat["name"].index(')')
            subStringID = cat["name"][intStart:intEnd]
            # get subcategory controls
            for subCat in cat["subCategories"]:
                wizID = subCat["id"]
                lookupID = subStringID + '-' + subCat["externalId"]
                bCTRLMatch = False
                for item in ctrlList:
                    if item["title"].startswith(lookupID) == True:
                        item["wizID"] = wizID
                        item["wizParentID"] = parentID
                        item["wizParentName"] = parentName
                        bCTRLMatch = True
                if (bCTRLMatch == False):
                    print (Logger.ERROR + "OOps: " + lookupID + " not found." + Logger.END)

#output consolidated list
#for item in ctrlList:
    #print(item)

# get the control results
wizCTRLS = open('wiz-results/controls_result_file.json', 'r', encoding='utf-8-sig')
wisCTRLSData = json.load(wizCTRLS)

#loop through the Wiz controls
wizControls = []
for sc in wisCTRLSData["controls"]["nodes"]:
    # new model for controls
    wizCTRLModel = {
        "id": 0,
        "name": '',
        "description": '',
        "type": '',
        "severity": ''
    }
    # map fields
    wizCTRLModel["id"] = sc["id"]
    wizCTRLModel["name"] = sc["name"]
    wizCTRLModel["description"] = sc["description"]
    wizCTRLModel["type"] = sc["type"]
    wizCTRLModel["severity"] = sc["severity"]
    wizControls.append(wizCTRLModel)

#output Wiz controls
for item in wizControls:
    print(item["id"] + ": " + item["name"])

#artifacts for troubleshooting/verifications
with open("wiz-results/consolidatedFrameworks.json", "w") as outfile: 
    outfile.write(json.dumps(ctrlList, indent=4)) 
with open("wiz-results/wizControls-flat.json", "w") as outfile: 
    outfile.write(json.dumps(wizControls, indent=4)) 

