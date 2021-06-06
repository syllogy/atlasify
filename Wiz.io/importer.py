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
url_login = "https://atlas-dev.c2labs.com/api/authentication/login"

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

#loop through issues and see which ones relate to NIST CSF
intLoop = 0
intL1 = 0
intL2 = 0
intL3 = 0
atlasityIssues = []
for iss in wizIssueList:
    #get the record based on control ID
    found = list(filter(lambda x: x["id"] == iss["controlId"], wizControls))
    #get first item in the list
    found = found[0]
    #see if it has a corresponding NIST CSF ID (ignore others)
    if (found["nist-csf-id"] != ""):
        # increment counter for number of issues
        intLoop += 1
        # create an issue
        atlasityIssueModel = {
            "id": 0,
            "uuid": '',
            "title": '',
            "description": '',
            "severityLevel": '',
            "issueOwnerId": userId,
            "orgId": None,
            "facilityId": None,
            "costEstimate": 0,
            "dueDate": None,
            "identification": 'Security Control Assessment',
            "sourceReport": '',
            "status": 'Open',
            "dateCompleted": None,
            "createdById": userId,
            "dateCreated": None,
            "lastUpdatedById": userId,
            "dateLastUpdated": '',
            "parentId": intPlan,
            "parentModule": 'securityplans'
        }
        #map attributes to the issue
        atlasityIssueModel["title"] = iss["entityName"] + " - " + iss["controlName"]
        atlasityIssueModel["description"] = "Wiz Control ID: " + iss["controlId"] + "<br/>"
        atlasityIssueModel["description"] += "First Detected: " + iss["createdAt"] + "<br/>"
        atlasityIssueModel["description"] += "Last Scanned: " + iss["updatedAt"] + "<br/>"
        atlasityIssueModel["description"] += "Wiz Severity: " + iss["severity"] + "<br/>"
        atlasityIssueModel["description"] += "Wiz Entity ID: " + iss["entityId"] + "<br/>"
        atlasityIssueModel["description"] += "Wiz Entity Type: " + iss["entityType"] + "<br/>"
        if iss["ticketId"] != '':
            atlasityIssueModel["description"] += "Jira Ticket #: " + iss["ticketId"] + "<br/>"
        if iss["ticketURL"] != '':
            atlasityIssueModel["description"] += "Jira Ticket URL: " + iss["ticketURL"] + "<br/>"
        atlasityIssueModel["sourceReport"] = "Wiz.io Issue #: " + iss["id"]
        #status mapping
        if iss["severity"] == 'CRITICAL':
            atlasityIssueModel["dueDate"] = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%m/%d/%Y")
            atlasityIssueModel["severityLevel"] = "I - High - Significant Deficiency"
            intL1 += 1
        elif iss["severity"] == "HIGH":
            atlasityIssueModel["dueDate"] = (datetime.date.today() + datetime.timedelta(days=90)).strftime("%m/%d/%Y")
            atlasityIssueModel["severityLevel"] = "II - Moderate - Reportable Condition"
            intL2 += 1
        else:
            atlasityIssueModel["dueDate"] = (datetime.date.today() + datetime.timedelta(days=365)).strftime("%m/%d/%Y")
            atlasityIssueModel["severityLevel"] = "III - Low - Other Weakness"
            intL3 += 1
        # add to the list
        atlasityIssues.append(atlasityIssueModel)

# output the result
print(Logger.OK + "SUCCESS: " + str(intLoop) + " issues related to NIST CSF were identified." + Logger.END)
print(Logger.OK + "SUCCESS: " + str(intL1) + " Level 1 issues related to NIST CSF were identified." + Logger.END)
print(Logger.OK + "SUCCESS: " + str(intL2) + " Level 2 issues related to NIST CSF were identified." + Logger.END)
print(Logger.OK + "SUCCESS: " + str(intL3) + " Level 3 issues related to NIST CSF were identified." + Logger.END)

# loop through Atlasity issues
url_issues = "http://localhost:5000/api/issues"
for iss in atlasityIssues:
    if iss["severityLevel"] == "I - High - Significant Deficiency":
        # create the control
        try:
            response = requests.request("POST", url_issues, headers=headers, json=iss)
            scJsonResponse = response.json()
            print(Logger.OK + "Success - " + str(scJsonResponse["id"]) + Logger.END)
        except requests.exceptions.HTTPError as errh:
            print (Logger.ERROR + "Http Error:", errh  + Logger.END)
        except requests.exceptions.ConnectionError as errc:
            print (Logger.ERROR + "Error Connecting:", errc + Logger.END)
        except requests.exceptions.Timeout as errt:
            print (Logger.ERROR + "Timeout Error:",errt + Logger.END)
        except requests.exceptions.RequestException as err:
            print (Logger.ERROR + "OOps: Something Else", err + Logger.END)

#artifacts for troubleshooting/verifications
with open("wiz-results/frameworkList.json", "w") as outfile: 
    outfile.write(json.dumps(frameworks, indent=4)) 
with open("wiz-results/consolidatedFrameworks.json", "w") as outfile: 
    outfile.write(json.dumps(ctrlList, indent=4)) 
with open("wiz-results/wizControls.json", "w") as outfile: 
    outfile.write(json.dumps(wizControls, indent=4)) 
with open("wiz-results/wizIssues.json", "w") as outfile: 
    outfile.write(json.dumps(wizIssueList, indent=4)) 
with open("wiz-results/atlasityIssues.json", "w") as outfile: 
    outfile.write(json.dumps(atlasityIssues, indent=4)) 

