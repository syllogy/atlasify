# OSCAL Export

This repository contains files to validate Atlasity exports are compliant with the OSCAL JSON schemas using the NIST published schema files.

## Purpose

Atlasity is being adapted to allow its use as a free, community publishing platform for OSCAL content.  Development is underway to fully align Atlasity compliance modules to NIST OSCAL and to allow content created in Atlasity to be exported as OSCAL.  To ensure quality and compliance with the standard, this repository contains sample code and instructions for validating OSCAL JSON exports against NIST schemas.

## Useful Links

- [NIST OSCAL GitHub Repository](https://github.com/usnistgov/OSCAL)
- [AJV Schema Validator CLI](https://www.npmjs.com/package/ajv-cli)

## Validation Steps and Commands

- Install AJV-CLI

`npm install -g ajv-cli`

- Export the OSCAL files you want to validate in Atlasity and save them into the "data" folder

- Run the following command with the appropriate schema ("-s parameter") and data ("-d paramter") to validate the data

`ajv validate -s schemas/oscal_component_schema.json -d data/atlasity-component-export.json`