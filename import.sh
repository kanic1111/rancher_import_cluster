sudo apt update
export node_user=$(awk -F "=" '/node1-user/ {print $2}' config.ini)
export node_ip=$(awk -F "=" '/node1-ip/ {print $2}' config.ini)
pip3 install requests
python3 import-cluster.py
bash import_cluster.sh
python3 cluster-state-check.py
ssh -t $node_user@$node_ip "bash app-install.sh"
