# Arguments: <FILE_PATH>, <VAR_SET>, <TOKEN
# vscode debug: "args": ["./envs.json", "varset-foovar", "TOKEN"]
# Example: 
# {
#  "key": "value",
#  "foo": "var"
# }

import requests
import json, sys

f = open(sys.argv[1])
data = json.load(f)
f.close()

varset = sys.argv[2]
token = sys.argv[3]

headers = {
  "Authorization": "Bearer %s" % token,
  "Content-Type": "application/vnd.api+json"
}

url = "https://app.terraform.io/api/v2/varsets/%s/relationships/vars" % varset
payload = {
  "data": {
    "type": "vars",
    "attributes": {
      "category": "terraform",
      "key": "",
      "value": "",
      "description": "",
      "sensitive": True,
      "hcl": False
    }
  }
}

for d in data:
  payload["data"]["attributes"]["key"] = d
  payload["data"]["attributes"]["value"] = data[d]
  response = requests.post(url, data=json.dumps(payload), headers=headers)
  res = response.json()
  print(res)