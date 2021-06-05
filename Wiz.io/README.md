# Wiz.io Integration - Assessment Results Loader

This repository contains example Python scripts for integrating compliance assessment results from Wiz.io to update Atlasity security plans that are based on the NIST Cyber Security Framework (CSF).

## Purpose

Atlasity customers are increasingly looking to automate their compliance reporting.  With the rise of cloud computing, customers are leveraging leading cloud security posture management tools such as Wiz.io to manage and assess the security of their cloud infrastructure.  Our goals for this integration included:

- Generating an export of compliance data from Wiz.io in JSON readable files
- Parsing and mapping the Wiz output to the Atlasity data structure 
- Generating automated assessments in Atlasity and attaching evidence from Wiz
- Updating the status of security controls based on the assessment results

At the end of this integration, Wiz/Atlasity joint customers can periodically assess their platform with Wiz and then leverage this script to auto-update their security documentation to ensure that compliance paperwork is in sync with the real-time reality of the security posture.  This approach:

- Lowers costs by eliminating the need to manually assess
- Reduces risk by detecting compliance issues closer to real-time 
- Improves speed by allowing any changes to auto-populate the paperwork during the next integration run

## Background

Wiz is a new approach to cloud security that finds the most critical risks and infiltration vectors with complete coverage across the full stack of multi-cloud environments. [Learn More](https://wiz.io)

## Execute the Script

To process the Wiz.io files and upload to Atlasity, run the following script:

- `py importer.py --user 'AtlasityUserName' --pwd 'YourPassword' --planID 107`
- NOTE: Source files from Wiz must be in the wiz-results folder
- NOTE: Log in with your Atlasity credentials and provide the relevant security plan ID