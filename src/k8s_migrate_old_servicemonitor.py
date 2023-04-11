from kubernetes import client, config
from openshift.dynamic import DynamicClient
import yaml
import logging

logging.captureWarnings(True)

k8s_client = config.new_client_from_config(".kube/config")
dyn_client = DynamicClient(k8s_client)
sm_object = dyn_client.resources.get(api_version='v1', kind='ServiceMonitor')
sm_list = dyn_client.get(sm_object,namespace='openshift-monitoring')

sm_template = """
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    k8s-app: __DC__
  name: __DC__-monitor-borrar
spec:
  endpoints:
  - interval: 30s
    path: __PATH__
    targetPort: __PORT__
  namespaceSelector:
    matchNames:
    - __NS__
  selector:
    matchLabels:
      app: __DC__
"""

for s in sm_list.items:
    if 'matchNames' in s['spec']['namespaceSelector'].keys() and 'matchLabels' in s['spec']['selector'].keys():
        for i in s['spec']['namespaceSelector']['matchNames']:
            
            if 'openshift' in i or 'kube-system' in i:
                pass
            else:
                if s['spec']['selector']['matchLabels']['app'] == '':
                    logging.warn("Skipping because label is empty " + s['metadata']['name'])
                    pass
                
                ns = s['spec']['namespaceSelector']['matchNames'][0]
                sm_data = sm_template

                sm_data = sm_data.replace("__DC__", s['spec']['selector']['matchLabels']['app'])
                sm_data = sm_data.replace("__NS__", ns)
                sm_data = sm_data.replace("__PATH__", s['spec']['endpoints'][0]['path'])
                sm_data = sm_data.replace("__PORT__", str(s['spec']['endpoints'][0]['targetPort']))
    
                sm_data = yaml.load(sm_data)
                logging.info("Setting " + str(sm_data))

                try:
                    resp = sm_object.create(body=sm_data, namespace=ns)
                    logging.info("Created " + resp.metadata)

                except Exception as e:
                    logging.error(e)

print("End")