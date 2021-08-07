# Automated User Creation

This Atlasify integration demonstrates the ability to auto-create a new user and assign them a role programmatically
## Purpose

To allow for efficient scripting of user account creation

## In This Repository

- Example Python code for logging in with an Admin account, creating a user, and assigning a role

## Pre-Requisites

- Install external libraries using PIP
- Login account for this script must have the `administrator` role in Atlasity

`pip install requests`

## Running the Python Script

- `py script.py --user 'AtlasityUserName' --pwd 'YourPassword'`