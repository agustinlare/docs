import boto3
import requests
import json
import os
import logging
from types import SimpleNamespace
from requests import status_codes


# Boto3 documentacion oficial
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
#
# Glosary
# TM: Tenant Manager like AWS Account
# GM: Grid Manager like IAM AWS User
# env: dev, qa, dmz, prod
# Account: Tenant Account
# Size: En desa y qa, 0=512 1=2gb - prod y dmz, 0=1gb y 5 gb (provider fixed)

# Get configuration from file 
sgrid_conf = os.environ['SGRID_STATIC_CONFIG']
sgrid_cert = os.environ['SGRID_CA_CERTIFICATE']

if os.path.exists(sgrid_conf):
    with open(sgrid_conf, 'r') as f:
        sgrid_conf = json.load(f)
else:
    os.exit(1)

# Create an object with the configuration corresponding to the enviroment
def getEnviroment(env):
    obj = json.loads(
        json.dumps(
            sgrid_conf['enviroment'][env]
        ), 
        object_hook=lambda d: SimpleNamespace(**d)
    )

    return obj

# Get token and if 200 response create a header
def gridToken(grid):
    pload = { 
        "username": grid.user, 
        "password": grid.password, 
        "cookie": True, 
        "csrfToken": False }

    resp = requests.post(
        grid.manager + sgrid_conf['grid']['auth'], 
        json=pload, 
        verify=sgrid_cert
    )

    if resp.status_code != 200:
        raise "Error at login " + resp.reason

    else:
        resp = { 'Authorization': "Bearer " + json.loads(resp.text)['data'] }

    return resp

# Get token fro the tenant and if response 200 create the header
def tenantToken(grid,accountId):
    pload = { 
        "accountId": accountId,
        "username": grid.user,
        "password": grid.password, 
        "cookie": True, 
        "csrfToken": False }

    resp = requests.post(
        grid.manager + sgrid_conf['grid']['auth'],
        json=pload, 
        verify=sgrid_cert
    )

    if resp.status_code != 200:
        raise "Error at login " + resp.reason

    else:
        resp = { 'Authorization': "Bearer " + json.loads(resp.text)['data'] }

    return resp

# Check that account name exists, it has a prefix required by my employer
def getAccountid(grid,name):
    if not name.startswith("t-"):
        name = "t-" + name

    pload = {
        "limit": 1000
    }

    resp = requests.get(
        grid.manager + sgrid_conf['grid']['accounts']['url'],
        headers=gridToken(grid),
        params=pload,
        verify=sgrid_cert
    )

    data = json.loads(resp.text)
    accounts = json.loads(
        json.dumps(data['data']
        ),
        object_hook=lambda d: SimpleNamespace(**d)
    )

    accountId = []
    for a in accounts:
        if a.name == name:
            accountId.append(a.id)
    
    try:
        assert len(accountId) == 1, "Exception encountered, none or more than one account was found. Count was " + str(len(accountId))
    except AssertionError as error:
        logging.warning(error)
        raise error

    return accountId[0]

# Creation of account 
def createAccount(env,name,size):
    grid = getEnviroment(env)

    # Check if exist, the hardest way possible
    try:
        getAccountid(grid,name) # Si no falla es porque encontro uno
        raise Exception("Exception encountered there sould not be any account id corresponding to this name at this time")
    except Exception as e:
        if "0" in str(e):
            logging.info("Exception expected there should not be any account id corresponding to this name at this time") # Si encontro 0 es porque no hay uno con el mismo nombre.
        else:
            logging.info(str(e))
            raise Exception(str(e))
        
    pload = sgrid_conf['grid']['accounts']['json']
    pload['name'] = "t-" + name
    pload['policy']['quotaObjectBytes'] = grid.size[size]

    if env == "prod" and env == "dmz":
        pload['grantRootAccessToGroup'] = "federated-group/grpbucketadmprod"

    resp = requests.post(
        grid.manager + sgrid_conf['grid']['accounts']['url'],
        headers=gridToken(grid),
        json=pload,
        verify=sgrid_cert
    )

    if resp.status_code == 201:
        logging.info(resp)

    return resp

# Create group inside the tenant
def createGroup(env,account,name):
    grid = getEnviroment(env)

    name = "grp-" + name + "-" + grid.prefix
    groups = sgrid_conf['tenant']['groups']

    pload = groups['json']
    pload['displayName'] = name
    pload['uniqueName'] = "group/" + name

    resp = requests.post(
        grid.manager + groups['url'],
        headers=tenantToken(grid,getAccountid(grid,account)),
        json=pload,
        verify=sgrid_cert
    )

    return resp

# Create user inside account
def createUser(env,account,name):
    grid = getEnviroment(env)
    name = "srv-" + name + "-" + grid.prefix
    users = sgrid_conf['tenant']['users']

    pload = users['json']
    pload['fullName'] = name
    pload['uniqueName'] = "user/" + name
    pload['memberOf'] = []

    resp = requests.post(
        grid.manager + users['url'],
        headers=tenantToken(grid,getAccountid(grid,account)),
        json=pload,
        verify=sgrid_cert
    )

    return resp

# Get the user id and its name
def getUser(grid,account,name):
    uri = "/user/"
    if not name.startswith("srv") and not name.endswith(grid.prefix):
        name = "srv-" + name + "-" + grid.prefix
    elif name == grid.user:
        uri = "/federated-user/"

    resp = requests.get(
        grid.manager + sgrid_conf['tenant']['users']['url'] + uri + name,
        headers=tenantToken(grid,getAccountid(grid,account)),
        verify=sgrid_cert
    )

    try:
        assert resp.status_code == 200 or resp.status_code == 302, "User not found"
    except AssertionError as error:
        raise error

    data = json.loads(resp.text)
    user = json.loads(
        json.dumps(data['data']
        ),
        object_hook=lambda d: SimpleNamespace(**d)
    )

    return user.id, user.fullName

