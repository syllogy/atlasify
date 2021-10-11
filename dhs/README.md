# DHS 4300A Parser

This Atlasify integration parses the Department of Homeland Security (DHS) 4300 Sensitive Systems Handbook Version 12 into a machine readable format.

## Purpose

This repository digitizes the DHS 4300A using the following methodology:

- PDF is loaded and parsed to extract the data
- Data is ingested into Atlasity (mostly via manual means)
- Data is exported from Atlasity into multiple JSON formats
- Machine readable version of DHS 4300A is now freely available for use by others

## In This Repository

- Python code for parsing the PDF
- Source DHS 4300A PDF
- Converted files using Adobe Cloud to RTF, Excel, and Word formats
- Converted catalog files in Atlasity, including:
    - DHS-4300A - file for loading catalog into an Atlasity instance
    - OSCAL-Catalog-DHS-4300A - NIST OSCAL representation of the DHS catalog in machine readable format

## Pre-Requisites

- Install external libraries using PIP

`pip install PyPDF2`

## Running the Python Script

- `py parser.py`