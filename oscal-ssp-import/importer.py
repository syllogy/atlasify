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
    "ParentId": 49,
    "ParentModule": "securityplans",
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
ssp["Description"] += "<h4>System Metadata</h4>"
ssp["Description"] += "Version: " + meta["version"] + "<br/>"
ssp["Description"] += "Imported Using OSCAL Version: " + meta["oscal-version"] + "<br/>"
ssp["Description"] += "Remarks: " + meta["remarks"] + "<br/>"
# get the properties
props = meta["properties"]
ssp["Description"] += "<h4>System Properties</h4>"
for i in props:
    ssp["Description"] += i["name"] + ": " + i["value"]
# get the revision history
hist = meta["revision-history"]
ssp["Description"] += "<h4>Revision History</h4>"
for i in hist:
    ssp["Description"] += "Version: " + i["version"] + ", Date Published: " + i["published"] + ", OSCAL Version: " + i["oscal-version"] + ", Remarks: " + i["remarks"] + "<br/>"
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
ssp["Description"] += "<h4>OSCAL Profile</h4>"
for i in prof:
    ssp["Description"] += "Imported: " + prof["href"] + "<br/>"

#############################################################################################
# SYSTEM CHARACTERISTICS
#############################################################################################
chars = L1["system-characteristics"]
otherIDs = chars["system-ids"]
intLoop = 0
for i in otherIDs:
    if intLoop != 0:
        ssp["OtherIdentifier"] += ", "
    ssp["OtherIdentifier"] +=  i["id"]
    intLoop += 1
# process properties
scProps = chars["properties"]
ssp["Description"] += "<h4>System Properties</h4>"
for i in scProps:
    ssp["Description"] += i["name"] + ": " + i["value"] + "<br/>"
# process annotations
scAnn = chars["annotations"]
ssp["Description"] += "<h4>System Annotations</h4>"
for i in scAnn:
    ssp["Description"] += i["name"] + ": " + i["value"] + " (Remarks: " + i["remarks"]  + ")<br/>"
# process system information
scInfo = chars["system-information"]
scInfoProps = scInfo["properties"]
ssp["Description"] += "<h4>System Sensitivity and Privacy</h4>"
ssp["Description"] += "Security Sensitivity Level: " + chars["security-sensitivity-level"] + "<br/>"
for i in scInfoProps:
    if "class" in i:
        ssp["Description"] += i["name"] + ": " + i["value"] + "(Class: " + i["class"] + ")<br/>"
    else:
        ssp["Description"] += i["name"] + ": " + i["value"] + "<br/>"
# process information types
scInfoTypes = scInfo["information-types"]
ssp["Description"] += "<h4>Information Types and System Classification</h4>"
for i in scInfoTypes:
    ssp["Description"] += "Type: " + i["title"] + "(GUID: " + i["uuid"] + ")<br/>"
    ssp["Description"] += "Description: " + i["description"] + "<br/>"
    ssp["Description"] += "InfoType ID (From - https://doi.org/10.6028/NIST.SP.800-60v2r1): " + i["information-type-ids"]["https://doi.org/10.6028/NIST.SP.800-60v2r1"]["id"] + "<br/>"
    ssp["Description"] += "Confidentiality Impact - Base: " + i["confidentiality-impact"]["base"] + ", Selected: " + i["confidentiality-impact"]["selected"]  + "<br/>"
    ssp["Description"] += "Integrity Impact - Base: " + i["integrity-impact"]["base"] + ", Selected: " + i["integrity-impact"]["selected"]  + "<br/>"
    ssp["Description"] += "Availability Impact - Base: " + i["availability-impact"]["base"] + ", Selected: " + i["availability-impact"]["selected"]  + "<br/>"
# process security impact level
scLevels = chars["security-impact-level"]
ssp["Description"] += "<h4>Security Impact Levels</h4>"
if scLevels["security-objective-confidentiality"] == "fips-199-high":
    ssp["Confidentiality"] = "High"
elif scLevels["security-objective-confidentiality"] == "fips-199-moderate":
    ssp["Confidentiality"] = "Moderate"
else:
    ssp["Confidentiality"] = "Low"
if scLevels["security-objective-integrity"] == "fips-199-high":
    ssp["Integrity"] = "High"
elif scLevels["security-objective-integrity"] == "fips-199-moderate":
    ssp["Integrity"] = "Moderate"
else:
    ssp["Integrity"] = "Low"
if scLevels["security-objective-availability"] == "fips-199-high":
    ssp["Availability"] = "High"
elif scLevels["security-objective-availability"] == "fips-199-moderate":
    ssp["Availability"] = "Moderate"
else:
    ssp["Availability"] = "Low"
#get overall categorization using the system high approach
if ssp["Confidentiality"] == "High" or ssp["Integrity"] == "High" or ssp["Availability"] == "High":
    ssp["OverallCategorization"] = "High"
elif ssp["Confidentiality"] == "Moderate" or ssp["Integrity"] == "Moderate" or ssp["Availability"] == "Moderate":
    ssp["OverallCategorization"] = "Moderate"
else:
    ssp["OverallCategorization"] = "Low"
# get the status
stat = chars["status"]
if stat["state"] == "operational":
    ssp["Status"] = "Operational"
else:
    ssp["Status"] = "Under Development"
# process authorization boundary, network architecture, and data flow
authb = chars["authorization-boundary"]
ssp["AuthorizationBoundary"] += authb["description"]
netx = chars["network-architecture"]
ssp["NetworkArchitecture"] += netx["description"]
df = chars["data-flow"]
ssp["DataFlow"] += df["description"]

#############################################################################################
# SYSTEM IMPLEMENTATION
#############################################################################################
imps = L1["system-implementation"]
# process properties
impProps = imps["properties"]
ssp["Environment"] += "<h4>System Properties</h4>"
for i in impProps:
    ssp["Environment"] += i["name"] + ": " + i["value"] + "<br/>"
# process users
scUsers = imps["users"]
ssp["Environment"] += "<h4>Users</h4>"
userTable = "<table border=\"1\"><tr><td>User</td><td>Properties</td><td>Roles</td><td>Privileges</td></tr>"
for i in scUsers:
    # get the user
    userTable += "<tr>"
    scUser = scUsers[i]
    userTable += "<td>" + scUser["title"] + " (GUID: " + i + ")</td>"
    # get user properties
    strUserProp = "<td>"
    scUserProps = scUser["properties"]
    for i in scUserProps:
        strUserProp += i["name"] + ": " + i["value"] + "<br/>"
    scUserAnno = scUser["annotations"]
    for i in scUserAnno:
        strUserProp += i["name"] + ": " + i["value"] + "<br/>"
    strUserProp += "</td>"
    userTable += strUserProp
    # get user roles
    scRoles = scUser["role-ids"]
    strUserRoles = "<td>"
    for i in scRoles:
        strUserRoles += i + "<br/>"
    strUserRoles += "</td>"
    userTable += strUserRoles
    # get privileges
    scPrivs = scUser["authorized-privileges"]
    strPrivs = "<td>"
    for i in scPrivs:
        strPrivs += i["title"] + ", including the following functions: <br/>"
        scFunctions = i["functions-performed"]
        for x in scFunctions:
            strPrivs += "- " + x + "<br/>"
    strPrivs += "</td>"
    userTable += strPrivs
    #close the row
    userTable += "</tr>"
#close the table
userTable += "</table><br/>"
ssp["Environment"] += userTable
print(ssp["Environment"])

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
#print("Raw SSP JSON")
#print(ssp["Description"])
#print(ssp)
