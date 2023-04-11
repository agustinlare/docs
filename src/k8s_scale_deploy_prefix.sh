#!/bin/bash
# bash scale-deployment.sh $PREFIX $REPLICAS
for i in $(kubectl get ns | grep -v kube | grep $1 | grep -v NAME | awk '{print $1}');
do
	kubectl scale --replicas=$2 $(kubectl get deploy -n ${i} -o name) -n ${i}
done