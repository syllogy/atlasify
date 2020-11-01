#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

# set the catalog URL for your Atlasity instance
url_cats = "http://localhost:5000/api/catalogues"

# set your bearer token (Click your name in top right and select Service Accounts, paste Bearer token from this page)
headers = {
   'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob3dpZWF2cCIsImp0aSI6ImJkZGM0ZDQ5LTdjZjMtNDcwNS04YjNjLTkwZDg0ODAyOTdhYSIsImlhdCI6MTYwNDI0Mjc2MywiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiI4ZDhkNTQ2OC03NGY4LTQ5OWQtOTc2Yy1iY2E2NzFlMTliMTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiaG93aWVhdnAiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbmlzdHJhdG9yIiwibmJmIjoxNjA0MjQyNzYzLCJleHAiOjE2MDQzMjkxNjMsImlzcyI6IkF0bGFzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwLyJ9.0PNlLKFJ9UUQaQnLTmQ_w-vtTxEpq0C0mH-QPYZeqJA'
}

# setup catalog data
cat = {
    "title": "NIST 800-171 Rev. 2 - Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations",
    "description": "The purpose of this publication is to provide federal agencies with recommended security requirements for protecting the confidentiality of CUI: 1) when the CUI is resident in a nonfederal system and organization; 2) when the nonfederal organization is not collecting or maintaining information on behalf of a federal agency or using or operating a system on behalf of an agency, and 3) when there are no specific safeguarding requirements for protecting the confidentiality of CUI prescribed by the authorizing law, regulation, or government-wide policy for the CUI category listed in the CUI Registry.",
    "datePublished": "2/21/2020",
    "lastRevisionDate": "2/21/2020",
    "url": "https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final",
    "abstract": "The protection of Controlled Unclassified Information (CUI) resident in nonfederal systems and organizations is of paramount importance to federal agencies and can directly impact the ability of the federal government to successfully conduct its essential missions and functions. This publication provides agencies with recommended security requirements for protecting the confidentiality of CUI when the information is resident in nonfederal systems and organizations; when the nonfederal organization is not collecting or maintaining information on behalf of a federal agency or using or operating a system on behalf of an agency; and where there are no specific safeguarding requirements for protecting the confidentiality of CUI prescribed by the authorizing law, regulation, or governmentwide policy for the CUI category listed in the CUI Registry. The requirements apply to all components of nonfederal systems and organizations that process, store, and/or transmit CUI, or that provide protection for such components. The security requirements are intended for use by federal agencies in contractual vehicles or other agreements established between those agencies and nonfederal organizations.",
    "keywords": "basic security requirement; contractor systems; Controlled Unclassified Information; CUI Registry; derived security requirement; Executive Order 13556; FIPS Publication 199; FIPS Publication 200; FISMA; NIST Special Publication 800-53; ronfederal organizations; nonfederal systems; security assessment; security control; security requirement",
    "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14" }

# create the catalog and printe success result
response = requests.request("POST", url_cats, headers=headers, json=cat)
jsonResponse = response.json()
print("\n\nAtlasity Output\n")
print(response.text.encode('utf8'))
print("\nCatalog ID: " + str(jsonResponse["id"]))

# get the catalog ID
intCat = jsonResponse["id"]

# load local json
f = open('800-171.json', 'r', encoding='utf-8-sig')
data = json.load(f)

# create controls array
controls = []

# create a counter for records created
intTotal = 0

# your Atlasity URL
url_sc = "http://localhost:5000/api/securitycontrols"

#loop through and print the results
for i in data["ITS-Managed"]:

    # create each security control
    # NOTE: Use your user ID in Atlasity which you can find under your user profile
    sc = {
    "title": i["NIST 800-171 Control Number"] + " - " + i["Control Text"],
    "description": i["Discussion"],
    "references": "",
    "relatedControls": i["NIST 800-53 Mapped Control"],
    "subControls": "",
    "enhancements": "",
    "family": i["Control Family"],
    "mappings": "",
    "assessmentPlan": "",
    "weight": i["Weight"],
    "practiceLevel": "",
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

# retrieve full list created
url_allcats = "http://localhost:5000/api/SecurityControls/filterSecurityControlsByCatalogue/" + str(intCat)

headers_allcats = {
   "Accept": "application/json",
   'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob3dpZWF2cCIsImp0aSI6ImJkZGM0ZDQ5LTdjZjMtNDcwNS04YjNjLTkwZDg0ODAyOTdhYSIsImlhdCI6MTYwNDI0Mjc2MywiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiI4ZDhkNTQ2OC03NGY4LTQ5OWQtOTc2Yy1iY2E2NzFlMTliMTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiaG93aWVhdnAiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbmlzdHJhdG9yIiwibmJmIjoxNjA0MjQyNzYzLCJleHAiOjE2MDQzMjkxNjMsImlzcyI6IkF0bGFzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwLyJ9.0PNlLKFJ9UUQaQnLTmQ_w-vtTxEpq0C0mH-QPYZeqJA'
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




