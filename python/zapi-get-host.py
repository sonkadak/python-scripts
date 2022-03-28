# python script to make 'server.json' for geofront configuration
# server.json format:
# {"HOSTNAME": {"account": "USERNAME", "ip": "IP", "group": "GROUPNAME"}}
from pyzabbix import ZabbixAPI
import json
import os

# zabbix API set up
zapi = ZabbixAPI("https://localhost", user="Admin", password="PASS")
#zapi.session.auth = ('Admin', 'PASS')
#zapi.session.verify = False
#zapi.login("Admin", "PASS")

# get zabbix hostgroup ids
itemlist = zapi.hostgroup.get(output='extend')
groupids = dict()
for item in itemlist:
	groupids.update({item['groupid']: item['name']})

# dictionary for 'server.json'
d = dict()

# excluded zabbix hostgroups that has no availability of ZBX on configuration
excludes = ['SOME SERVERS', 'ETC']

# get hosts
for gid in groupids:
	if groupids.get(gid) not in excludes:
		itemlist = zapi.host.get(groupids=gid, output='extend')

		for item in itemlist:
			item_id = item['hostid']
			item_name = item['name']
	
			ifacelist = zapi.hostinterface.get(output='extend', filter={"hostid": item_id,"main": 1})
			for iface in ifacelist:
				iface_ip = iface['ip']

			# group name value has to be lowercase and replace whitespace to dash(-)
			group_name = groupids.get(gid).lower().replace(" ", "-")

			# update base dict of server list
			d.update({item_name: { "account": "USER", "ip": iface_ip, "group": group_name }})

zapi.user.logout()

with open('serverlist.txt', 'w') as list:
	for ent in d:
		list.write(ent+'\n')
print ("serverlist.txt created")

# write json file
#with open('server.json', 'w') as f:
#	json.dump(d, f, indent=8)
#print ("Server list from Zabbix created: server.json")

#ans = input("Do you want to update hosts file for ansible? (Y/n)")
#if ans == "":
#	ans = "y"
#if ans.lower() == "y":
#	os.popen("python create-ansible-inventory.py")
