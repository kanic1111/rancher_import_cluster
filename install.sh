sudo docker run -d --restart=unless-stopped   -p 80:80 -p 443:443 --privileged --name rancher  rancher/rancher:v2.6.4 # deploy rancher
sleep 1m # wait rancher to finish init
sudo docker logs  rancher  2>&1 | grep "Bootstrap Password:" # get the random generated default password
