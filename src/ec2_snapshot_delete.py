import boto3

snaps = boto3.client('ec2')

response = snaps.describe_snapshots(
    Filters = [{'Name':'tag:velero.io/schedule-name', 'Values':['k8tkprod-scheduler']}
          ]
)

borrarIds = []

for r in response['Snapshots']:
  for t in r['Tags']:
    if "velero.io/schedule-name" in t['Key'] and 'k8tkprod-scheduler' == t['Value']:
      borrarIds.append(r['SnapshotId'])
      resp = snaps.delete_snapshot(
        SnapshotId=r['SnapshotId']
      )
      

print("Snapshots eliminadas " + str(len(borrarIds)) + ":" + str(borrarIds))