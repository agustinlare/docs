#!/bin/bash
for POD in $(oc get pods | grep Terminating | awk '{print $1}'); do
  oc delete pods $POD --grace-period=0 --force;
done