# Get the group and json
def getGroup(grid,account,name):
    uri = "/group/"
    if not name.startswith("grp-") and not name.endswith(grid.prefix):
        name = "grp-" + name + "-" + grid.prefix
    elif name == grid.group:
        uri = "/federated-group/"

    resp = requests.get(
        grid.manager + sgrid_conf['tenant']['groups']['url'] + uri + name,
        headers=tenantToken(grid,getAccountid(grid,account)),
        verify=sgrid_cert
    )

    try:
        assert resp.status_code == 200 or resp.status_code == 302, "Group not found"
    except AssertionError as error:
        raise error

    data = json.loads(resp.text)
    group = json.loads(
        json.dumps(
            data['data']
        ),
        object_hook=lambda d: SimpleNamespace(**d)
    )

    return group, data['data']

# Add a local user and groupe for the account
# addUsermember("desa","t-quay","pizarro","fullaccess")
def addUsermember(env,account,group,user):
    grid = getEnviroment(env)

    if not user.startswith("srv-") and not user.endswith(grid.prefix):
        name = "srv-" + user + "-" + grid.prefix

    userid, userName = getUser(grid,account,user)
    users = sgrid_conf['tenant']['users']

    pload = users['json']
    pload['fullName'] = userName
    del pload['uniqueName']

    if type(group) is list:
        for i in group:
            pload['memberOf'].append(getGroup(grid,account,group).id)
    else:
        pload['memberOf'].append(getGroup(grid,account,group)[1]['id'])

    resp = requests.patch(
        grid.manager + sgrid_conf['tenant']['users']['url'] + "/" + userid,
        headers=tenantToken(grid,getAccountid(grid,account)),
        json=pload,
        verify=sgrid_cert
    )

    return resp

# Check that only exists a unique key per user, and if not it gets deleted and create a new one
def checkKey(env,account,userid):
    grid = getEnviroment(env)

    resp = requests.get(
       grid.manager + sgrid_conf['tenant']['users']['url'] + "/" + userid + "/s3-access-keys",
       headers=tenantToken(grid,getAccountid(grid,account)),
       verify=sgrid_cert
    )

    accessIds = json.loads(resp.text)['data']
    if len(accessIds) > 0:

        for id in accessIds:
            resp = requests.delete(
                grid.manager + sgrid_conf['tenant']['users']['url'] + "/" + userid + "/s3-access-keys/" + id['id'],
                headers=tenantToken(grid,getAccountid(grid,account)),
                verify=sgrid_cert
            )

    if resp.status_code == 204 or len(accessIds) > 0:
        logging.info("Se borraron " + str(len(accessIds)) + "access keys")
    elif resp.status_code == 200:
        pass
    else:
        logging.info("Ocurrio una excepcion")
        logging.warn(resp)

# Create an access key for the user inside the tenant
def createAccesskey(env,account,user):
    grid = getEnviroment(env)
    headers = tenantToken(grid,getAccountid(grid,account))
    userid, _ = getUser(grid,account,user)

    checkKey(env,account,userid)

    pload = { }

    resp = requests.post(
       grid.manager + sgrid_conf['tenant']['users']['url'] + "/" + userid + "/s3-access-keys",
       headers=headers,
       json=pload,
       verify=sgrid_cert
    )

    return resp

# Add a policy to new groups for the tenant. This is not a bucket policy
def putPolicy(env,account,group,policy):
    grid = getEnviroment(env)
    group, pload = getGroup(grid,account,group)
    policy = sgrid_conf['tenant']['groups']['policy'][policy]

    pload['policies'].update(policy)

    resp = requests.put(
        grid.manager + sgrid_conf['tenant']['groups']['url'] + "/" + group.id,
        json=pload,
        headers=tenantToken(grid,getAccountid(grid,account)),
        verify=sgrid_cert
    )
    
    return resp


# BOTO3 Client
def s3_client(creds,endpoint):
    return boto3.client('s3',
    aws_access_key_id=creds['X-AWS-ACCESS-KEY-ID'],
    aws_secret_access_key=creds['X-AWS-SECRET-ACCESS-KEY'],
    endpoint_url=endpoint,
    verify=sgrid_cert)

# BOTO3 Resource
def s3_resource(creds,endpoint):
    return boto3.resource('s3',
    aws_access_key_id=creds['X-AWS-ACCESS-KEY-ID'],
    aws_secret_access_key=creds['X-AWS-SECRET-ACCESS-KEY'],
    endpoint_url=endpoint,
    verify=sgrid_cert)

# Create the bucket 
def createBucket(env,creds,name):
    grid = getEnviroment(env)
    s3 = s3_client(creds, grid.tenant)

    name = grid.prefix + "-" + name

    try:
        resp = s3.create_bucket(
            Bucket=name,
            CreateBucketConfiguration={'LocationConstraint': grid.region}
        )

    except Exception as e:
        logging.error(str(e))
        resp = { "status_code": 500, "reason": e.response }

    return resp

# Apply policy to bucket
def applyBucketpolicy(env,creds,name,policy):
    grid = getEnviroment(env)
    s3 = s3_client(creds, grid.tenant)

    resp = s3.put_bucket_policy(
        Bucket=name,
        Policy=policy
    )

    return resp