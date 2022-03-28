import os
import json

# create public key
create_pub_key = os.popen("ssh-keygen -y -f /var/lib/geofront/id_rsa > /var/lib/geofront/id_rsa.pub").read()

with open("/opt/geofront/server/server.json", 'r') as f:
        ds = json.load(f)

hosts = list()
for k, v in ds.items():
        hosts.append(k)

pw = os.environ['REMOTE_PW']
epw = os.environ['REMOTE2_PW']
# start coping to remote authorized_key
for host in hosts:
        remote = ds[host]["account"] + "@" + ds[host]["ip"]
        try:
                if 'edge' in host:
                        cmd = "sh /ssh-copy-id.sh " + remote + " " + epw
                else:
                        cmd = "sh /ssh-copy-id.sh " + remote + " " + pw
                print("Executing ssh-copy-id on: " + host)
                exec_cmd = os.popen(cmd).read()
        except:
                e = os.popen("echo " + remote + " >> /failed_ssh_host.log").read()
                print("Exception error: check /failed_ssh_host.log")

date = os.popen("date").read()
print(date)
