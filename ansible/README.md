# Atlasify Ansible Playbooks

This directory contains a collection of Ansible code written by C2 Labs as a sample for our Atlasity RegOps platform.

## Purpose

The purpose of this integration is to show Ansible being used to read in assets from Atlasity (using the API), run a series of assessments, and log the results back to Atlasity (using the API). All is done using the open-source version of Atlasity and the POC was actually performed with an Ansible Server and 4 Ubuntu Linux hosts running in containers.

These were the files used for the [demo video](https://www.youtube.com/watch?v=D6uiXtqY5aQ)

## Tasks

Ths script in this directory and the corresponding playbooks/roles do the following:

- Read in a list of assets from Atlasity
- Run compliance checks against those assets tied to 4 different security control implementations (1109, 1110, 1111, and 1113)
- Log an assessment against a given security control implementation for a security plan

## Execution

There are certainly a few edits and settings that will need to take place. While this is not intended to be an all inclusive list, it should give you a good start:

1. Set your Bearer Token as an environment variable on your Ansible Server. This should be named `BEARER_TOKEN`
2. Set an environment variable for the playbook you want to run named `PLAYBOOK`. You could also update `compliance.sh`. `compliance.yml` is the main playbook that really does all the work. A couple others are left as samples.
3. Update `compliance.sh` to point to the appropriate directory for your Ansible Server. This file grabs the list of assets and overwrites the Managed Hosts file. If you do not want to overwrite this file each time, make the appropriate edits here. We are writing them to `/home/ansible-user/assets`.
4. Update `compliance.sh` with the appropriate parent for the assets. We are getting all the assets from Security Plan 13 (line 10).
5. Update `vars/api_info.yml` with the correct:
    - assessor_id: This is the User ID in Atlasity for the person that is conducting the assessment
    - api_baseurl: This is the base URL for the Atlasity install.
    - You also have the ability to put your bearer token in this file if you don't want to read it from an environment variable.
6. Take a look through `compliance.yml`. This file uses the IDs of several control implementations, the desired settings, and more. It has been made very modular, so that it can be used over and over. However, you will need to edit these for your desired use cases. We are running against Security Control Implementations with IDs: 1109, 1110, 1111, and 1113.
7. Peruse some of the other files. They may need some modifications as well, but these should get you well on your way to running and logging assessments from Ansible to Atlasity.

Finally, run `./compliance.sh` to get the assets and run the playbook.
