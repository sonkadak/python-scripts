import os
import shutil
import json
from collections import defaultdict

# read server.json file born from zabbix-get-host.py
with open('server.json', 'r') as f:
    j = json.load(f)

d = defaultdict(list)
groups = list()

for item in j:
    if j[item]["group"] not in groups:
        groups.append(j[item]["group"])

os.remove("server.ini")
inventory_group = ["[oc:children]"]
for group in groups:
    inventory_group.append(group)
    hosts = list()
    for item in j:
        if group == j[item]["group"]:
            if j[item]["ip"] not in hosts:
                hosts.append(item + " ansible_host=" + j[item]["ip"])
    f = open('server.ini', 'a+')
    f.write("[" + group + "]\n")
    for host in hosts:
        f.write(host + "\n")
    f.write("\n")

for ent in inventory_group:
    f.write(ent + "\n")

f.close()

# copy to ansible hosts file
cmd = os.popen("sudo cp server.ini /etc/ansible/hosts")