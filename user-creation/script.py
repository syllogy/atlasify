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

# setup parser for command line arguments
parser = argparse.ArgumentParser(description='Atlasity parser for CMMC with Objectives')
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

# login to your Atlasity instance
url_login = "https://atlas-dev.c2labs.com/api/authentication/login"

# set the catalog URL for your Atlasity instance
url_cats = "https://atlas-dev.c2labs.com/api/catalogues"

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

# set desired user attribes for the new user
user = {
    "id": "",
    "userName": "dead", 
    "email": "thowerton@c2labs.com", 
    "password": "RAND0m$$2021pwd", 
    "firstName": "Rick",
    "lastName": "Grimes",
    "workPhone": "8658888888",
    "mobilePhone": "8658888888",
    "pictureURL": "", # user avatar, leave blank and let them set in the UI
    "activated": True,
    "jobTitle": "Walker Killer",
    "orgId": None,
    "emailNotifications": True,
    "createdById": userId,
    "dateCreated": None,
    "lastUpdatedById": userId,
    "dateLastUpdated": None,
    "tenantId": 1 #default to first tenant, set appropriately
}

# your Atlasity URL
url_user = "https://atlas-dev.c2labs.com/api/accounts"

# attempt to create the user
userResponse = requests.request("POST", url_user, headers=headers, json=user)
userOBJ = userResponse.json()

# get the list of roles
url_roles = "https://atlas-dev.c2labs.com/api/accounts/getRoles"
roleRaw = requests.request("GET", url_roles, headers=headers)
roleList = roleRaw.json()
strRoleId = ""
for role in roleList:
    if role["name"] == "Administrator":
        # get the Role ID for the administrator
        strRoleId = role["id"]

# assign the role
url_assign = "https://atlas-dev.c2labs.com/api/accounts/assignRole"

# create the role assignment
role = {
    "userId": userOBJ["id"],
    "roleId": strRoleId
}

# attempt to create the security control
assignRaw = requests.request("POST", url_assign, headers=headers, json=role)
assignOBJ = assignRaw.json()
print(assignOBJ)







