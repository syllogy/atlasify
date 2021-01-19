# OSCAL Integration - Catalog and Profile Importer

This repository contains example Python scripts for processing NIST OSCAL artifacts and parsing and loading them into Atlasity as catalogues and controls.

## Purpose

A large number of Atlasity customers, especially government, rely on publications from NIST to build their cyber security programs.  Many Information System Security Plans (ISSPs) are based on NIST related publications.  In this case, this repository is focused on processing NIST 800-53 Rev 4 and Rev 5 catalogs/profiles using the tooling published by the NIST OSCAL team.  Our goals included:

- Create Atlasity catalogs using automation to parse NIST OSCAL files for NIST 800-53 Rev 4 & 5
- Create catalogs for Low, Moderate, High, and Privacy using the same tool
- Create catalogs to support FedRAMP baselines

## Background

This work was performed using Open Source code and tooling in support of the [ATARC Cloud Security Working Group](https://atarc.org/working-groups/cloud-working-group/#:~:text=The%20ATARC%20Cloud%20Working%20Group,the%20Federal%20cloud%20%26%20infrastructure%20community.)

## Process

- Downloaded the NIST OSCAL versions of 800-53 from their [GitHub site](https://github.com/usnistgov/oscal-content) 
- Loaded the full catalog for each version of 800-53 using OSCAL
- Loaded each profile based on these catalogs using OSCAL published Release Candidate (RC) profiles
- Documented issues encountered in the process to provide feedback to the NIST OSCAL team and ATARC

## Run the Script

Setup - you will need the following Atlasity items to run this script:

- Get your user ID within Atlasity (the GUID on your profile) to use in the created by fields, replace existing GUIDs
- Login via command line to get your JWT token
- Your Atlasity URL to route API calls to a running Atlasity instance

To load the full catalog, run the script below (NOTE: You must must be an admin or maintainer account and select the proper script (rev 4 or 5)):

`py importer-rev4-catalog.py --user 'username' --pwd 'password'`

- or -

`py importer-rev5-catalog.py --user 'username' --pwd 'password'`

Once this tool runs, it outputs a set of files that can be used with the profile importer to create discrete profiles.  After completing the full catalog import, run this command to create each baseline within Atlasity (NOTE: You must pass in the bearer token for your Atlasity user, must be an admin or maintainer account, and do include the 'Bearer' portion):

`py profiles.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob3dpZWF2cCIsImp0aSI6ImJhZjI5MDgxLTYwNTEtNGQzNy05NWY5LTc3YmI1Y2M0NjE5OSIsImlhdCI6MTYwNTM2MTkzNywiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZWlkZW50aWZpZXIiOiI4ZDhkNTQ2OC03NGY4LTQ5OWQtOTc2Yy1iY2E2NzFlMTliMTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2gsYWltcy9uYW1lIjoiaG93aWVhdnAiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbmlzdHJhdG9yIiwibmJmIjoxNjA1MzYxOTM2LCJleHAiOjE2MDU0NDgzMzYsImlzcyI6IkF0bGFzIiwiYXVkIjoiaHR0cDovL2xvY2FtaG9zdDo1MDAwLyJ9.46Nq59adKvXajdADCAz__WZxeD-BzRYZ9dnW5QmSdGo`

These scripts provide feedback in the terminal to monitor progress on parsing and uploading.  It also performs validation at the end to ensure that all parsed controls are uploaded successfully into Atlasity.

NOTE: This script is a proof of concept for parsing OSCAL content to load it into an external tool.  Atlasity customers will not need to use this script.  Atlasity has internal mechanisms for importing and exporting catalogs that do not rely on any external tools/scripts. We used this script internally to C2 Labs to load the NIST OSCAL data but have published relevant catalogues within Atlasity for ease of customer use.

## References

- [Atlasity.io](https://atlasity.io)
- [NIST OSCAL Website](https://pages.nist.gov/OSCAL/) 
- [NIST OSCAL GitHub Site - OSCAL Content](https://github.com/usnistgov/OSCAL)
- [NIST 800-53 Rev 4 Website](https://csrc.nist.gov/publications/detail/sp/800-53/rev-4/final)
- [NIST 800-53 Rev 5 Website](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

## Useful Tools

The JSON files generate by the OSCAL team are large and not easy to visually parse by humans.  We leveraged a free online tool - [JSON Viewer](http://jsonviewer.stack.hu/) - that allows you to interactively drill into the data.  This tool was a nice complement for our developers to assist with working on this large data set.  

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
- For the base control metadata, the Excel file published by NIST was a lot easier to manipulate and parse than the OSCAL.  For that reason, we chose to use the Excel file as the base of our work, convert it to JSON using free tools, and then enrich it with additional data available in the OSCAL.
- Controls do not have GUIDS where you can cross-reference betwen the catalog and baselines.  Ran into issues with case sensitivity that required some additional processing.  Also, found some items in the baselines that don't exist in the catalog as shown above.  