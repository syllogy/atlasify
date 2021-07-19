# CMMC Catalog with Objectives

This Atlasify integration parses the CMMC controls at the objective level to allow greater granularity in tracking.

## Purpose

This repository digitizes the CMMC using the following methodology:

- Controls from the Excel file were enhanced and reformatted
- Excel file was then converted to a JSON representation for ease of machine parsing using [BeautifyTools](http://beautifytools.com/excel-to-json-converter.php), a free online JSON convertor
- A Python script was developed to parse the JSON and load the controls into an Atlasity catalog

## In This Repository

- Excel spreadsheet with the full set of CMMC controls, re-formatted and flattened
- JSON file with an easily parsible representation of the spreadsheet above
- Example Python code for parsing the Python to integrate with Atlasity

## Pre-Requisites

- Install external libraries using PIP

`pip install requests`

## Running the Python Script

- `py importer.py --user 'AtlasityUserName' --pwd 'YourPassword'`