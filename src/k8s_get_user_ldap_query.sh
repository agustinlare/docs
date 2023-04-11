
#!/bin/bash

PROJECT=$1

ARB=$(oc get rolebinding -o name -n $1 | grep view)

for r in $ARB ; do
    RU=$(oc get ${r} -ojsonpath='{.subjects[*].name}')
    for i in $RU; do
        echo $(ldapsearch -z 0 -H ldap://some-dns.com:389 -w 'PASSWORD' -D "LDAPQUERY" -b "DOMINIO" "(cn=${i})"  sn givenName -LLL | grep 'givenName:\|sn:')
    done
done