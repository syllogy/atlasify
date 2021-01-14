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

## Run the Script

Setup - you will need the following Atlasity items to run this script:

- You must have a running version of Atlasity and have created a user with the appropriate permissions to create security plans
- You must update the URL in the script to point to your running instance of Atlasity
- Verify you are able to log into Atlasity using your username and password
- Ensure you have Python installed on your machine and use `pip` to install the required packages
- You must have loaded a catalog into Atlasity containing the security controls that are relevant for this ISSP (replace the `00` below with the actual catalog number within Atlasity).  **NOTE** - our previous work on loading Profiles via OSCAL would obviate this step if we integrated the script to dynamically load the profiles based on the provided profile link.

To load the SSP using OSCAL, run the script below:

`py importer.py --user 'yourusername' --pwd 'myPassword' --catalog 00`

- You need to provide your Atlasity username
- Enter your Atlasity password
- Enter the ID of the catalog that contains the control set in the SSP you are uploading (int the case, it was NIST 800-53 rev5 MODERATE)

As this tool runs, it will provide logs as telemetry to show progress as the job completes.  Depending on the size of the SSP, this process could take several minutes to complete.

## Feedback for NIST/GovReady

The following feedback is provided to NIST and GovReady for continuous improvement (and to indicate areas where we got stuck/confused and may require additional clarification):

- OSCAL file references an `import-profile` but we didn't have access to it.  We did a soft mapping against a plan that leveraged the NIST 800-53 Rev5 Moderate baseline (which was previously imported via OSCAL) to complete this POC.  All controls resolved using this catalog. **UPDATE:** - after further investigation, the UUID references a link later in the document.  However, we missed that on the first pass as the lookup included the `#` sign so it didn't find it on lookup.
- Missing important date information such as date submitted, authorization date, and expiration date
- Roles do not have GUIDs so they cannot easily be related to the responsible parties
- Some of the type and key value pair data would be better if they were enums, especially for components.  A lot of the information provided is relevant to the Atlasity assets module but a lot of fragile custom coding would be required to map the properties of each component.
- In the back matter, most of the links use relative pathing which will not resolve from an external system.  Also, could not load them in Atlasity since they are not valid URLs which is required in Atlasity for validation of Links.  Attachments do not contain any data, just a string of zeros.  If relative URLs, the files should be provided as well with the OSCAL file (maybe in a ZIP file) for bulk processing.
- Unclear what to do with "New Control Stuff" in the metadata section.  Does not feel like part of OSCAL but a ton of content is in there.
- UUIDs are not handled consistently.  On some areas of the ISSP, the 'uuid' is a field with a value.  In system characteristics and other areas of the SSP, it assigns the uuids as the name of the object.  This results in increased nesting and code to parse.  You can't just count on the structure to be there so each section required coding to process how it was setup versus a general/consistent processing routing.
- Authorization Boundary, Network Architecture, and Data Flow present their 'diagrams' property as an object.  Recommend that it be an array of objects and flatten by having each diagram have a UUID property (as noted in feedback item above).  Also, caption seems redundant to the description field on each diagram.
- System Implementation - users should be an array of objects, also uses UUIDs as object names versus properties
- System Implementation - components should be an array of objects, also uses UUIDs as object names versus properties
- System Implementation - system inventory should have inventory items be an array, also uses UUIDs as object names versus properties.  'system-inventory' and 'inventory-items' seem redundant.  Unless some metadata is provided at the system inventory level, don't see the distinction being necessary.
- System Implementation - status and state appear redundant for components.  Same issue with with the need for an array and GUID as a property.
- Control Implementation - UUIDs for the controls are not found in components or inventory.
- Control Implementation - for the "by-components" section, it is confusing why the object name is a UUID then the object has a different UUID within it that doesn't tie to any actual component or inventory item.  
- Metadata and System Characteristics have different system names and descriptions.  Used the metadata section as it seemed more accurate.

**NOTE** - this feedback is based solely on the initial input file provided for parsing.  Upon subsequent discussions, there was an issue with the GovReady export and some/many issues may resolve on the next provided file.

**BOTTOM LINE:** We were able to successfully load a SSP into Atlasity using the OSCAL SSP file.  However, there are still data consistency issues and and some variability that result in a high degree of custom mapping work for the portability use case.

**LOE:** ~30 hours to complete the mapping from GovReady to Atlasity using the OSCAL SSP format.

**NOTE:** This is a limited scope test performed using a GovReady output with a small amount of sample data versus a full SSP.

## Atlasity Gaps for OSCAL

- No logical representation of multiple locations in the system (only a single location per SSP in Atlasity)
- Loading responsible parties is difficult.  Atlasity responsible parties (AO, System Owner, ISSO, etc.) are licensed users in our system.  In the provided OSCAL, there is no good way to map those users as there are no primary keys that match and they may not be actual users of the system.  In addition, many users are listed as roles versus actual people which doesn't map well to our stakeholders field.
- Need a concept in Atlasity for components to allow the grouping of assets to the system inventory and related controls.  We don't have this concept represented currently in Atlasity.
- We didn't have another OSCAL file for the leveraged authorization.  We mocked that up by hard coding a parent SSP in Atlasity to mimic the effect of a leveraged authorization.  Atlasity leverage inheritance natively to model leveraged authorizations.

## To Do List

The following future enhancements might be considered for future work based on community interest:

- Add a step up front to validate the OSCAL file against the standard prior to import
- Add an Atlasity OSCAL export option and validate that OSCAL file against the standard (round trip the other way)
- Processing strategy for authorization boundary, network architecture, and data flow
- Lookup component name via GUID for inventory table
- Metadata - process stakeholders and responsible parties into their equivalent in Atlasity
- **Bug** - Figure out what to do with "new-control-stuff" array in metadata - unclear what that is or what to do with it.  Seems to have the most content but isn't part of the OSCAL standard.
- Process location data
- Replace \n with <br/> for HTML representation in Atlasity
- Add component lookup for control implementations

## Results

The following file is offered showing the results of the OSCAL SSP import into Atlasity:

- See [Atlasity Imported OSCAL SSP](Atlasity-SSP-Imported.pdf)
- Local file name: `Atlasity-SSP-Imported.pdf`


