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

- Obtained an example SSP from GovReady as a JSON file in OSCAL format
- Parsed the file with a Python script to map the data to the Atlasity schema
- Uploaded the SSP and control implementations to Atlasity leveraging the platform's REST APIs
- Mapped to a previously loaded OSCAL Profile for NIST 800-53 Rev4 MODERATE

## Run the Script

Setup - you will need the following Atlasity items to run this script:

- You must have a running version of Atlasity and have created a user with the appropriate permissions to create security plans
- You must update the URL in the script to point to your running instance of Atlasity
- Verify you are able to log into Atlasity using your username and password
- Ensure you have Python installed on your machine and use `pip` to install the required packages
- You must have loaded a catalog into Atlasity containing the security controls that are relevant for this SSP (replace the `00` below with the actual catalog number within Atlasity).  **NOTE** - our previous work on loading Profiles via OSCAL would obviate this step if we integrated the script to dynamically load the profiles based on the provided profile link.

To load the SSP using OSCAL, run the script below:

`py importer.py --user 'yourusername' --pwd 'myPassword' --catalog 00`

- You need to provide your Atlasity username
- Enter your Atlasity password
- Enter the ID of the catalog that contains the control set in the SSP you are uploading (int the case, it was NIST 800-53 rev5 MODERATE)

As this tool runs, it will provide logs as telemetry to show progress as the job completes.  Depending on the size of the SSP, this process could take several minutes to complete.

## Change Log

### [20210126] 

### Added

- Added "Component" to the data model in Atlasity
- Added "Parameter" to the data model in Atlasity
- Updated Python script to map OSCAL SSP properties to the Component and Parameter objects in Atlasity
- Updated to add "if/else" checks for optional fields in the OSCAL Specification (NOTE: Focused on import of the SSP, not all OSCAL fields are currently parsed)

## Feedback for NIST/GovReady

The following feedback is provided to NIST and GovReady for continuous improvement (and to indicate areas where we got stuck/confused and may require additional clarification):

- OSCAL file references an `import-profile` but we didn't have access to it since it was a localhost HREF.  We used our previously loaded NIST 800-53 REV4 MODERATE profile as the baseline catalog for this SSP.

**BOTTOM LINE:** We were able to successfully load a SSP into Atlasity using the OSCAL SSP file.  

**LOE:** ~36 hours to complete the mapping from GovReady to Atlasity using the OSCAL SSP format, including multiple enhancements.

**NOTE:** This is a limited scope test performed using a GovReady output with a small amount of sample data versus a full SSP.

## Atlasity Gaps for OSCAL

- No logical representation of multiple locations in the system (only a single location per SSP in Atlasity)
- Loading responsible parties is difficult.  Atlasity responsible parties (AO, System Owner, ISSO, etc.) are licensed users in our system.  In the provided OSCAL, there is no good way to map those users as there are no primary keys that match and they may not be actual users of the system.  In addition, many users are listed as roles versus actual people which doesn't map well to our stakeholders field.
- We didn't have another OSCAL file for the leveraged authorization.  We mocked that up by hard coding a parent SSP in Atlasity to mimic the effect of a leveraged authorization.  Atlasity leverages inheritance natively to model leveraged authorizations.

## To Do List

The following future enhancements might be considered for future work based on community interest:

- Add a step up front to validate the OSCAL file against the standard prior to import
- Add an Atlasity OSCAL export option and validate that OSCAL file against the standard (round trip the other way)
- Lookup component name via GUID for inventory table
- Metadata - process stakeholders and responsible parties into their equivalent in Atlasity
- Process location data
- Replace \n with <br/> for HTML representation in Atlasity
- Add component lookup for control implementations
- Add checks for all optional OSCAL fields for full parsing
- Add links to the "Links" subsystem in Atlasity

## Results

The following file is offered showing the results of the OSCAL SSP import into Atlasity:

- See [Atlasity Imported OSCAL SSP](Atlasity-SSP-Imported.pdf)
- Local file name: `Atlasity-SSP-Imported.pdf`


