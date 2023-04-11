import boto3

client = boto3.client('amplify')
all_domains = []

def get_domain_name(app):
  return client.list_domain_associations(appId=app, maxResults=50)["domainAssociations"][0]["domainName"]

list_apps = client.list_apps(maxResults=100)
for app in list_apps["apps"]:
  print(get_domain_name(app["appId"]))
