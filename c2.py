#!/usr/bin/python
# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

# Get a list of projects from Jira (C2 Projects for this example)
url_jira = "https://atlas-dev.c2labs.com/api/projects/getAll"

headers_jira = {
   "Accept": "application/json",
   'Authorization': 'Bearer <atlasity_api_token>'
}

response_jira = requests.request(
   "GET",
   url_jira,
   headers=headers_jira,
)
jsonResponse_jira = response_jira.json()

print("\nJira Output\n")
print(response_jira.text.encode('utf8'))

# ADD CODE to parse the Output from Jira
assessmentReportText = "<br><b>Assessment Report</b><br>List of Projects:"
for i in jsonResponse_jira:
    # print(i["title"])
    assessmentReportText = assessmentReportText + "<br>" + i["title"]

print("\n\n--------------------------------\n")

print(assessmentReportText)

print("\n\n--------------------------------\n")

url = "https://atlas-dev.c2labs.com/api/assessments"
# url = "http://localhost:5000/api/assessments"

payload = {"leadAssessorId": "44f8b777-1647-4b73-933d-b3e9135c1c52",
"title": "Testing with Travis with Projects",
"assessmentType": "Script/DevOps Check",
"assessmentResult": "Partial Pass",
"plannedStart": "10/30/2020",
"plannedFinish": "10/30/2020",
"status": "Complete",
"actualFinish": "10/30/2020",
"assessmentReport": assessmentReportText,
"parentId": 3,
"parentModule": "requirements",
"createdById": "44f8b777-1647-4b73-933d-b3e9135c1c52",
"lastUpdatedById": "44f8b777-1647-4b73-933d-b3e9135c1c52"}

headers = {
  'Authorization': 'Bearer <atlasity_api_token>'
}

response = requests.request("POST", url, headers=headers, json=payload)
jsonResponse = response.json()

print("\n\nAtlasity Output\n")
print(response.text.encode('utf8'))

print("\nAssessment ID: " + str(jsonResponse["id"]))
