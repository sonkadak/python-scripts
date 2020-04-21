#!/usr/bin/python3
import json
import sys
import os
import yaml
import base64


geofront_configmap_dir = "/home/[USER]/geofront/server.json"
'''
server.json
{
            "HOSTNAME": {
                    "account": "ACCOUNT",
                    "ip": "HOST_IP",
                    "group": "devops TEAM1 TEAM2"
            },
            ...
'''

# Kubernetes secret yaml file for pass remote passwords of hosts to deployment
geofront_secret_dir = "/home/[USER]/geofront/geofront-secret.yml"
# kubernetes configmap yaml file
geofront_configmap_yaml = "/home/[USER]/geofront/geofront-configmap.yml"


def define_host(name, ip, acl=""):
    host_name = name
    host_ip = ip
    # default acl
    host_acl = "devops"
    if acl is not "":
        host_acl += " " + acl
    host_info = {"account": "DEFAULT_ACCOUNT", "ip": host_ip, "group": host_acl}

    return host_info

def add_host():
    # create host info data
    hostname = sys.argv[2]
    if len(sys.argv) > 4:
        data = define_host(hostname, sys.argv[3], sys.argv[4])
    else:
        data = define_host(hostname, sys.argv[3])

    # add data and write to the file
    jf[hostname] = data
    print(hostname, jf[hostname])

    return True

def usage():
    print('''Manage geofront-server configuration
USAGE: ./geofront-mgr.py COMMAND OPTION
- Commands
    - add        Add a host: geofront-mgr add HOST IP [ACL] (ACL example: \"team1 team2\")
    - edit       Edit a host: geofront-mgr edit user|ip|acl TARGET_HOST VALUE
                 Default value: user = DEFAULT_USER
                                 acl = devops
                 Edit a hostname: geofront-mgr edit host OLD_HOSTNAME NEW_HOSTNAME
                 If you edit a host info, json file will pop old data and append new data
    - del        Delete a host: geofront-mgr del HOST
    - secret     Update password: geofront-mgr secret HOST_TYPE1|HOST_TYPE2 NEW_PASSWORD
                 NEW_PASSWORD is string
    - show       Show host information: geofront-mgr show HOSTNAME
    - list       List all hosts in configmap
    - help       print this message and exit''')
    sys.exit()

# if edit the hostname, pop the existing data and append new data
def edit_host(select, hostname, value):
    try:
        if jf[hostname]:
            if select == "user":
                jf[hostname]["account"] = value
            if select == "ip":
                jf[hostname]["ip"] = value
            if select == "acl":
                jf[hostname]["group"] = value
            if select == "host":
                for i in jf:
                    if i == hostname:
                        jf[value] = jf.pop(i)
                        hostname = value
            print("Host info changed:")
            print(hostname, jf[hostname])

        return True
    except KeyError:
        print(hostname, ": The host is not exist")
        return False

def del_host(hostname):
    try:
        jf.pop(hostname)
        return True
    except KeyError:
        print(hostname, ": The host is not exist")
        return False

def update_pw(loc, pw):
    print("Update " + geofront_secret_dir)
    os.popen("kubectl get secret -noc-system geofront-secrets -o yaml > " + geofront_secret_dir).read()
    with open(geofront_secret_dir) as y:
        d = yaml.safe_load(y)
    if loc == "HOST_TYPE":
        target = "PW_VARIABLE_NAME"
    new_pw = pw.encode('ascii')
    new_pw_bytes = base64.b64encode(new_pw)
    new_pw_str = new_pw_bytes.decode('ascii')
    d["data"][target] = new_pw_str
    with open('secret.yml', 'w') as y:
        yaml.dump(d, y, default_flow_style=False)

    return 'secret'

def update_on_k8s(target):
    # update geofront configmap
    ans = input("Would you want to update K8S resource with "+target+"? [y/n]")
    if ans == "y" or ans == "Y":
        if 'geofront-secret.yml' in target:
            os.popen("kubectl replace -f " + target).read()
        else:
            os.popen("kubectl delete configmap -nNAMESPACE geofront-config").read()
            os.popen("kubectl create configmap -nNAMESPACE geofront-config --from-file=" + target).read()
        print("Updated on K8s. You should restart geofront-server on K8S")

def renew_config():
    print("Update " + geofront_configmap_dir + "from current data")
    os.popen("kubectl get configmap -nNAMESPACE geofront-config -o yaml > "+geofront_configmap_yaml).read()
    with open(geofront_configmap_yaml) as y:
        yd = yaml.safe_load(y)
    jd = yd["data"]["server.json"]
    with open(geofront_configmap_dir, 'w') as dst:
        for line in jd:
            dst.write(line)

    with open(geofront_configmap_dir, 'r') as j:
        jf = json.load(j)

    return jf

def show_host_info(host):
    print(host, jf[host])
    sys.exit()

def list_hosts():
    for i in jf:
        print(i)
    sys.exit()

try:
    res = 0
    if sys.argv[1] == "secret":
        res = update_pw(sys.argv[2], sys.argv[3])
    else:
        if sys.argv[1] == "help":
            jf = renew_config()
            res = usage()

        # add host
        elif sys.argv[1] == "add":
            jf = renew_config()
            res = add_host()

        # edit host
        elif sys.argv[1] == "edit":
            jf = renew_config()
            res = edit_host(sys.argv[2], sys.argv[3], sys.argv[4])

        # delete host
        elif sys.argv[1] == "del":
            jf = renew_config()
            res = del_host(sys.argv[2])

        # show host information
        elif sys.argv[1] == "show":
            jf = renew_config()
            show_host_info(sys.argv[2])
        elif sys.argv[1] == "list":
            jf = renew_config()
            list_hosts()

        else:
            usage()

        # write to the file
        with open(geofront_configmap_dir, 'w') as j:
            json.dump(jf, j, indent=8)
except IndexError:
    usage()
finally:
    if res is 'secret':
        update_on_k8s(geofront_secret_dir)
    elif res is True:
        update_on_k8s(geofront_configmap_dir)
