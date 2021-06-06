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
# master list of frameworks
frameworks = []

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
    #process NIST CSF
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
    #full mapping to build framework list
    fwkModel = {
        "id": sc["id"],
        "name": sc["name"]
    }
    frameworks.append(fwkModel)

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
        "severity": '',
        "nist-csf-id": '',
        "cis-aws-120-id": '',
        "pci-dss-id": '',
        "hipaa-id": '',
        "cis-aws-130-id": '',
        "nist-800-171-id": '',
        "gdpr-id": '',
        "wiz-id": '',
        "cis-71-id": '',
        "iso-27001-id": '',
        "cis-gcp-110-id": ''
    }

    # map fields
    wizCTRLModel["id"] = sc["id"]
    wizCTRLModel["name"] = sc["name"]
    wizCTRLModel["description"] = sc["description"]
    wizCTRLModel["type"] = sc["type"]
    wizCTRLModel["severity"] = sc["severity"]

    # evaluate frameworks to map
    for scat in sc["securitySubCategories"]:
        # match NIST CSF
        if scat["category"]["framework"]["id"] == "wf-id-13":
            wizCTRLModel["nist-csf-id"]= scat["category"]["id"]
        # match CIS AWS 1.2.0
        if scat["category"]["framework"]["id"] == "wf-id-6":
            wizCTRLModel["cis-aws-120-id"]= scat["category"]["id"]
        # match PCI DSS
        if scat["category"]["framework"]["id"] == "wf-id-12":
            wizCTRLModel["pci-dss-id"]= scat["category"]["id"]
        # match HIPAA
        if scat["category"]["framework"]["id"] == "wf-id-2":
            wizCTRLModel["hipaa-id"]= scat["category"]["id"]
        # match CIS AWS 1.3.0
        if scat["category"]["framework"]["id"] == "wf-id-7":
            wizCTRLModel["cis-aws-130-id"]= scat["category"]["id"]
        # match NIST 800-171
        if scat["category"]["framework"]["id"] == "wf-id-21":
            wizCTRLModel["nist-800-171-id"]= scat["category"]["id"]
        # match GDPR
        if scat["category"]["framework"]["id"] == "wf-id-10":
            wizCTRLModel["gdpr-id"]= scat["category"]["id"]
        # match Wiz
        if scat["category"]["framework"]["id"] == "wf-id-1":
            wizCTRLModel["wiz-id"]= scat["category"]["id"]
        # match CIS Control v7.1
        if scat["category"]["framework"]["id"] == "wf-id-17":
            wizCTRLModel["cis-71-id"]= scat["category"]["id"]
        # match ISO/IEC 27001
        if scat["category"]["framework"]["id"] == "wf-id-3":
            wizCTRLModel["iso-27001-id"]= scat["category"]["id"]
        # match CIS GCP 1.1.0
        if scat["category"]["framework"]["id"] == "wf-id-9":
            wizCTRLModel["cis-gcp-110-id"]= scat["category"]["id"]

    #add to the array
    wizControls.append(wizCTRLModel)

# get the Wiz issues
wizISS = open('wiz-results/issues_result_file.json', 'r', encoding='utf-8-sig')
wisIssues = json.load(wizISS)

#loop through the Wiz issues
wizIssueList = []
for iss in wisIssues["issues"]["nodes"]:
    # new model for issues
    wizIssueModel = {
        "id": 0,
        "controlId": '',
        "controlName": '',
        "createdAt": '',
        "updatedAt": '',
        "status": '',
        "severity": '',
        "entityId": '',
        "entityName": '',
        "entityType": '',
        "ticketId": '',
        "ticketURL": ''
    }
    #map the fields
    wizIssueModel["id"] = iss["id"]
    wizIssueModel["createdAt"] = iss["createdAt"]
    wizIssueModel["updatedAt"] = iss["updatedAt"]
    wizIssueModel["status"] = iss["status"]
    wizIssueModel["severity"] = iss["severity"]
    if not iss["control"] is None:
        if "control" in iss:
            wizIssueModel["controlId"] = iss["control"]["id"]
            wizIssueModel["controlName"] = iss["control"]["name"]
    if not iss["entity"] is None:
        if "entity" in iss:
            wizIssueModel["entityId"] = iss["entity"]["id"]
            wizIssueModel["entityName"] = iss["entity"]["name"]
            wizIssueModel["entityType"] = iss["entity"]["type"]
    if not iss["serviceTicket"] is None:
        if "name" in iss["serviceTicket"]:
            wizIssueModel["ticketId"] = iss["serviceTicket"]["name"]
        if "url" in iss["serviceTicket"]:
            wizIssueModel["ticketURL"] = iss["serviceTicket"]["url"]
    wizIssueList.append(wizIssueModel)

#artifacts for troubleshooting/verifications
with open("wiz-results/frameworkList.json", "w") as outfile: 
    outfile.write(json.dumps(frameworks, indent=4)) 
with open("wiz-results/consolidatedFrameworks.json", "w") as outfile: 
    outfile.write(json.dumps(ctrlList, indent=4)) 
with open("wiz-results/wizControls.json", "w") as outfile: 
    outfile.write(json.dumps(wizControls, indent=4)) 
with open("wiz-results/wizIssues.json", "w") as outfile: 
    outfile.write(json.dumps(wizIssueList, indent=4)) 

