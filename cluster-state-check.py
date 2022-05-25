import requests
import json
import configparser, time

config1 = configparser.ConfigParser()
config1.read('config.ini') #load config

headers = {"Authorization": config1['rancher']['token']}

rancher_ip = config1['rancher']['server-ip']
cluster_id = config1['rancher']['cluster-id']
config = {
    "name":config1['cluster']['cluster1-name']
}
cluster_state = ''
server_url = f'https://{rancher_ip}/v3/clusters/{cluster_id}'
try:
    response=requests.get(server_url,json=config, headers=headers,verify=False)
    import_data=json.loads(response.text)
    # print(response.text)
    print(response.status_code)
    cluster_state=import_data["state"]
    while(cluster_state !='active' ):
        response=requests.get(server_url,json=config, headers=headers,verify=False)
        import_data=json.loads(response.text)
        # print(response.text)
        cluster_state=import_data["state"]
        print(import_data["state"])
        print(response.status_code)
        time.sleep(5)
except:
    print(response.text)
    print(response.status_code)
