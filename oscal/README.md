# OSCAL Integration - Catalog and Profile Importer

This repository contains example Python scripts for processing NIST OSCAL artifacts and parsing and loading them into Atlasity as catalogues and security controls.

## Purpose

A large number of Atlasity customers, especially government, rely on publications from NIST to build their cyber security programs.  Many Information System Security Plans (ISSPs) are based on NIST related publications.  This repository is focused on processing NIST 800-53 Rev 4 and Rev 5 catalogs/profiles using the tooling published by the NIST OSCAL team.  Our goals included:

- Create Atlasity catalogs using automation by parsing NIST OSCAL files for NIST 800-53 Rev 4 & 5
- Create baselines for Rev 4 Low, Moderate, and High 
- Create baselines for Rev 5 Low, Moderate, High, and Privacy 
- Create applicable FedRAMP baselines

## Background

This work was performed using Open Source code and free tooling in support of the [ATARC Cloud Security Working Group](https://atarc.org/working-groups/cloud-working-group/#:~:text=The%20ATARC%20Cloud%20Working%20Group,the%20Federal%20cloud%20%26%20infrastructure%20community.)

## Process

- Downloaded the NIST OSCAL versions of 800-53 from their [GitHub site](https://github.com/usnistgov/oscal-content) 
- Loaded the full catalog for each version of 800-53 (Rev 4 and 5) using OSCAL
- Loaded each profile/baseline based on these catalogs using OSCAL published Release Candidate (RC) profiles
- Total Level of Effort: ~16 hours

## Run the Script

Setup - you will need the following Atlasity items to run this script:

- Get your user ID and password to log into Atlasity 
- Login via command line to get your JWT token and UserID
- Set your Atlasity URL in the scripts to route API calls to a running Atlasity instance (NOTE: the URLs here leveraged a DEV instance running on localhost)

To load the full catalog, run the script below (NOTE: You must must be an admin or maintainer role and select the proper script (rev 4 or 5)):

`py importer-rev4-catalog.py --user 'username' --pwd 'password'`

- or -

`py importer-rev5-catalog.py --user 'username' --pwd 'password'`

After loading the catalogs, you can then create additional Atlasity catalogs from profiles using the command below (NOTE: pick the appropriate profile importer (rev 4, 5, or FedRAMP)).  Enter the appropriate catalog number from the step above.

`py importer-fedramp-profiles.py --user 'username' --pwd 'password' --catalog '00'`

- or -

`py importer-rev4-profiles.py --user 'username' --pwd 'password' --catalog '00'`

- or -

`py importer-rev5-profiles.py --user 'username' --pwd 'password' --catalog '00'`

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

N/A - this version of the import worked flawlessly based on the release candidate files.
