# OSCAL Integration - System Security Plan (SSP) Loader

This repository contains example Python scripts for processing NIST OSCAL SSP artifacts and parsing and loading them into Atlasity as a new security plan

## Purpose

A large number of Atlasity customers, especially government, rely on publications from NIST to build their cyber security programs.  Many Information System Security Plans (ISSPs) are based on NIST related publications.  In this case, this repository is focused on processing OSCAL SSP outputs from the GovReady tool.  Our goals included:

- Create a new SSP with all implemented controls from OSCAL
- Demonstrate the ability to export a SSP from GovReady using OSCAL and then import it into Atlasity using OSCAL (proof of concept for SSP portability)
- Identify any issues to the NIST OSCAL team as feedback for continuous improvement
- Demo the results to the ATARC Working Group

## Background

This work was performed using Open Source code and tooling in support of the [ATARC Cloud Security Working Group](https://atarc.org/working-groups/cloud-working-group/#:~:text=The%20ATARC%20Cloud%20Working%20Group,the%20Federal%20cloud%20%26%20infrastructure%20community.)

## Process

- Downloaded the Excel version of 800-53 rev5 from the NIST website
- Downloaded the NIST OSCAL versions of 800-53 from their GitHub site
- Cleaned the Excel file - control numbers did not match in format between the Excel version and JSON.  Did some substitution string manipulation to make the control numbers exactly match so the data could be programmatically merged
- Converted the Excel file to JSON using free online tools
- Enriched the Excel file data with additional data from the NIST OSCAL JSON
- Loaded the full catalog from NIST 800-53 Rev 5 into Atlasity
- Loaded the Low, Moderate, High, and Privacy baselines into Atlasity based on the OSCAL profiles
- Published derived JSON files for further use by others
- Documented issues encountered in the process to provide feedback to the NIST OSCAL team and ATARC

## Run the Script

Setup - you will need the following Atlasity items to run this script:

- You must have a running version of Atlasity and have created a user with the appropriate permissions to create security plans
- Verify you are able to log into Atlasity using your username and password
- Ensure you have Python installed on your machine and use `pip` to install the required packages

To load the SSP using OSCAL, run the script below:

`py importer.py --user 'howieavp' --password 'myPassword'`

As this tool runs, it will provide logs as telemetry to show progress as the job completes.  Depending on the size of the SSP, this process could take several minutes to complete.

## Feedback for NIST/GovReady

The following feedback is provided to NIST and GovReady for continuous improvement:

- Missing important date information such as date submitted, authorization date, and expiration date
- Roles do not have GUIDs so they cannot easily be related to the responsible parties
- Some of the type and key value pair data would be better if they were enums, especially for components.  A lot of the information provided is relevant to the Atlasity assets module but a lot of fragile custom coding would be required to map the properties of each component.
- In the back matter, most of the links use relative pathing which will not resolve from an external system.  Also, could not load them in Atlasity since they are not valid URLs which is required in Atlasity for validation of Links.  Attachments do not contain any data, just a string of zeros.
- Unclear what to do with "New Control Stuff" in the metadata section.  Does not feel like part of OSCAL but a ton of content is in there.

NOTE: This is a limited scope test performed using a GovReady output with a small amount of sample data versus a full SSP.

## Atlasity Gaps for OSCAL

- Move Created By fields into the API versus as part of the client application
- No logical representation of locations in the system
- Loading responsible parties is difficult.  Atlasity responsible parties (AO, System Owner, ISSO, etc.) are licensed users in our system.  In the provided OSCAL, there is no good way to map those users as there are no primary keys that match and they may not be actual users of the system.  
- Need a concept in Atlasity for components to allow the grouping of assets to the system inventory
- OSCAL file references an import profile but we didn't have access to it.  We did a soft mapping against a plan that leverage the NIST 800-53 Rev5 Moderate baseline (which was previously imported via OSCAL)
- We didn't have another OSCAL file for the leveraged authorization.  We mocked that up by hard coding a parent SSP in Atlasity to mimic the effect of a leveraged authorization.
- Metadata and System Characteristics have different system names and descriptions.  Used the metadata section as it seemed more accurate.

## To Do List

The following future enhancements might be considered:

- Add a step up front to validate the OSCAL file against the standard prior to import
- Add an Atlasity OSCAL export option and validate that OSCAL file against the standard


