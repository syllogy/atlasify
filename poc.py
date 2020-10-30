#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json


# Get a list of projects from Jira
url_jira = "https://your-domain.atlassian.com/rest/api/3/project/search"

auth_jira = HTTPBasicAuth("email@example.com", "<api_token>")

headers_jira = {
   "Accept": "application/json"
}

response_jira = requests.request("GET", url_jira, headers=headers_jira, auth=auth_jira)
jsonResponse_jira = response_jira.json()

print("\nJira Output\n")
print(json.dumps(json.loads(response_jira.text), sort_keys=True, indent=4, separators=(",", ": ")))

# ADD CODE to parse the Output from Jira
assessmentReportText = "<br><b>Assessment Report</b><br>List of Projects:"
for i in jsonResponse_jira["values"]:
    # print(i["name"])
    assessmentReportText = assessmentReportText + "<br>" + i["name"]

print("\n\n--------------------------------\n")

print(assessmentReportText)

print("\n\n--------------------------------\n")

# Post output to Atlasity
url = "https://c2.pnmac.com/api/assessments"

headers = {
  'Authorization': 'Bearer <atlasity_api_token>'
}

payload = {"leadAssessorId": "b7dd8ff0-80d2-4d01-9916-a736fdcecafd",
"title": "Testing 123",
"assessmentType": "Script/DevOps Check",
"assessmentResult": "Pass",
"plannedStart": "10/29/2020",
"plannedFinish": "10/29/2020",
"status": "Complete",
"actualFinish": "10/29/2020",
"assessmentReport": assessmentReportText,
"parentId": 4,
"parentModule": "requirements",
"createdById": "b7dd8ff0-80d2-4d01-9916-a736fdcecafd",
"lastUpdatedById": "b7dd8ff0-80d2-4d01-9916-a736fdcecafd"}

response = requests.request("POST", url, headers=headers, json=payload, verify=False)
jsonResponse = response.json()

print("\n\nAtlasity Output\n")
print(response.text.encode('utf8'))

print("\nAssessment ID: " + str(jsonResponse["id"]))
