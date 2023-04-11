# My swiss army knife repo

Things

## Index

- [My swiss army knife repo](#my-swiss-army-knife-repo)
  - [Index](#index)
    - [Docs](#docs)
      - [Kubernetes](#kubernetes)
      - [Amazon](#amazon)
      - [Openshift 4](#openshift-4)
    - [Scripts](#scripts)

### Docs

#### Kubernetes

+ [Kubernetes Best Practices 101](k8s-bestpractices.md)
+ [Best practices to follow for deployment or change management](cicd-best-practices.md)
+ [Liveness, Readiness y Startup probes](k8s-probes/probes.md)
    + [TLDR + Examples](k8s-probes/tldr.md)
+ [OOM Killed JVM Sizing](k8s-oomkill/k8s-ommkill.md)

#### Amazon

+ [AWS Virtual Private Cloud](aws-vpc.md) *EN*
+ [AWS Virtual Private Cloud](aws-vpc-es.md) *ES*
+ [AWS Cloud Practitioner](aws-cloudpratictioner.md)  # Not finished
+ [AWS RDS vs Aurora Comparacion](aws-analisis-rds-vs-aurora.md)
+ [AWS Security Specialist](aws-security-specialist.md) # Not finished


#### Openshift 4

+ RedHat OpenShift Service Mesh EN
    + [Introduction](rhocp-servicemesh/chap1-en.md)
    + [Installation](rhocp-servicemesh/chap2-en.md)
    + [Observing a Service Mesh](rhocp-servicemesh/chap3-en.md)
    + [Controlling Service Traffic](rhocp-servicemesh/chap4-en.md)
    + [Releasing Applications with OpenShift Service Mesh](rhocp-servicemesh/chap5-en.md)
    + [Testing Service Resilience with Chaos Testing](rhocp-servicemesh/chap6-en.md)
    + [Building Resilient Services](rhocp-servicemesh/chap7-en.md)
    + [Securing an OpenShift Service Mesh](rhocp-servicemesh/chap8-en.md)


+ RedHat OpenShift Service Mesh ES
    + [Introduccion](rhocp-servicemesh/chap1-es.md)
    + [Instalacion](rhocp-servicemesh/chap2-es.md)
    + [Observando Service Mesh](rhocp-servicemesh/chap3-es.md)
    + [Controlando Trafico de Servicio](rhocp-servicemesh/chap4-es.md)
    + [Desplegando Aplicaciones con OpenShift Service Mesh](rhocp-servicemesh/chap5-es.md)
    + [Testear Servicios Resilientes con Chaos Testing](rhocp-servicemesh/chap6-es.md)
    + [Creando Servicios Resilientes](rhocp-servicemesh/chap7-es.md)
    + Securitizando OpenShift Service Mesh *Proximamente*

### Scripts

+ [Install aws-cli](./src/awscli_install.sh)
+ [Install mongosh](./src/mongosh_install.sh)
+ [Elasticsearch log overflow search](./src/es_docs_injector.py)
+ [1Password API calls](./src/1Password_apicall.py)
+ [Run all AWS Pipelines](./src/codepipeline_start.sh)
+ [TFC Upload mass env_vars to variableset](./src/terraform_add_varset.py)
+ [Install helm-3.8.2](./src/helm_install.sh)
+ [Stop RDS Instances](./src/rds_stop.py)
+ [Delete AWS EC2 Snapshot by tag](./src/ec2_snapshot_delete.py)
+ [StorageGRID NetApp ABM](./src/storagegrid_usage.py)
+ [Python json to Object](./src/json_2_obj.py)
+ [Delete all Openshift pods in terminating](./src/k8s_delete_terminating_pods.sh)
+ [RH Quay backup](./src/k8s_quay_backup.sh)
+ [Node state email notification](./src/k8s_node_status.py)
+ [Quick python app thing](./src/flask.py)
+ [All in one Pod manifest](./src/pod_testing.yaml)
+ [Awful Bash deploy with Helm and notification to Google Chat](./src/deploy_helm_script.sh)
+ [Scale K8s-deployments of specific prefix](./src/k8s_scale_deploy_prefix.sh)
+ [Postgres script creates user and db](./src/create_project_psql.py)
+ [Migration of documents from S3 Bucket to 1Password-cli ](./src/migrate_s3-2-1Password.py)
+ [Get size of logs within local docker](./src/log_size.sh)
+ [Refresh iptables in case of ip changed](./src/refresh_iptables.sh)
+ [Get all registered domains in amplify](./src/amplify_list_dns.py)
+ [Python remote command](./src/remote_execution.py)
+ [Python check and notify when internet returns](./src/check_internet.py)
