sudo apt update
pip3 install requests
python3 import-cluster.py
bash import_cluster.sh
python3 cluster-state-check.py
ssh $(awk -F "=" '/node1-user/ {print $2}' config.ini)@$(awk -F "=" '/node1-ip/ {print $2}' config.ini) bash app-install.sh
