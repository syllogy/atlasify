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

# function for recursively working through objectives
def processObjectives(obj):
    strOBJ = "<ul>"
    for o in obj:
        strOBJ += "<li>" + o["name"] + ": {{" + o["id"] + "}}"
        if ("prose" in o):
            strOBJ += " - " + o["prose"]
        strOBJ += "</li>"
        if ("parts" in o):
            strOBJ += processObjectives(o["parts"])
    strOBJ += "</ul>"
    return strOBJ

# function to process each control
def processControl(ctrl, resources):
    strParams = ""
    if ("params" in ctrl):
        strParams += "<strong>Parameters</strong><br/>"
        for p in ctrl["params"]:
            if ("label" in p):
                strParams += "{{" + p["id"] + "}}: " + p["label"] + "<br/>"
            else:
                if ("select" in p):
                    select = p["select"]
                    strParams += p["id"] + ", "
                    if ("how-many" in select):
                        strParams += "How Many: " + select["how-many"]
                    if ("choice" in select):
                        for z in select["choice"]:
                            strParams += z + ", "
                        strParams += "<br/>"
    strLinks = ""

    #get enhancements
    strEnhance = ""
    if ("controls" in ctrl):
        childENHC = ctrl["controls"]
        strEnhance += "<strong>Enhancements</strong><br/><br/>"
        strEnhance += "<ul>"
        for che in childENHC:
            strEnhance += "<li>{{" + che["id"] + "}} - " + che["title"] + "</li>"
        strEnhance += "</ul>"
        
    #process control links
    if ("links" in ctrl):
        for l in ctrl["links"]:
            #lookup the OSCAL control to enrich the data
            linkLookup = next((item for item in resources if ("#" +item["uuid"]) == l["href"]), None)
            if (linkLookup != None):
                strLinks += "{{" + linkLookup["uuid"] + "}} - " + linkLookup["title"] + "<br/>"
            else: 
                strLinks += l["href"] + "<br/>"
        
    #process parts
    if ("parts" in ctrl):
        strParts = ""
        strGuidance = ""
        strAssessment = ""
        strParts += "<ul>"
        for p in ctrl["parts"]:
            if ("id" in p):
                # process objectives
                if (p["name"] == "objective" or p["name"] == "statement"):
                    try:
                        strParts += "<li>ID: {{" + p["id"] + "}}, Name: " + p["name"] + " - " + p["prose"] + "</li>"
                    except:
                        print(p)
                    if ("parts" in p):
                        strParts += processObjectives(p["parts"])
                # process guidance
                if (p["name"] == "guidance"):
                    strGuidance = "<ul><li>Guidance</li>"
                    if ("links" in p):
                        strGuidance += "<ul>"
                        for lkp in p["links"]:
                            strGuidance += "<li>" + lkp["href"] + ", " + lkp["rel"] + "</li>"
                        strGuidance += "</ul>"
                    strGuidance += "</ul>"
            else:
                # process assessments
                if (p["name"] == "assessment"):
                    strAssessment = "<ul><li>Assessment</li>"
                    if ("props" in p):
                        strAssessment += "<ul>"
                        props = p["props"]
                        for pr in props:
                            strAssessment += "<li>Assessment Type: " + pr["value"] + "</li>"
                    if ("parts" in p):
                        strAssessment += "<ul>"
                        for pts in p["parts"]:
                            strAssessment += "<li>" + pts["prose"] + "</li>"
                            strAssessment += "</ul>"
                        strAssessment += "</ul>"
                    strAssessment += "</ul>"                        
        strParts += "</ul>"
    else:
        # no parts - set default values
        strParts = ""
        strGuidance = ""
        strAssessment = ""
        
    #add control
    newCTRL = {
        "id": ctrl["id"],
        "title": ctrl["title"],
        "family": strFamily,
        "links": strLinks,
        "parameters": strParams,
        "parts": strParts,
        "assessment": strAssessment,
        "guidance": strGuidance,
        "enhancements": strEnhance
    }

    # return the result
    return newCTRL

# setup parser for command line arguments
parser = argparse.ArgumentParser(description='Atlasity parser for NIST 800-53 OSCAL')
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

# load the catalog
oscal = open('nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json', 'r', encoding='utf-8-sig')
oscalData = json.load(oscal)

#parse the OSCAL JSON to get related data (used to enrich base spreadsheet)
arrL1 = oscalData["catalog"]
strUUID = arrL1["uuid"]

