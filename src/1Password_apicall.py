import requests
import json, sys

token = sys.argv[1]
op_uri = sys.argv[2]

headers = {
  "Authorization": "Bearer %s" % token,
  "Content-Type": "application/json"
}

def get_vault_uid():
  url = "%s%s?name=%s" % (op_uri, "/v1/vaults", "devops")
  response = requests.get(url, headers=headers)
  return json.loads(response.text)[0]["id"]

def get_vault(uid):
  url = "%s%s/%s/items" % (op_uri, "/v1/vaults", uid)
  response = requests.get(url, headers=headers)
  return json.loads(response.text)[0]["id"]

def get_item(uid,itemuid):
  url = "%s%s/%s/items/%s" % (op_uri, "/v1/vaults", uid, itemuid)
  response = requests.get(url, headers=headers)
  return json.loads(response.text)

uid = get_vault_uid()
itemuid = "gbbji244o4riewxhkmwnorqbvi"
print(json.dumps(get_item(uid, itemuid), indent=2))