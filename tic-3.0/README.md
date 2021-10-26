# Trusted Internet Connection (TIC) 3.0

This Atlasify integration parses the TIC 3.0 PDF to create multiple digitally readable artifacts and to upload it as a new catalog in Atlasity.

## Purpose

This repository digitizes TIC 3.0 using the following methodology:

- PDF was converted to Word using Adobe cloud
- Controls were pasted from Word into a new spreadsheet
- Controls from the Excel file were enhanced and reformatted
- Excel file was then converted to a JSON representation for ease of machine parsing using [BeautifyTools](http://beautifytools.com/excel-to-json-converter.php), a free online JSON convertor
- A Python script was developed to parse the JSON and load the controls into an Atlasity catalog
- TIC 3.0 catalog was exported as OSCAL 

## In This Repository

- Excel spreadsheet with the full set of TIC 3.0 controls
- JSON file with an easily parsible representation of the spreadsheet above
- OSCAL file of the TIC 3.0 catalog
- Example Python code for parsing the Python to integrate with Atlasity

## Pre-Requisites

- Install external libraries using PIP

`pip install requests`

## Running the Python Script

- `py importer.py --user 'AtlasityUserName' --pwd 'YourPassword'`