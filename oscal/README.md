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

These scripts provide feedback in the terminal to monitor progress on parsing and uploading.  It also performs validation at the end to ensure that all parsed controls are uploaded successfully into Atlasity.

NOTE: This script is a proof of concept for parsing OSCAL content to load it into an external tool.  Atlasity customers will not need to use this script.  Atlasity has internal mechanisms for importing and exporting catalogs that do not rely on any external tools/scripts.  

## Output Files

As part of that process, we generated some new versions of JSON that are flattened and cleaned across multiple sources.  These raw artifacts are shown below and provided for others use where there is a desire to leverage this data programatically without dealing with the complexity of parsing OSCAL:

- `AtlasityControls.json` - the full NIST 800-53 catalog in a flat JSON file
- `OSCALParsedControls.json` - full list of controls parsed from OSCAL; mostly used to normalize families and links for controls in a flat format
- `OSCALParsedControls-High.json` - full list of controls parsed from OSCAL; mostly used to normalize families and links for controls in a flat format; all controls for HIGH baseline
- `OSCALParsedControls-Moderate.json` - full list of controls parsed from OSCAL; mostly used to normalize families and links for controls in a flat format; all controls for MODERATE baseline
- `OSCALParsedControls-Low.json` - full list of controls parsed from OSCAL; mostly used to normalize families and links for controls in a flat format; all controls for LOW baseline
- `OSCALParsedControls-Privacy.json` - full list of controls parsed from OSCAL; mostly used to normalize families and links for controls in a flat format; all controls for PRIVACY baseline
- `OSCALParsedFamilies.json` - full list of NIST 800-53 control families
- `OSCALParsedResources.json` - full list of resources used within NIST 800-53 Rev 5 including all references

## References

- [Atlasity.io](https://atlasity.io)
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
    - UUID: c3397cc9-83c6-4459-adb2-836739dc1b94
    - UUID: f7cf488d-bc64-4a91-a994-810e153ee481
- When fields have no data, they are removed from the OSCAL files.  Would prefer them to default to an empty string so they are always there.  Allows for more efficient looping without constantly checking if the data exists.
- Some baselines reference controls that do not exist:
    - NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - PRIVACY Baseline - pm-33 not found.
    - NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - PRIVACY Baseline - pt-8.1 not found.
    - NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - PRIVACY Baseline - pt-8.2 not found.
    - NIST 800-53 Rev. 5 - Security and Privacy Controls for Information Systems and Organizations - PRIVACY Baseline - pt-9 not found.