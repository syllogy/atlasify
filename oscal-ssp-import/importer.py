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
parser = argparse.ArgumentParser(description='Atlasity parser for NIST 800-53 OSCAL')
parser.add_argument('--user', metavar='path', type=str, help='Atlasity username')
parser.add_argument('--pwd', metavar='path', type=str, help='Atlasity password')
parser.add_argument('--catalog', metavar='path', type=str, help='Atlasity catalog containing security controls for this SSP')

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
if (args.catalog == ''):
    print('ERROR: No catalog provided.')
    exit
else:
    intCatalog = args.catalog

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

# get the list of controls for this catalog
url_cats = "http://localhost:5000/api/SecurityControls/filterSecurityControlsByCatalogue/" + intCatalog
responseCats = requests.request("GET", url_cats, headers=headers)
scDict = json.loads(responseCats.text)

# load the OSCAL SSP JSON
oscal = open('GovReady/govready-ssp-oscal-01.json', 'r', encoding='utf-8-sig')
#oscal = open('GovReady/govready-ssp-oscal-cmpt-ubuntu-16.04-ac-10-01.json', 'r', encoding='utf-8-sig')
#oscal = open('GovReady/govready-ssp-ubuntu-16.04-lts-oscal.json', 'r', encoding='utf-8-sig')
oscalData = json.load(oscal)

