# rancher install (5/9)

#### install.sh

```bash=
sudo docker run -d --restart=unless-stopped   -p 80:80 -p 443:443 --privileged --name rancher  rancher/rancher:v2.6.4 # deploy rancher
sleep 1m # wait rancher to finish init
sudo docker logs  rancher  2>&1 | grep "Bootstrap Password:" # get the random generated default password

```

### 設定admin密碼與取得金鑰
(要有圖片)
![](https://i.imgur.com/69z1mDz.png)
**這邊打上 docker log 顯示的預設密碼**
![](https://i.imgur.com/nj1zFoG.png)
**密碼限定要12個字元以上**
![](https://i.imgur.com/CTDV16B.png)
**進到homepage後點開右上角的圖示**
![](https://i.imgur.com/CL1eSSf.png)
**選擇Account&API Keys**
![](https://i.imgur.com/kFaqtW3.png)
**進到Account&API Keys後選擇Create API Key**
![](https://i.imgur.com/wxmzdgD.png)
**可設定此API KEY的權限和是否會過期都沒有特別要求就可以按Create**
![](https://i.imgur.com/Kn29ZLA.png)
**這邊可以看到創建的Token 若沒保存的話要再重新申請一個**

#### 創建Cluster

**config.ini.sample**
```bash=
[rancher]
token=Bearer token:token key # token for rancher api service 
server-ip=127.0.0.1 #rancher-server ip
[cluster]
cluster-number=1 #numbers of import cluster
cluster1-name=sample # cluster name shows on rancher
[remote]
node1-user=sample-kanic #username for remote script 
node1-ip=127.0.0.1 # cluster serverip for remote script 

```
**import.sh**
```bash=
sudo apt update
pip3 install requests
python3 import-cluster.py
bash import_cluster.sh
```
**import-cluster.py**
```bash=
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

```
