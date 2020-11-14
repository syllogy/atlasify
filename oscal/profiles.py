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

# load parsed data from initial catalogue load
oscalRaw = open('AtlasityControls.json', 'r', encoding='utf-8-sig')
oscalControls = json.load(oscalRaw)

# create array of profiles to iterate through
profiles = [
    {
        "title": "NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - HIGH Baseline",
        "fileName": "NIST_SP-800-53_rev5-FPD_HIGH-baseline_profile.json",
        "export": "OSCALParsedControls-High.json"
    },
    {
        "title": "NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - MODERATE Baseline",
        "fileName": "NIST_SP-800-53_rev5-FPD_MODERATE-baseline_profile.json",
        "export": "OSCALParsedControls-Moderate.json"
    },
    {
        "title": "NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - LOW Baseline",
        "fileName": "NIST_SP-800-53_rev5-FPD_LOW-baseline_profile.json",
        "export": "OSCALParsedControls-Low.json"
    },
    {
        "title": "NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - PRIVACY Baseline",
        "fileName": "NIST_SP-800-53_rev5-FPD_PRIVACY-baseline_profile.json",
        "export": "OSCALParsedControls-Privacy.json"
    }
]

# set the catalog URL for your Atlasity instance
url_cats = "http://localhost:5000/api/catalogues"

# set your bearer token (Click your name in top right and select Service Accounts, paste Bearer token from this page)
headers = {
   'Authorization': 'Bearer ' + token
}

# loop over the profiles to load each one
for p in profiles:
    # setup catalog data
    cat = {
        "title": p["title"],
        "description": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. ",
        "datePublished": "9/1/2020",
        "lastRevisionDate": "9/1/2020",
        "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
        "abstract": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. The controls are flexible and customizable and implemented as part of an organization-wide process to manage risk. The controls address diverse requirements derived from mission and business needs, laws, executive orders, directives, regulations, policies, standards, and guidelines. Finally, the consolidated control catalog addresses security and privacy from a functionality perspective (i.e., the strength of functions and mechanisms provided by the controls) and from an assurance perspective (i.e., the measure of confidence in the security or privacy capability provided by the controls). Addressing functionality and assurance helps to ensure that information technology products and the systems that rely on those products are sufficiently trustworthy.",
        "keywords": "assurance; availability; computer security; confidentiality; control; cybersecurity; FISMA; information security; information system; integrity; personally identifiable information; Privacy Act; privacy controls; privacy functions; privacy requirements; Risk Management Framework; security controls; security functions; security requirements; system; system security.",
        "createdById": "8d8d5468-74f8-499d-976c-bca671e19b14",
        "lastUpdatedById": "8d8d5468-74f8-499d-976c-bca671e19b14" }

    # create the catalog and print success result
    response = requests.request("POST", url_cats, headers=headers, json=cat)
    jsonResponse = response.json()
    print("\n\nAtlasity Output\n" + p["title"])
    print(response.text.encode('utf8'))
    print("\nCatalog ID: " + str(jsonResponse["id"]))

    # get the catalog ID
    intCat = jsonResponse["id"]

    # load translated Excel file (cleaned and converted to JSON)
    oscal = open(p["fileName"], 'r', encoding='utf-8-sig')
    oscalData = json.load(oscal)

    # create controls array
    controls = []

    # create a counter for records created
    intTotal = 0

    # your Atlasity URL
    url_sc = "http://localhost:5000/api/securitycontrols"

    #parse the OSCAL Profile JSON to get the controls to load 
    arrL1 = oscalData["profile"]
    imports = arrL1["imports"]
    obj = imports[0]
    include = obj["include"]
    ctrls = include["id-selectors"]

    #loop through controls in the baseline
    for c in ctrls:
        # find the control
        lookup = next((item for item in oscalControls if item["title"].startswith(c["control-id"].upper()) == True), None)

        # make sure something was returned
        if (lookup == None):
            print(p["title"] + " - " + c["control-id"] + " not found.")
        else:
            #update catalog ID
            lookup["catalogueID"] = intCat
            
            #add control to this baseline
            controls.append(lookup)

        #increment the total processed in this baseline
        intTotal += 1

        # attempt to create the security control
        if (lookup != None):
            try:
                response = requests.request("POST", url_sc, headers=headers, json=lookup)
                jsonResponse = response.json()
                print("\n\nSuccess - " + lookup["title"])
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
                print("\n\nError - " + lookup["title"])
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
                print("\n\nError - " + lookup["title"])
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
                print("\n\nError - " + lookup["title"])
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)
                print("\n\nError - " + lookup["title"])

    # Write to file to visualize the output
    with open(p["export"], "w") as outfile: 
        outfile.write(json.dumps(controls, indent=4)) 

    # retrieve full list created
    url_allcats = "http://localhost:5000/api/SecurityControls/filterSecurityControlsByCatalogue/" + str(intCat)

    headers_allcats = {
    "Accept": "application/json",
    'Authorization': 'Bearer ' + token
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




