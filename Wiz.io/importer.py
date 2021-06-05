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
url_login = "http://atlas-dev.c2labs.com/api/authentication/login"

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

# get all security controls for the plan provided
url_getPlans = "https://atlas-dev.c2labs.com/api/controlImplementation/getAllByPlan/" + intPlan
responseSC = requests.request("GET", url_getPlans, headers=headers)
scDict = json.loads(responseSC.text)

#loop through the security controls
for sc in scDict:
    print(sc["controlTitle"])
