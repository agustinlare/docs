# Requires a TAG_KEY & TAG_VALUE, enviroment variable to search the apropiate resources.
# Enviroment variable ENV=DEBUG prevents correct execution.
import boto3
import os

rds = boto3.client('rds')
dbs = rds.describe_db_instances()

def get_tags_for_db(db):
    instance_arn = db['DBInstanceArn']
    instance_tags = rds.list_tags_for_resource(ResourceName=instance_arn)
    return instance_tags['TagList']

target_db = []

for db in dbs['DBInstances']:
    db_tags = get_tags_for_db(db)
    tag = next(iter(filter(lambda tag: tag['Key'] == 'Environment' and tag['Value'] == os.getenv("TAG_ENV"), db_tags)), None)
    if tag and not db["Engine"].startswith('oracle'):
        target_db.append(db["DBInstanceIdentifier"])

for instance in target_db:
    if os.getenv("ENV") != "DEBUG":
        print("NO DEBUG")
        rds.stop_db_instance(DBInstanceIdentifier=instance)
    else:
        print("rds.stop_db_instance(DBInstanceIdentifier=%s)" % instance)