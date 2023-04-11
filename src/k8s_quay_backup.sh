#/bin/bash
POD=$(oc get pods -n quay-enterprise -l quay-enterprise-component=quay-database -o name)
DB=$1_$(date +"%Y_%m_%d").gz
PVCFOLDER=$2
NS="quay-enterprise"

if [ "$1" != '' ]; then
    oc rsh $NS $POD -- pg_dump | gzip > $1
    mv $1 $PVCFOLDER/$1
else
    echo "This script is expected to be executed with 2 args: 1) Database name 2) Path where to leave the backup."
fi