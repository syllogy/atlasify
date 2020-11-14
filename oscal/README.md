# OSCAL Integration - Catalog and Profile Importer

This repository contains example Python scripts for processing NIST OSCAL artficacts and parsing and loading them into Atlasity as catalogues and controls.

## Purpose

A large number of Atlasity customers, especially government, rely on publications for NIST to build their cyber security programs.  Many Information System Security Plans (ISSPs) are based on NIST related publications.  In this case, this repository is focused on processing NIST 800-53 Rev 5 using the tooling published by the NIST OSCAL team.  Our goals included:

- Create Atlasity catalogs using automation to parse NIST OSCAL files for NIST 800-53 Rev 5
- Create catalogs for Low, Moderate, High, and Privacy using the same tool
- Fuse data from multiple sources to enrich the catalogs prior to loading (i.e. OSCAL files, 800-53 rev 5 spreadsheet, etc.)

## Process

- Downloaded the Excel version of 800-53 rev5 from the NIST website
- Download the NIST OSCAL versions of 800-53 from their GitHub site
- Cleaned the Excel file - control numbers did not match in format between the Excel version and JSON.  Did some substitution string manipulation to make the control numbers exactly match so the data could be programmatically merged

## Run the Script

Setup - you will need the following Atlasity items to run this script:

- Get your user ID within Atlasity (the GUID on your profile) to use in the created by fields, replace existing GUIDs
- Get your JWT Bearer token within Atlasity (from the Service Account page)
- Your Atlasity URL to route API calls to a running Atlasity instance

To load the full catalog, run the script below (NOTE: You must pass in the bearer token for your Atlasity user, must be an admin or maintainer account, and do include the 'Bearer' portion):

`py importer.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob3dpZWF2cCIsImp0aSI6ImJhZjI5MDgxLTYwNTEtNGQzNy05NWY5LTc3YmI1Y2M0NjE5OSIsImlhdCI6MTYwNTM2MTkzNywiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiI4ZDhkNTQ2OC03NGY4LTQ5OWQtOTc2Yy1iY2E2NzFlMTliMTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2gsYWltcy9uYW1lIjoiaG93aWVhdnAiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbmlzdHJhdG9yIiwibmJmIjoxNjA1MzYxOTM2LCJleHAiOjE2MDU0NDgzMzYsImlzcyI6IkF0bGFzIiwiYXVkIjoiaHR0cDovL2xvY2FtaG9zdDo1MDAwLyJ9.46Nq59adKvXajdADCAz__WZxeD-BzRYZ9dnW5QmSdGo`

Once this tool runs, it outputs a set of files that can be used with the profile importer to create discrete profiles.  After completing the full catalog import, run this command to create each baseline within Atlasity (NOTE: You must pass in the bearer token for your Atlasity user, must be an admin or maintainer account, and do include the 'Bearer' portion):

`py profiles.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob3dpZWF2cCIsImp0aSI6ImJhZjI5MDgxLTYwNTEtNGQzNy05NWY5LTc3YmI1Y2M0NjE5OSIsImlhdCI6MTYwNTM2MTkzNywiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiI4ZDhkNTQ2OC03NGY4LTQ5OWQtOTc2Yy1iY2E2NzFlMTliMTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2gsYWltcy9uYW1lIjoiaG93aWVhdnAiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbmlzdHJhdG9yIiwibmJmIjoxNjA1MzYxOTM2LCJleHAiOjE2MDU0NDgzMzYsImlzcyI6IkF0bGFzIiwiYXVkIjoiaHR0cDovL2xvY2FtaG9zdDo1MDAwLyJ9.46Nq59adKvXajdADCAz__WZxeD-BzRYZ9dnW5QmSdGo`

## References

- [NIST OSCAL Website](https://pages.nist.gov/OSCAL/) 
- [NIST OSCAL GitHub Site - OSCAL Content](https://github.com/usnistgov/OSCAL)
- [NIST 800-53 Rev 5 Website](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

## Useful Tools

The JSON files generate by the OSCAL team are large and need easy to visually parse by humans.  We leveraged a free online tool - [JSON Viewer](http://jsonviewer.stack.hu/) - that allows you interactively drill into the data.  This tool was a nice complement for our developers to assist with working on this large data set.  In addition, we used the [Beautify Tools](http://beautifytools.com/excel-to-json-converter.php) to do an Excel to JSON conversion to allow for easier programmatic manipulation of the data.

## OSCAL Feedback

Below is a running log of feedback on enhancements to OSCAL that would have made this import easier:

- The 800-53 rev 5 spreadsheet from NIST and OSCAL use different numbering formats for control enhancements.  This difference requires some pre-processing.  Some feedback that would help:
    - Update the spreadsheet to match the OSCAL naming convention, or vice-versa
    - Ideally, add the OSCAL control GUID to the spreadsheet as a new column
- Some resources in the NIST 800-53 rev5 catalog have no data, requires more error handling in the code
- When fields have no data, they are removed from the OSCAL files.  Would prefer them to default to an empty string so they are always there.  Allows for more efficient looping without constantly checking if the data exists.