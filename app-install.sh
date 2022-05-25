# install helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
# add longhorn repository
helm repo add longhorn https://charts.longhorn.io
helm repo update
# install rancher 
kubectl create namespace longhorn-system
helm install longhorn longhorn/longhorn --namespace longhorn-system
kubectl -n longhorn-system get pod
# install nginx controller
helm repo add nginx-stable https://helm.nginx.com/stable
helm repo update 
helm install my-release nginx-stable/nginx-ingress
# add harbor repository 
helm repo add harbor https://helm.goharbor.io
# install Harbor default using ingress 
helm install my-harbor harbor/harbor 

# change service to NodePort
workload.user.cattle.io/workloadselector apps.deployment-harbor-harbor-nginx
# sed -i 's/  type: ingress/  type: NodePort/g' values.yaml
# sed -i 's/      commonName: ""/      commonName: "core.harbor.domain"/g' values.yaml
# kubectl create ns harbor
# helm install harbor . -n harbor