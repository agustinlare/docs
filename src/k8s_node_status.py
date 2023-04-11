# cluster.conf example
# [CLUSTER1]
# ENDPOINT = https://KUBERNETESAPIURL:6443
# TOKEN = SOMETOKEN

# [CLUSTER2]
# ENDPOINT = https://KUBERNETESAPIURL:6443
# TOKEN = SOMETOKEN
import urllib.request
import json
import time                 
import ssl                  
import smtplib              
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  
from configparser import ConfigParser   
import sys
import os

def get_all_nodes(endpoint, token, node):         # Esta funcion abre la URL(api) y devuelve todos los nodos con sus detalles.
    """Fetch the nodes data from the openshift cluster"""
    request = urllib.request.Request(endpoint + "/api/v1/nodes/" + node)
    request.add_header('Authorization', 'Bearer ' + token)
    request.add_header('Accept', 'application/json')
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    #ssl_context = None  # or ssl._create_unverified_context() 
    try: 
        result = urllib.request.urlopen(request, context=ssl_context)
        return result.read()
    except urllib.error.URLError: 
        message = 'Se ha producido un Error de URLError en' + endpoint
        send_mail(message)
        exit()
    except urllib.error.HTTPError: 
        message = 'Se ha producido un Error de HTTPError en' + endpoint
        send_mail(message)
        exit()
    except urllib.error.ContentTooShortError: 
        message = 'Se ha producido un Error de ContentTooShortError en' + endpoint
        send_mail(message)
        exit()
    except Exception: 
        message = 'Se ha producido un Error de GenericError en' + endpoint
        send_mail(message)
        exit()  


def send_mail(mensaje):
    strFrom = 'frommail@yourorganization.com'
    strTo = ["somemail@yourorganization.com", "maybeanother@yourorganization.com"]

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Monitoreo Custom de OCP'
    msgRoot['From'] = strFrom
    msgRoot['To'] = ", ".join(strTo)
    msgRoot.preamble = 'Multi-part message in MIME format.'
    
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText(mensaje)
    msgAlternative.attach(msgText)

    msgText = MIMEText('<b>' + mensaje + '<br><img width="546" height="306.8" src="https://cdn.vox-cdn.com/thumbor/e4RVAW3hRA3T9IUR0LqtoRWB0dw=/6x0:895x500/1600x900/cdn.vox-cdn.com/uploads/chorus_image/image/49493993/this-is-fine.0.jpg" alt="Its Fine"><br> ', 'html')
    msgAlternative.attach(msgText)

    server = smtplib.SMTP('relayserver.comh',25)
    server.sendmail(strFrom, strTo, msgRoot.as_string())
    
    server.quit()

    exit(0)

def get_status_from_node(data_item):      
    """ Extract the status conditions from the data"""
    addresses = data_item['status']['addresses']
    address = None
    for addr in addresses:
        if addr['type'] == 'Hostname':
            address = addr['address']
    return {'hostname': address,
            'conditions': data_item['status']['conditions']}

def find_faults(cond_data):               
    """ find whether each node is in a failed state"""
    failures = []
    for node in cond_data:
        hostname = node['hostname']
        for cond in node['conditions']:
            if cond['status'] != "False" and cond['type'] != "Ready":
                if hostname not in failures:
                    failures.append(hostname)
            elif cond['status'] != "True" and cond['type'] == "Ready":
                if hostname not in failures:
                    failures.append(hostname)
    return failures

def checkAgain(node):
    n = json.loads(get_all_nodes(ENDPOINT, TOKEN, node))
    time.sleep(15)
    all_conditions = []
    all_conditions.append(get_status_from_node(n))
    if node in find_faults(all_conditions):
        return True
    else:
        return False


def main():               
    all_conditions = []
    all_nodes = json.loads(get_all_nodes(ENDPOINT, TOKEN, ""))
    for n in all_nodes['items']:
        all_conditions.append(get_status_from_node(n))
    
    fail_nodes = find_faults(all_conditions)
    num_nodes = 0
    list_nodes = ""
    if len(fail_nodes) > 0:
        for f in fail_nodes:
            if checkAgain(f):
                num_nodes = num_nodes + 1
            list_nodes = f + '\n' + list_nodes
    else: 
        sys.exit()

    if num_nodes > 0:
        message = """\
            <html>
                <body>
                    <p>Estado del cluster {}<br>
                    Se encontraron {} nodos en estado failed: 
                    {}<br>
                    </p>
                </body>
                </html>
            """.format(ENDPOINT,num_nodes,list_nodes)
        send_mail(message)

def verificarArg(argumento):
    workingDIR = os.getcwd()
    data_file = workingDIR +'/.clusters.conf'
    config = ConfigParser()
    config.read(data_file)
    if ( argumento in config ):
        endpoint_arg = config[argumento]['ENDPOINT']
        token_arg = config[argumento]['TOKEN']
        return(endpoint_arg,token_arg)
    else:
        return("None")
        

if __name__ == "__main__":
    if (len(sys.argv) - 1) == 1:
        datos_arg = verificarArg(sys.argv[1])
        if (datos_arg == "None"):
            print("You should use an enviroment as an arugment. EJ: clustermonitor.py CLUSTER2")
        else:
            ENDPOINT = datos_arg[0]
            TOKEN = datos_arg[1]
            main()
    else:
        print("You should use an enviroment as an arugment. EJ: clustermonitor.py CLUSTER2")