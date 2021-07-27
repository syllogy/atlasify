# CIS Controls Version 8 

This Atlasify integration parses the Center for Internet Security (CIS) Controls Version 8.0

## Purpose

This repository digitizes the CIS V8 Controls using the following methodology:

- Controls from the Excel file provided by CIS were enchanced and reformatted
- Controls belonging to each Implementation Group (IG-1, IG-2, and IG-3) were separated into respective Excel files
- Excel files were then converted to a JSON representation for ease of machine parsing using [BeautifyTools](http://beautifytools.com/excel-to-json-converter.php), a free online JSON convertor
- A Python script was developed to parse each JSON and load the controls into an Atlasity catalog

## In This Repository

- Excel spreadsheets with CIS Controls corresponding to each implementation group
- JSON file with an easily parsible representation of the spreadsheet above
- Example Python code for parsing the Python to integrate with Atlasity

## Pre-Requisites

- Install external libraries using PIP

`pip install requests`

## Running the Python Script

- Don't forget to put username/password in quotes

- To load a catalog, run the script below (NOTE: pick the proper script (IG-1, IG-2 or IG-3)):

Run on Mac: 
```
# IG-1 Import
$ python3 ig-1-importer.py --user 'AtlasityUserName' --pwd 'YourPassword'

# IG-2 Import
$ python3 ig-2-importer.py --user 'AtlasityUserName' --pwd 'YourPassword'

# IG-3 Import 
$ python3 ig-3-importer.py --user 'AtlasityUserName' --pwd 'YourPassword'
```

Run on Windows:

```
# IG-1 Import
$ py ig-1-importer.py --user 'AtlasityUserName' --pwd 'YourPassword'

# IG-2 Import
$ py ig-2-importer.py --user 'AtlasityUserName' --pwd 'YourPassword'

# IG-3 Import 
$ py ig-3-importer.py --user 'AtlasityUserName' --pwd 'YourPassword'
```
These scripts provide feedback in the terminal to monitor progress on parsing and uploading.  It also performs validation at the end to ensure that all parsed controls are uploaded successfully into Atlasity.

NOTE: This script is a proof of concept for parsing CIS content to load it into an external tool.  Atlasity customers will not need to use this script.  Atlasity has internal mechanisms for importing and exporting catalogs that do not rely on any external tools/scripts. We used this script internally to C2 Labs to load the CIS Controls data but have published relevant catalogues within Atlasity for ease of customer use.

## References

- [Atlasity.io](https://atlasity.io)
- [CIS Controls Navigator](https://www.cisecurity.org/controls/cis-controls-navigator)
- [CIS Controls Home](https://www.cisecurity.org/controls/)