#process resources for lookup
resources = []
arrL2 = arrL1["back-matter"]
for i in arrL2["resources"]:
    #make sure values exist
    strResourceTitle = ""
    if ("title" in i):
        strResourceTitle = i["title"]
    strResourceGUID = ""
    if ("uuid" in i):
        strResourceGUID = i["uuid"]
    strCitation = ""
    if ("citation" in i):
        citation = i["citation"]
        if ("text" in citation):
            strCitation = citation["text"]
    strLinks = ""
    if ("rlinks" in i):
        links = i["rlinks"]
        for x in links:
            if ("href" in x):
                strLinks += x["href"] + "<br/>"
    #add parsed/flattened resource to the array
    res = {
        "uuid": strResourceGUID,
        "short": strResourceTitle,
        "title": strCitation,
        "links": strLinks
    }
    resources.append(res)

# Write to file to visualize the output
with open("rev5artifacts/resources.json", "w") as outfile: 
    outfile.write(json.dumps(resources, indent=4)) 

# create the resource table
strResources = ""
strResources += "<table border=\"1\" style=\"width: 100%;\"><tr style=\"font-weight: bold\"><td>UUID</td><td>Title</td><td>Links</td></tr>"
for res in resources:
    strResources += "<tr>"
    strResources += "<td>" + res["uuid"] + "</td>"
    strResources += "<td>" + res["title"] + "</td>"
    strResources += "<td>" + res["links"] + "</td>"
    strResources += "</tr>"
strResources += "</table>"

# set the catalog URL for your Atlasity instance
url_cats = "http://localhost:5000/api/catalogues"

# setup catalog data
cat = {
    "title": "NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations",
    "description": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. <br/><br/><strong>Resources</strong><br/><br/>" + strResources,
    "datePublished": "9/23/2020",
    "lastRevisionDate": "9/23/2020",
    "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
    "abstract": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. The controls are flexible and customizable and implemented as part of an organization-wide process to manage risk. The controls address diverse requirements derived from mission and business needs, laws, executive orders, directives, regulations, policies, standards, and guidelines. Finally, the consolidated control catalog addresses security and privacy from a functionality perspective (i.e., the strength of functions and mechanisms provided by the controls) and from an assurance perspective (i.e., the measure of confidence in the security or privacy capability provided by the controls). Addressing functionality and assurance helps to ensure that information technology products and the systems that rely on those products are sufficiently trustworthy.",
    "keywords": "assurance; availability; computer security; confidentiality; control; cybersecurity; FISMA; information security; information system; integrity; personally identifiable information; Privacy Act; privacy controls; privacy functions; privacy requirements; Risk Management Framework; security controls; security functions; security requirements; system; system security",
    "createdById": userId,
    "lastUpdatedById": userId }

# create the catalog and print success result
response = requests.request("POST", url_cats, headers=headers, json=cat)
jsonResponse = response.json()
print("\n\nAtlasity Output\n")
print("\nCatalog ID: " + str(jsonResponse["id"]))

# get the catalog ID
intCat = jsonResponse["id"]

#process NIST families of controls
families = []
oscalControls = []

#process groups of controls
for i in arrL1["groups"]:
    strFamily = i["title"]
    f = {
        "id": i["id"],
        "title": i["title"],
    }
    #add parsed item to the family array
    families.append(f)
    
    #loop through controls
    for ctrl in i["controls"]:

        #process the control
        newCTRL = processControl(ctrl, resources)
        oscalControls.append(newCTRL)

        #check for child controls/enhancements
        if ("controls" in ctrl):
            childCTRLs = ctrl["controls"]
            for childCTRL in childCTRLs:
                child = processControl(childCTRL, resources)
                oscalControls.append(child)

# # Write to file to visualize the output
with open("rev5artifacts/families.json", "w") as outfile: 
    outfile.write(json.dumps(families, indent=4)) 

# # Write to file to visualize the output
with open("rev5artifacts/controls.json", "w") as outfile: 
    outfile.write(json.dumps(oscalControls, indent=4)) 

# quit()

# create controls array
controls = []

# create a counter for records created
intTotal = 0

# your Atlasity URL
url_sc = "http://localhost:5000/api/securitycontrols"

#loop through and print the results
for i in oscalControls:

    # create each security control
    sc = {
    "title": i["id"] + " - " + i["title"],
    "controlType": "Stand-Alone",
    "controlId": i["id"],
    "description": i["parts"] + "<br/><br/>" + i["guidance"],
    "references": i["links"],
    "relatedControls": "",
    "subControls": "",
    "enhancements": i["enhancements"],
    "family": i["family"],
    "mappings": i["parameters"],
    "assessmentPlan": i["assessment"],
    "weight": 0,
    "practiceLevel": "",
    "catalogueID": intCat,
    "createdById": userId,
    "lastUpdatedById": userId }

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

# Write to file to visualize the output
with open("rev5artifacts/mappedControls.json", "w") as outfile: 
    outfile.write(json.dumps(controls, indent=4)) 

quit()

# retrieve full list created
url_allcats = "http://localhost:5000/api/SecurityControls/filterSecurityControlsByCatalogue/" + str(intCat)

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
else:
    print("ERROR: Some controls were not created successfully.")


    


