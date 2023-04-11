#!/bin/bash
# {
#     "fields": {
#        "project":
#        {
#           "key": "PROJECT"
#        },
#        "summary": "TEST",
#        "description": "Creating of an issue using project keys and issue type names using the REST API",
#        "issuetype": {
#           "name": "Error"
#        }
#    }
# }

curl -D- -k -u $USER:$PASSWORD -X POST -d @issue.json -H "Content-Type: application/json" $JIRA_URL/rest/api/2/issue/