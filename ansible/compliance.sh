#!/bin/bash

# PLAYBOOK="/home/ansible-user/playbooks/compliance.yml"

rm -f /home/ansible-user/assets
echo '[managed-hosts]' > /home/ansible-user/assets
echo Environment variables:
printenv
echo Curl results for managed hosts:
curl -X GET "https://atlas.c2labs.com/api/assets/getAllByParent/13/securityPlans" -H "accept: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -s | jq '.[] | .name' | sed 's/"//g'

curl -X GET "https://atlas.c2labs.com/api/assets/getAllByParent/13/securityPlans" -H "accept: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -s | jq '.[] | .name' | sed 's/"//g' >> /home/ansible-user/assets

echo Ansible hosts file
cat /home/ansible-user/assets

ansible-playbook -i /home/ansible-user/assets /home/ansible-user/playbooks/$PLAYBOOK