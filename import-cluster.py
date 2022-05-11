import requests
import json
import configparser, time

config = configparser.ConfigParser()
config.read('config.ini') #load config

headers = {"Authorization": config['rancher']['token']}
rancher_ip = config['rancher']['server-ip']
config = {
    "name":config['cluster']['cluster1-name']
}
server_url = f'https://{rancher_ip}/v3/clusters'
print(headers)
response=requests.post(server_url,json=config, headers=headers,verify=False) # create cluster
cluster_info=json.loads(response.text)
cluster_url=cluster_info["links"]['self']
time.sleep(3)
response=requests.get(cluster_url+'/clusterregistrationtokens', headers=headers,verify=False) # get import yaml script 
print(response.text)
import_data=json.loads(response.text)
import_command=import_data["data"][0]['insecureCommand']
with open('import_cluster.sh', 'w') as f:
    f.write("ssh $(awk -F \"=\" '/node1-user/ {print $2}' config.ini)@$(awk -F \"=\" '/node1-ip/ {print $2}' config.ini) "+import_command) # write remote import cluster script 
