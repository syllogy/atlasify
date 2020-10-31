# NIST 800-171 

This Atlasify integration parses the National Institue of Standards and Technology (NIST) Special Publication (SP) 800-171 Revision 2, "Protecting Controlled Unclassified Information (CUI) in Nonfederal Systems and Organizations".  The protection of Controlled Unclassified Information (CUI) resident in nonfederal systems and organizations is of paramount importance to federal agencies and can directly impact the ability of the federal government to successfully conduct its essential missions and functions. This publication provides agencies with recommended security requirements for protecting the confidentiality of CUI when the information is resident in nonfederal systems and organizations; when the nonfederal organization is not collecting or maintaining information on behalf of a federal agency or using or operating a system on behalf of an agency; and where there are no specific safeguarding requirements for protecting the confidentiality of CUI prescribed by the authorizing law, regulation, or governmentwide policy for the CUI category listed in the CUI Registry. The requirements apply to all components of nonfederal systems and organizations that process, store, and/or transmit CUI, or that provide protection for such components. The security requirements are intended for use by federal agencies in contractual vehicles or other agreements established between those agencies and nonfederal organizations.

## Purpose

This repository digitizes the NIST 800-171 regulation using the following methodology:

- Controls were translated to a spreadsheet using a manual copy and paste exercise
- Data was enriched using the Department of Defense (DOD) Assessment Methodology, version 1.2.1, dated June 24, 2020 which includes the weighting for controls
- Excel file was then converted to a JSON representation for ease of machine parsing using [BeautifyTools](http://beautifytools.com/excel-to-json-converter.php), a free online JSON convertor
- A Python script was developed to parse the JSON and load the controls into an Atlasity catalog

## In This Repository

- Excel spreadsheet with the full set of NIST 800-171 controls including the title, description, and control weight
- JSON file with an easily parsible representation of the spreadsheet above
- Example Python code for parsing the Python to integrate with Atlasity

## Pre-Requisites

- Install external libraries using PIP

`pip install requests`

## Running the Python Script

