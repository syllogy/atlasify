#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import argparse

# setup parser for command line arguments
parser = argparse.ArgumentParser(description='Atlasity parser for NIST 800-53 OSCAL')
parser.add_argument('token', metavar='path', type=str, help='Atlasity JWT token to authenticate API calls')

# get the argument from the command line
args = parser.parse_args()
if (args.token == ''):
    print('No JWT Bearer token provided.')
else:
    print(args.token)
    token = args.token

# set the catalog URL for your Atlasity instance
url_cats = "http://localhost:5000/api/catalogues"

# set your bearer token (Click your name in top right and select Service Accounts, paste Bearer token from this page)
headers = {
   'Authorization': 'Bearer ' + token
}

# setup catalog data
cat = {
    "title": "NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations",
    "description": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. ",
    "datePublished": "9/1/2020",
    "lastRevisionDate": "9/1/2020",
    "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
    "abstract": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. The controls are flexible and customizable and implemented as part of an organization-wide process to manage risk. The controls address diverse requirements derived from mission and business needs, laws, executive orders, directives, regulations, policies, standards, and guidelines. Finally, the consolidated control catalog addresses security and privacy from a functionality perspective (i.e., the strength of functions and mechanisms provided by the controls) and from an assurance perspective (i.e., the measure of confidence in the security or privacy capability provided by the controls). Addressing functionality and assurance helps to ensure that information technology products and the systems that rely on those products are sufficiently trustworthy.",
    "keywords": "assurance; availability; computer security; confidentiality; control; cybersecurity; FISMA; information security; information system; integrity; personally identifiable information; Privacy Act; privacy controls; privacy functions; privacy requirements; Risk Management Framework; security controls; security functions; security requirements; system; system security.",
    "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14" }

# create the catalog and print success result
#response = requests.request("POST", url_cats, headers=headers, json=cat)
#jsonResponse = response.json()
#print("\n\nAtlasity Output\n")
#print(response.text.encode('utf8'))
#print("\nCatalog ID: " + str(jsonResponse["id"]))

# get the catalog ID
#intCat = jsonResponse["id"]
intCat = 1

# load translated Excel file (cleaned and converted to JSON)
excel = open('80053rev5-excelConversion.json', 'r', encoding='utf-8-sig')
excelData = json.load(excel)

# load the full catalog for the NIST 800-53 OSCAL
oscal = open('NIST_SP-800-53_rev5-FINAL_catalog.json', 'r', encoding='utf-8-sig')
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
    #add parsed/flattened resource to the array
    res = {
        "uuid": strResourceGUID,
        "short": strResourceTitle,
        "title": strCitation
    }
    resources.append(res)

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
        strLinks = ""
        #process control links
        if ("links" in ctrl):
            for l in ctrl["links"]:
                strLinks += l["text"]
        #add control
        newCTRL = {
            "id": ctrl["id"],
            "title": ctrl["title"],
            "family": strFamily,
            "links": strLinks
        }
        oscalControls.append(newCTRL)

print(oscalControls)

# create controls array
controls = []

# create a counter for records created
intTotal = 0

# your Atlasity URL
url_sc = "http://localhost:5000/api/securitycontrols"

#loop through and print the results
for i in excelData["SP 800-53 Revision 5"]:

    #make sure values exist
    if ("Related Controls" in i):
        strRelated = i["Related Controls"]
    else: 
        strRelated = ""
    if ("Control (or Control Enhancement) " in i):
        strControl = i["Control (or Control Enhancement) "]
    else:
        strControl = ""
    if ("Discussion" in i):
        strDiscussion = i["Discussion"]
    else:
        strDiscussion = ""

    # create each security control
    # NOTE: Use your user ID in Atlasity which you can find under your user profile
    sc = {
    "title": i["Control Number"] + " - " + i["Control (or Control Enhancement) Name"],
    "description": strControl + "<br/><h3>Discussion</h3>" + strDiscussion,
    "references": "",
    "relatedControls": strRelated,
    "subControls": "",
    "enhancements": "",
    "family": "",
    "mappings": "",
    "assessmentPlan": "",
    "weight": 0,
    "practiceLevel": "",
    "catalogueID": intCat,
    "UUID": strUUID,
    "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14" }

    #append the result
    controls.append(sc)

    # increment the count
    intTotal += 1

    # # attempt to create the security control
    # try:
    #     response = requests.request("POST", url_sc, headers=headers, json=sc)
    #     jsonResponse = response.json()
    #     print("\n\nSuccess - " + sc["title"])
    # except requests.exceptions.HTTPError as errh:
    #     print ("Http Error:",errh)
    #     print("\n\nError - " + sc["title"])
    # except requests.exceptions.ConnectionError as errc:
    #     print ("Error Connecting:",errc)
    #     print("\n\nError - " + sc["title"])
    # except requests.exceptions.Timeout as errt:
    #     print ("Timeout Error:",errt)
    #     print("\n\nError - " + sc["title"])
    # except requests.exceptions.RequestException as err:
    #     print ("OOps: Something Else",err)
    #     print("\n\nError - " + sc["title"])

# # output total controls created
# print(intTotal)

# # retrieve full list created
# url_allcats = "http://localhost:5000/api/SecurityControls/filterSecurityControlsByCatalogue/" + str(intCat)

# headers_allcats = {
#    "Accept": "application/json",
#    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob3dpZWF2cCIsImp0aSI6ImJkZGM0ZDQ5LTdjZjMtNDcwNS04YjNjLTkwZDg0ODAyOTdhYSIsImlhdCI6MTYwNDI0Mjc2MywiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiI4ZDhkNTQ2OC03NGY4LTQ5OWQtOTc2Yy1iY2E2NzFlMTliMTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiaG93aWVhdnAiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbmlzdHJhdG9yIiwibmJmIjoxNjA0MjQyNzYzLCJleHAiOjE2MDQzMjkxNjMsImlzcyI6IkF0bGFzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwLyJ9.0PNlLKFJ9UUQaQnLTmQ_w-vtTxEpq0C0mH-QPYZeqJA'
# }

# allcats = requests.request(
#    "GET",
#    url_allcats,
#    headers=headers_allcats,
# )
# catsArray = allcats.json()

# # loop through and compare arrays, see if anything is missing (validation check)
# intMatch = 0
# for y in controls:
#     bMatch = False
#     # make sure each control in the raw JSON was returned from Atlasity
#     for z in catsArray:
#         if z["title"] == y["title"] :
#             bMatch = True
#             break
#     #make sure they match or throw error in console if missing
#     if bMatch == True :
#         intMatch += 1
#     else:
#         # ones that didn't upload
#         print("ERROR: " + y["title"] + " is missing.")
#         # see if it was length related
#         print(len(y["title"] ))

# # validate all were loaded
# if intMatch == intTotal :
#     print("SUCCESS: Verified all controls were successfully created.")




