# OSCAL Integration - Catalog and Profile Importer

This repository contains example Python scripts for processing NIST OSCAL artficacts and parsing and loading them into Atlasity as catalogues and controls.

## Purpose

A large number of Atlasity customers, especially government, rely on publications for NIST to build their cyber security programs.  Many Information System Security Plans (ISSPs) are based on NIST related publications.  In this case, this repository is focused on processing NIST 800-53 Rev 5 using the tooling published by the NIST OSCAL team.  Our goals included:

- Create Atlasity catalogs using automation to parse NIST OSCAL files for NIST 800-53 Rev 5
- Create catalogs for Low, Moderate, High, and Privacy using the same tool
- Fuse data from multiple sources to enrich the catalogs prior to loading (i.e. OSCAL files, 800-53 rev 5 spreadsheet, etc.)

## References

- [NIST OSCAL Website](https://pages.nist.gov/OSCAL/) 
- [NIST OSCAL GitHub Site - OSCAL Content](https://github.com/usnistgov/OSCAL)
- [NIST 800-53 Rev 5 Website](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

## Useful Tools

The JSON files generate by the OSCAL team are large and need easy to visually parse by humans.  We leveraged a free online tool - [JSON Viewer](http://jsonviewer.stack.hu/) - that allows you interactively drill into the data.  This tool was a nice complement for our developers to assist with working on this large data set.  In addition, we used the [Beautify Tools](http://beautifytools.com/excel-to-json-converter.php) to do an Excel to JSON conversion to allow for easier programmatic manipulation of the data.