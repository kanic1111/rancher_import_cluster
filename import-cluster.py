import requests
import json
import configparser, time

config1 = configparser.ConfigParser()
config1.read('config.ini') #load config

headers = {"Authorization": config1['rancher']['token']}
rancher_ip = config1['rancher']['server-ip']
config = {
    "name":config1['cluster']['cluster1-name']
}
server_url = f'https://{rancher_ip}/v3/clusters'

try:
    response=requests.post(server_url,json=config, headers=headers,verify=False) # create cluster
    cluster_info=json.loads(response.text)
    cluster_url=cluster_info["links"]['self']
    time.sleep(3)
    print(response.text)
    # print(response.status_code)
    cluster_id= cluster_url.replace( server_url+'/','')
    config1['rancher']['cluster-id'] = cluster_id
    with open('config.ini', 'w') as conf:
        config1.write(conf)
    response=requests.get(cluster_url+'/clusterregistrationtokens', headers=headers,verify=False) # get import yaml script 
    import_data=json.loads(response.text)
    import_command=import_data["data"][0]['insecureCommand']
    with open('import_cluster.sh', 'w') as f:
        f.write("ssh $(awk -F \"=\" '/node1-user/ {print $2}' config.ini)@$(awk -F \"=\" '/node1-ip/ {print $2}' config.ini) "+import_command) # write remote import cluster script 
except:
    print(response.text)
    print(response.status_code)

