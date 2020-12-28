#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse

# setup parser for command line arguments
parser = argparse.ArgumentParser(description='Atlasity parser for NIST 800-53 OSCAL')
parser.add_argument('--user', metavar='path', type=str, help='Atlasity username')
parser.add_argument('--pwd', metavar='path', type=str, help='Atlasity password')

# get the argument from the command line
args = parser.parse_args()
if (args.user == ''):
    print('ERROR: No username provided.')
else:
    strUser = args.user
if (args.pwd == ''):
    print('ERROR: No password provided.')
else:
    strPWD = args.pwd

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

# load the OSCAL SSP JSON
oscal = open('ssp_v1_oscal_json.json', 'r', encoding='utf-8-sig')
oscalData = json.load(oscal)

# create the ssp object
ssp = {
    "UUID": "",
    "SystemName": "",
    "PlanInformationSystemSecurityOfficerId": "",
    "PlanAuthorizingOfficialId": "",
    "SystemOwnerId": "",
    "OtherIdentifier": "",
    "Confidentiality": "",
    "Integrity": "",
    "Availability": "",
    "Status": "",
    "Description": "",
    "DateSubmitted": None,
    "ApprovalDate": None,
    "ExpirationDate": None,
    "SystemType": "",
    "Environment": "",
    "LawsAndRegulations": "",
    "AuthorizationBoundary": "",
    "NetworkArchitecture": "",
    "DataFlow": "",
    "OverallCategorization": "",
    "FacilityId": None,
    "ParentId": 0,
    "ParentModule": "",
    "CreatedById": userId,
    "DateCreated": None,
    "LastUpdatedById": userId,
    "DateLastUpdated": None,
    "Users": 0,
    "PrivilegedUsers": 0,
    "UsersMFA": 0,
    "PrivilegedUsersMFA": 0,
    "HVA": False,
    "ProcessLevel": "",
    "PracticeLevel": "",
    "cmmcLevel": "",
    "cmmcStatus": "",
}

# begin processing OSCAL data and get the level 1 data
L1 = oscalData["system-security-plan"]

# get the UUID provided
ssp["UUID"] = L1["uuid"]

#############################################################################################
# METADATA SECTION
#############################################################################################
meta = L1["metadata"]
ssp["SystemName"] = meta["title"]
ssp["DateCreated"] = meta["published"]
ssp["DateLastUpdated"] = meta["last-modified"]
ssp["Description"] += "Version: " + meta["version"] + "<br/>"
ssp["Description"] += "Imported Using OSCAL Version: " + meta["oscal-version"] + "<br/>"
ssp["Description"] += "Remarks: " + meta["remarks"] + "<br/>"
# get the properties
props = meta["properties"]
ssp["Description"] += "<h4>System Properties</h4>"
for i in props:
    ssp["Description"] += "Property Name: " + i["name"] + ", Property Value: " + i["value"]
# get the revision history
hist = meta["revision-history"]
ssp["Description"] += "<h4>Revision History</h4>"
for i in hist:
    ssp["Description"] += "Version: " + i["version"] + ", Date Published: " + i["published"] + ", OSCAL Version: " + i["oscal-version"] + ", Remarks: " + i["remarks"]
# get the roles
roles = meta["roles"]
ssp["Description"] += "<h4>Relevant Roles for this SSP</h4>"
for i in roles:
    if "desc" in i:
        ssp["Description"] += i["title"] + "(ID: " + i["id"] + ") - " + i["desc"] + "<br/>"
    else:
        ssp["Description"] += i["title"] + "(ID: " + i["id"] + ") - no description provided.<br/>"
# create a dictionary for locations
locations = meta["locations"]

#############################################################################################
# PROFILE SECTION
#############################################################################################
prof = L1["import-profile"]
ssp["Description"] += "OSCAL Profile Imported: " + i["href"] + "<br/>"

#############################################################################################
# SYSTEM CHARACTERISTICS
#############################################################################################
chars = L1["system-characteristics"]

#############################################################################################
# SYSTEM IMPLEMENTATION
#############################################################################################
imps = L1["system-implementation"]

#############################################################################################
# CONTROL IMPLEMENTATION
#############################################################################################
ctrls = L1["control-implementation"]

#############################################################################################
# BACK MATTER SECTION
#############################################################################################
back = L1["back-matter"]
resources = back["resources"]
ssp["Description"] += "<h4>Back Matter and Related Resources</h4>"
resourceTable = "<table border=\"1\"><tr><td>UUID</td><td>Title</td><td>Description</td><td>Properties</td><td>Links</td><td>Attachments</td><td>Remarks</td></tr>"
for i in resources:
    resourceTable += "<tr>"
    if "uuid" in i:
        resourceTable += "<td>" + i["uuid"] + "</td>"
    else:
        resourceTable += "<td>N/A</td>"
    if "title" in i:
        resourceTable += "<td>" + i["title"] + "</td>"
    else:
        resourceTable += "<td>N/A</td>"
    if "desc" in i:
        resourceTable += "<td>" + i["desc"] + "</td>"
    else:
        resourceTable += "<td>N/A</td>"
    if "properties" in i:
        zProps = ""
        for z in i["properties"]:
            zProps += z["name"] + ": " + z["value"] + "<br/>"
        resourceTable += "<td>" + zProps + "</td>"
    else:
        resourceTable += "<td>N/A</td>"
    if "rlinks" in i:
        zLinks = ""
        for z in i["rlinks"]:
            zLinks += z["href"] + "<br/>"
        resourceTable += "<td>" + zLinks + "</td>"
    else:
        resourceTable += "<td>N/A</td>"
    if "attachments" in i:
        zATT = ""
        for z in i["attachments"]:
            zATT += z["value"] + "<br/>"
        resourceTable += "<td>" + zATT + "</td>"
    else:
        resourceTable += "<td>N/A</td>"
    if "remarks" in i:
        resourceTable += "<td>" + i["remarks"] + "</td>"
    else:
        resourceTable += "<td>N/A</td>"
    resourceTable += "</tr>"
resourceTable += "</table><br/>"
ssp["Description"] += resourceTable

# print the SSP results
print("Raw SSP JSON")
print(ssp)

