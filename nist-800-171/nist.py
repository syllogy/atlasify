#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

# set the catalog URL for your Atlasity instance
url_cats = "https://atlas-dev.c2labs.com/api/catalogues"

headers = {
   'Authorization': 'Bearer <atlasity_api_token>'
}

# load local json
f = open('800-171.json', 'r', encoding='utf-8-sig')
data = json.load(f,)

# create controls array
controls = []

# create a counter for records created
intTotal = 0

#loop through and print the results
for i in data["ITS-Managed"]:

    #print the raw data
    #print(i["NIST 800-171 Control Number"])

    #create the object
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
    "catalogueID": 0,
    "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
    "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14" }

    #append the result
    controls.append(sc)

    # increment the count
    intTotal += 1

url_sc = "https://atlas-dev.c2labs.com/api/securitycontrols/batchcreate"

print(controls)

#response = requests.request("POST", url, headers=headers, json=payload)
#jsonResponse = response.json()

#print("\n\nSuccess - Catalog created and controls uploaded.\n")

print(intTotal)
