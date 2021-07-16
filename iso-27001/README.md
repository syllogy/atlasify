# ISO/IEC 27002:2013 (Version 1a)

This Atlasify integration parses the International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC) titled Information technology – Security techniques – Code of practice for information security controls.

## Purpose

- Controls from the excel file were enhanced and reformatted
- Excel file was then converted to a JSON representation for ease of machine parsing using [BeautifyTools](http://beautifytools.com/excel-to-json-converter.php), a free online JSON convertor
- A Python script was developed to parse the JSON and load the controls into an Atlasity catalog

## In This Repository

- Excel spreadsheet with the full set of ISO/IEC 27002:2013 controls, re-formatted and flattened
- JSON file with an easily parsible representation of the spreadsheet above
- Example Python code for parsing the Python to integrate with Atlasity

## Pre-Requisites

- Install external libraries using PIP

`pip install requests`

## Running the Python Script (on mac)
- `python3 importer.py --user 'AtlasityUserName' --pwd 'YourPassword'`