# create the ssp object schema for Atlasity
ssp = {
    "UUID": "",
    "SystemName": "",
    "PlanInformationSystemSecurityOfficerId": userId,
    "PlanAuthorizingOfficialId": userId,
    "SystemOwnerId": userId,
    "OtherIdentifier": "",
    "Confidentiality": "",
    "Integrity": "",
    "Availability": "",
    "Status": "",
    "Description": "",
    "DateSubmitted": None,
    "ApprovalDate": None,
    "ExpirationDate": None,
    "SystemType": "General Support System",
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
if "published" in meta:
    ssp["DateCreated"] = meta["published"]
else:
    ssp["DateCreated"] = datetime.date.today().strftime("%m/%d/%Y")
ssp["DateLastUpdated"] = meta["last-modified"]
ssp["Description"] += "<h4>System Metadata</h4>"
ssp["Description"] += "Version: " + meta["version"] + "<br/>"
ssp["Description"] += "Imported Using OSCAL Version: " + meta["oscal-version"] + "<br/>"
if "remarks" in meta:
    ssp["Description"] += "Remarks: " + meta["remarks"] + "<br/>"
# get the properties
if "properties" in meta:
    props = meta["properties"]
    ssp["Description"] += "<br/><h4>System Properties</h4>"
    for i in props:
        ssp["Description"] += i["name"] + ": " + i["value"] + "<br/>"
# get the revision history
if "revision-history" in meta:
    hist = meta["revision-history"]
    ssp["Description"] += "<br/><h4>Revision History</h4>"
    for i in hist:
        ssp["Description"] += "Version: " + i["version"] + ", Date Published: " + i["published"] + ", OSCAL Version: " + i["oscal-version"] + ", Remarks: " + i["remarks"] + "<br/>"
# get the roles
if "roles" in meta:
    roles = meta["roles"]
    ssp["Description"] += "<br/><h4>Relevant Roles for this SSP</h4>"
    for i in roles:
        if "desc" in i:
            ssp["Description"] += i["title"] + "(ID: " + i["id"] + ") - " + i["desc"] + "<br/>"
        else:
            ssp["Description"] += i["title"] + "(ID: " + i["id"] + ") - no description provided.<br/>"
# create a dictionary for locations
if "locations" in meta:
    locations = meta["locations"]

#############################################################################################
# PROFILE SECTION
#############################################################################################
prof = L1["import-profile"]
ssp["Description"] += "<br/><h4>OSCAL Profile</h4>"
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
# get system descriptions
ssp["Description"] += chars["description"] + "<br/><br/>" + ssp["Description"]
# overall categorization
ssp["OverallCategorization"] = chars["security-sensitivity-level"]
# process properties
if "properties" in chars:
    scProps = chars["properties"]
    if (len(scProps) > 0):
        ssp["Description"] += "<br/><h4>System Properties</h4>"
        for i in scProps:
            ssp["Description"] += i["name"] + ": " + i["value"] + "<br/>"
# process annotations
if "annotations" in chars:
    scAnn = chars["annotations"]
    if (len(scAnn) > 0):
        ssp["Description"] += "<br/><h4>System Annotations</h4>"
        for i in scAnn:
            ssp["Description"] += i["name"] + ": " + i["value"] + " (Remarks: " + i["remarks"]  + ")<br/>"
# process system information
scInfo = chars["system-information"]
if "properties" in scInfo:
    scInfoProps = scInfo["properties"]
    ssp["Description"] += "<br/><h4>System Sensitivity and Privacy</h4>"
    ssp["Description"] += "Security Sensitivity Level: " + chars["security-sensitivity-level"] + "<br/>"
    for i in scInfoProps:
        if "class" in i:
            ssp["Description"] += i["name"] + ": " + i["value"] + "(Class: " + i["class"] + ")<br/>"
        else:
            ssp["Description"] += i["name"] + ": " + i["value"] + "<br/>"
# process information types
scInfoTypes = scInfo["information-types"]
ssp["Description"] += "<br/><h4>Information Types and System Classification</h4>"
for i in scInfoTypes:
    if "uuid" in i:
        ssp["Description"] += "Type: " + i["title"] + "(GUID: " + i["uuid"] + ")<br/>"
    else:
        ssp["Description"] += "Type: " + i["title"] + "<br/>"
    ssp["Description"] += "Description: " + i["description"] + "<br/>"
    ssp["Description"] += "Confidentiality Impact - Base: " + i["confidentiality-impact"]["base"] + "<br/>"
    ssp["Description"] += "Integrity Impact - Base: " + i["integrity-impact"]["base"] + "<br/>"
    ssp["Description"] += "Availability Impact - Base: " + i["availability-impact"]["base"] + "<br/>"
# process security impact level
scLevels = chars["security-impact-level"]
if scLevels["security-objective-confidentiality"] == "fips-199-high":
    ssp["Confidentiality"] = "High"
elif scLevels["security-objective-confidentiality"] == "fips-199-moderate":
    ssp["Confidentiality"] = "Moderate"
elif scLevels["security-objective-confidentiality"] == "fips-199-low":
    ssp["Confidentiality"] = "Low"
else:
    ssp["Confidentiality"] = ssp["OverallCategorization"]
if scLevels["security-objective-integrity"] == "fips-199-high":
    ssp["Integrity"] = "High"
elif scLevels["security-objective-integrity"] == "fips-199-moderate":
    ssp["Integrity"] = "Moderate"
elif scLevels["security-objective-integrity"] == "fips-199-low":
    ssp["Integrity"] = "Low"
else:
    ssp["Integrity"] = ssp["OverallCategorization"]
if scLevels["security-objective-availability"] == "fips-199-high":
    ssp["Availability"] = "High"
elif scLevels["security-objective-availability"] == "fips-199-moderate":
    ssp["Availability"] = "Moderate"
elif scLevels["security-objective-availability"] == "fips-199-low":
    ssp["Availability"] = "Low"
else:
    ssp["Availability"] = ssp["OverallCategorization"]
# get the status
stat = chars["status"]
if stat["state"] == "operational":
    ssp["Status"] = "Operational"
else:
    ssp["Status"] = "Under Development"
# process authorization boundary, network architecture, and data flow
authb = chars["authorization-boundary"]
ssp["AuthorizationBoundary"] += authb["description"]
if "network-architecture" in chars:
    netx = chars["network-architecture"]
    ssp["NetworkArchitecture"] += netx["description"]
if "data-flow" in chars:
    df = chars["data-flow"]
    ssp["DataFlow"] += df["description"]

#############################################################################################
# SYSTEM IMPLEMENTATION
#############################################################################################
imps = L1["system-implementation"]
# process properties
if "props" in imps:
    impProps = imps["props"]
    ssp["Environment"] += "<br/><h4>System Properties</h4>"
    for i in impProps:
        if "value" in i:
            ssp["Environment"] += i["name"] + ": " + i["value"] + "<br/>"
        else:     
            ssp["Environment"] += i["name"] + "<br/>"

# process users
scUsers = imps["users"]
ssp["Environment"] += "<br/><h4>Users</h4>"
userTable = "<table border=\"1\" style=\"width: 100%;\"><tr style=\"font-weight: bold\"><td>User</td><td>Properties</td><td>Roles</td><td>Privileges</td></tr>"
for i in scUsers:
    # get the user
    userTable += "<tr>"
    scUser = scUsers[i]
    userTable += "<td>" + scUser["title"] + " (GUID: " + i + ")</td>"
    # get user properties
    strUserProp = "<td>"
    if "props" in scUser:
        scUserProps = scUser["props"]
        for i in scUserProps:
            strUserProp += i["name"] + ": " + i["value"] + "<br/>"
    if "annotations" in scUser:
        scUserAnno = scUser["annotations"]
        for i in scUserAnno:
            strUserProp += i["name"] + ": " + i["value"] + "<br/>"
    strUserProp += "</td>"
    userTable += strUserProp
    # get user roles
    if "role-ids" in scUser:
        scRoles = scUser["role-ids"]
        strUserRoles = "<td>"
        for i in scRoles:
            strUserRoles += i + "<br/>"
        strUserRoles += "</td>"
    else:
        strUserRoles = "<td></td>"
    userTable += strUserRoles
    # get privileges
    if "authorized-privileges" in scUser:
        scPrivs = scUser["authorized-privileges"]
        strPrivs = "<td>"
        for i in scPrivs:
            strPrivs += i["title"] + ", including the following functions: <br/>"
            scFunctions = i["functions-performed"]
            for x in scFunctions:
                strPrivs += "- " + x + "<br/>"
        strPrivs += "</td>"
    else:
        strPrivs = "<td></td>"
    userTable += strPrivs
    #close the row
    userTable += "</tr>"
#close the table
userTable += "</table><br/>"
ssp["Environment"] += userTable

# process components
scComps = imps["components"]

#create an array to hold the new Atlasity components
atlasityCOMPS = []

# loop through the components
for i in scComps:
    # create the component for Atlasity
    atlComp = {
        "UUID": "",
        "Title": "",
        "Description": "",
        "Purpose": "",
        "ComponentType": "",
        "ComponentOwnerId": userId,
        "SecurityPlansId": 0,
        "Status": "",
        "CreatedById": userId,
        "DateCreated": None,
        "LastUpdatedById": userId,
        "DateLastUpdated": None,
    }  

    # initialize table
    compTable = ""
    
    # get the components info
    atlComp["UUID"] = i
    atlComp["Title"] = scComps[i]["title"]
    atlComp["Description"] = scComps[i]["description"]
    if atlComp["Description"] == "":
        atlComp["Description"] = scComps[i]["title"]
    atlComp["Status"] = scComps[i]["status"]["state"]
    if "remarks" in scComps[i]:
        atlComp["Purpose"] += scComps[i]["remarks"] + "<br/>" 
    if "type" in scComps[i]:
        atlComp["ComponentType"] = scComps[i]["type"]

    # add to the array
    atlasityCOMPS.append(atlComp)

    #process ports and protocols
    strProto = ""
    if "protocols" in scComps[i]:
        compPorts = scComps[i]["protocols"]
        for x in compPorts:
            strProto += "<h3>Ports and Protocols</h3><br/>"
            compTable += "<strong>Name: " + x["name"] + "</strong></br>"
            ranges = x["port-ranges"]
            for y in ranges:
                if y["start"] == y["end"]:
                    compTable += "Transport: " + y["transport"] + ", Port: " + str(y["start"]) + "<br/>"
                else:
                    compTable += "Transport: " + y["transport"] + ", Port Range: " + str(y["start"]) + " - " + str(y["end"]) + "<br/>"
    else:
        compTable += "N/A"
    compTable += "</td><td>"
    #process roles
    if "responsible-roles" in scComps[i]:
        scRoles = scComps["responsible-roles"]
        for i in scRoles:
            compTable += i + "<br/>"
    else:
        compTable += "N/A"
    compTable += "</td><td>"
    #process status
    compTable += scComps[i]["status"]["state"] + "</td>"
    #close the row
    compTable += "</tr>"
#close the table
compTable += "</table><br/>"
ssp["Environment"] += compTable

# process inventory
if "system-inventory"in imps:
    scInvs = imps["system-inventory"]
    scItems = scInvs["inventory-items"]
    ssp["Environment"] += "<br/><h4>System Inventory</h4>"
    invTable = "<table border=\"1\" style=\"width: 100%;\"><tr style=\"font-weight: bold\"><td>ID</td><td>Description</td><td>Properties</td><td>Roles</td><td>Component</td></tr>"
    for i in scItems:
        # get the user
        userTable += "<tr>"
        scItem = scItems[i]
        invTable += "<td>" + scItem["asset-id"] + " (GUID: " + i + ")</td>"
        invTable += "<td>" + scItem["description"]
        if "remarks" in scItem:
            invTable += "<br/>" + scItem["remarks"]
        invTable += "</td>"
        # process properties and annotations
        invTable += "<td>"
        if "properties" in scItem:
            invProps = scItem["properties"]
            for x in invProps:
                if "remarks" in x:
                    invTable += x["name"] + ": " + x["value"] + "(Remarks: " + x["remarks"] + ")<br/>"
                else:
                    invTable += x["name"] + ": " + x["value"] + "<br/>"
            if "annotations" in scItem:
                for x in scItem["annotations"]:
                    if "remarks" in x:
                        invTable += x["name"] + ": " + x["value"] + "(Remarks: " + x["remarks"] + ")<br/>"
                    else:
                        invTable += x["name"] + ": " + x["value"] + "<br/>"
        else:
            invTable += "N/A"
        invTable += "</td><td>"
        #process roles
        if "responsible-parties" in scItem:
            invRoles = scItem["responsible-parties"]
            for i in invRoles:
                invTable += i + "<br/>"
        else:
            invTable += "N/A"
        invTable += "</td><td>"
        #process component
        if "implemented-components" in scItem:
            for z in scItem["implemented-components"]:
                invTable += i + "<br/>"
            invTable += "</td>"
        else:
            invTable += "N/A</td>"
        #close the row
        invTable += "</tr>"
    #close the table
    invTable += "</table><br/>"
    ssp["Environment"] += invTable

#############################################################################################
# BACK MATTER SECTION
#############################################################################################
if "back-matter" in L1:
    back = L1["back-matter"]
    resources = back["resources"]
    ssp["Description"] += "<br/><h4>Back Matter and Related Resources</h4>"
    resourceTable = "<table border=\"1\" style=\"width: 100%;\"><tr style=\"font-weight: bold\"><td>UUID</td><td>Title</td><td>Properties</td><td>Links</td><td>Remarks</td></tr>"
    for i in resources:
        resourceTable += "<tr>"
        if "uuid" in i:
            resourceTable += "<td>" + i["uuid"] + "</td>"
        else:
            resourceTable += "<td>N/A</td>"
        if "title" in i:
            if "desc" in i:
                resourceTable += "<td>" + i["title"] + " - " + i["desc"]  + "</td>"
            else:
                resourceTable += "<td>" + i["title"] + "</td>"
        elif "desc" in i:
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
        #no data right now, commenting out
        # if "attachments" in i:
        #     zATT = ""
        #     for z in i["attachments"]:
        #         zATT += z["value"] + "<br/>"
        #     resourceTable += "<td>" + zATT + "</td>"
        # else:
        #     resourceTable += "<td>N/A</td>"
        if "remarks" in i:
            resourceTable += "<td>" + i["remarks"] + "</td>"
        else:
            resourceTable += "<td>N/A</td>"
        resourceTable += "</tr>"
    resourceTable += "</table><br/>"
    ssp["Description"] += resourceTable

#############################################################################################
# CREATE THE SSP IN ATLASITY
#############################################################################################

# replace bad characters
ssp["Description"] = ssp["Description"].replace("\n", "<br/>")
ssp["Environment"] = ssp["Environment"].replace("\n", "<br/>")

# create the security plan and print success result
url_ssp = "http://localhost:5000/api/securityplans"
response = requests.request("POST", url_ssp, headers=headers, json=ssp)
jsonResponse = response.json()
print("\n\nAtlasity Output\n")
print("\nSecurity Plan ID: " + str(jsonResponse["id"]))
intSecurityPlanID = jsonResponse["id"]

#############################################################################################
# CREATE THE COMPONENTS IN ATLASITY
#############################################################################################

intCompTotal = 0
url_comp = "http://localhost:5000/api/components"
#loop through each component
for xComp in atlasityCOMPS:
    xComp["SecurityPlansId"] = intSecurityPlanID
    response = requests.request("POST", url_comp, headers=headers, json=xComp)
    jsonResponse = response.json()
    if "id" in jsonResponse:
        print("Component: " + str(jsonResponse["id"]) + " - " + xComp["Title"])
        intCompTotal += 1
    else:
        print(xComp)
        print(Logger.ERROR + str(xComp["Title"]) + " component was unable to upload." + Logger.END)

#############################################################################################
# CONTROL IMPLEMENTATION
#############################################################################################
ctrlOBJ = L1["control-implementation"]
ctrls = ctrlOBJ["implemented-requirements"]

#create an array to hold the new Atlasity controls and parameters
atlasityCTRLs = []
atlasityParams = []
#tracking variables
intTotal = 0
intParamTotal = 0
url_sc = "http://localhost:5000/api/controlimplementation"
url_param = "http://localhost:5000/api/parameters"

#loop through the requirements
for i in ctrls:
    bMatch = False
    intAtlasityControl = 0
    intMisses = 0
    #loop through the Atlasity controls to find a match within this catalog
    for x in scDict:
        if x["title"].lower().startswith(i["control-id"]) == True:
            bMatch = True
            print(Logger.OK + "Atlasity " + str(x["id"]) + " - " + x["title"] + " matches OSCAL " + i["control-id"] + Logger.END)
            intAtlasityControl = x["id"]
            break
    #break loop if no match
    if bMatch == False:
        print(Logger.WARNING + i["control-id"] + " has no match" + Logger.END)
        intMisses += 1
        break

    #define Atlasity Control Implementation structure
    ctrlimp = {
        "Id": 0,
        "UUID": "",
        "ControlOwnerId": userId,
        "Policy": "",
        "Implementation": "",
        "Status": "",
        "SecurityPlanID": intSecurityPlanID,
        "DateLastAssessed": None,
        "LastAssessmentResult": "",
        "ControlID": 0,
        "PracticeLevel": "",
        "ProcessLevel": "",
        "ParentID": intSecurityPlanID,
        "ParentModule": "securityplans",
        "CreatedById": userId,
        "DateCreated": None,
        "LastUpdatedById": userId,
        "DateLastUpdated": None,
        "Weight": 0
    }

    # assign the parent control
    ctrlimp["ControlID"] = intAtlasityControl
    ctrlimp["UUID"] = i["uuid"]

    #process statements
    if "statements" in i:
        ciState = i["statements"]
        ctrlimp["Policy"] += "<br/><h4>Statements</h4>"
        for x in ciState:
            st = ciState[x]
            ctrlimp["Policy"] += "<strong>" + x + "</strong><br/>"
            if "uuid" in st:
                ctrlimp["Policy"] += "UUID: " + st["uuid"] + "<br/>"
            if "remarks" in st:
                ctrlimp["Policy"] += "Remarks: " + st["remarks"] + "<br/>"
            if "links" in st:
                ciLinks = st["links"]
                ctrlimp["Policy"] += "<h5>Links</h5>"
                for z in ciLinks:
                    ctrlimp["Policy"] += z["text"]
                    if "rel" in z:
                        ctrlimp["Policy"] += " (Type: " + z["rel"] + ")<br/>"
                    if "href" in z:
                        ctrlimp["Policy"] += " (Link: " + z["href"] + ")<br/>"
            if "by-components" in st:
                ciComps = st["by-components"]
                ctrlimp["Policy"] += "<h5>Components</h5>"
                idvTable = "<table border=\"1\" style=\"width: 100%;\"><tr style=\"font-weight: bold\"><td>Component ID</td><td>UUID</td><td>Description</td><td>Annotations</td></tr>"
                for z in ciComps:
                    idv = ciComps[z]
                    idvTable += "<tr>"
                    idvTable += "<td>" + z + "</td>"
                    idvTable += "<td>" + idv["uuid"] + "</td>"
                    idvTable += "<td>" + idv["description"] 
                    if "remarks" in idv:
                        idvTable += "<br/>" + idv["remarks"] 
                    idvTable += "</td>"
                    if "annotations" in idv:
                        idvAnno = idv["annotations"]
                        idvTable += "<td>"
                        for t in idvAnno:
                            idvTable += t["name"] + ": " + t["value"]
                            if "remarks" in t:
                                idvTable += " (Remarks: " + t["remarks"] + ")"
                        idvTable += "</td>"
                    else:
                        idvTable += "<td>N/A</td>"
                    idvTable += "</tr>"
                idvTable += "</table><br/>"
                ctrlimp["Policy"] += idvTable
    
    #process annotations
    if "annotations" in i:
        ciAnno = i["annotations"]
        ctrlimp["Policy"] += "<br/><h4>Annotations</h4>"
        for x in ciAnno:
            if "remarks" in x:
                ctrlimp["Policy"] += x["name"] + ": " + x["value"] + "(Remarks: " + x["remarks"] + ")<br/>"
            else:
                ctrlimp["Policy"] += x["name"] + ": " + x["value"] + "<br/>"
            #check status
            if x["name"] == "implementation-status":
                if x["value"] == "planned":
                    ctrlimp["Status"] = "Not Implemented"
                elif x["value"] == "partial":
                    ctrlimp["Status"] = "Partially Implemented"
                elif x["value"] == "not-applicable":
                    ctrlimp["Status"] = "Not Applicable"
                elif x["value"] == "implemented":
                    ctrlimp["Status"] = "Fully Implemented"
                else:
                    print("Uknown Control Status: " + x["value"])

    # process properties 
    if "props" in i:
        ciProps = i["props"]
        ctrlimp["Implementation"] += "<br/><h4>Properties</h4>"
        for x in ciProps:
            if "value" in x:
                ctrlimp["Implementation"] += x["name"] + ": " + x["value"] + "<br/>"
            else:
                ctrlimp["Implementation"] += x["name"] + "<br/>"

    # process roles
    if "responsible-roles" in i:
        ciRoles = i["responsible-roles"]
        ctrlimp["Implementation"] += "<br/><h4>Responsible Roles</h4>"
        for x in ciRoles:
            ctrlimp["Implementation"] += x + "<br/>"

    # add to the list to process
    atlasityCTRLs.append(ctrlimp)

    # create the control
    try:
        response = requests.request("POST", url_sc, headers=headers, json=ctrlimp)
        scJsonResponse = response.json()
        print(Logger.OK + "Success - " + str(scJsonResponse["id"]) + Logger.END)
        intControl = scJsonResponse["id"]
        intTotal += 1
    except requests.exceptions.HTTPError as errh:
        print (Logger.ERROR + "Http Error:", errh  + Logger.END)
    except requests.exceptions.ConnectionError as errc:
        print (Logger.ERROR + "Error Connecting:", errc + Logger.END)
    except requests.exceptions.Timeout as errt:
        print (Logger.ERROR + "Timeout Error:",errt + Logger.END)
    except requests.exceptions.RequestException as err:
        print (Logger.ERROR + "OOps: Something Else", err + Logger.END)


#############################################################################################
# CREATE THE PARAMETERS IN ATLASITY
#############################################################################################

    # process parameters
    if "parameter-settings" in i:
        ciParams = i["parameter-settings"]
        for x in ciParams:
            ctrlparam = {
                "Id": 0,
                "UUID": "",
                "Name": "",
                "Value": "",
                "ControlImplementationId": intControl,
                "CreatedById": userId,
                "DateCreated": None,
                "LastUpdatedById": userId,
                "DateLastUpdated": None,
            }
            ctrlparam["Name"] = x
            if "values" in ciParams[x]:
                ctrlValues = ciParams[x]["values"]
                strValue = ""
                for y in ctrlValues:

                    strValue += y
                ctrlparam["Value"] = strValue
            # add the parameter
            atlasityParams.append(ctrlparam)
            # create the parameter
            try:
                response = requests.request("POST", url_param, headers=headers, json=ctrlparam)
                scJsonResponse = response.json()
                print(Logger.OK + "Parameter Success - " + ctrlparam["Name"] + " - " + str(scJsonResponse["id"]) + Logger.END)
                intParamTotal += 1
            except requests.exceptions.HTTPError as errh:
                print (Logger.ERROR + "Http Error:", errh  + Logger.END)
            except requests.exceptions.ConnectionError as errc:
                print (Logger.ERROR + "Error Connecting:", errc + Logger.END)
            except requests.exceptions.Timeout as errt:
                print (Logger.ERROR + "Timeout Error:",errt + Logger.END)
            except requests.exceptions.RequestException as err:
                print (Logger.ERROR + "OOps: Something Else", err + Logger.END)


#troubleshooting
if intMisses > 0:
    print(Logger.WARNING + str(intMisses) + " total controls missing in this catalog/profile." + Logger.END)
print(Logger.OK + "SUCCESS: " + str(intTotal) + " controls were found and mapped correctly for this SSP." + Logger.END)
print(Logger.OK + "SUCCESS: " + str(intCompTotal) + " components were uploaded for this SSP." + Logger.END)
print(Logger.OK + "SUCCESS: " + str(intParamTotal) + " parameters were uploaded for this SSP." + Logger.END)

#artifacts for troubleshooting/verifications
with open("artifacts/controls.json", "w") as outfile: 
    outfile.write(json.dumps(atlasityCTRLs, indent=4)) 
with open("artifacts/components.json", "w") as outfile: 
    outfile.write(json.dumps(atlasityCOMPS, indent=4)) 
with open("artifacts/parameters.json", "w") as outfile: 
    outfile.write(json.dumps(atlasityParams, indent=4)) 