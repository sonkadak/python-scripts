# python script to make 'server.json' for geofront configuration
from pyzabbix import ZabbixAPI
import json

# zabbix API set up
zapi = ZabbixAPI('ZABBIX_URL')
zapi.session.auth = ('admin', 'PASSWD')
#zapi.session.verify = False
zapi.login('admin', 'PASSWD')

# get zabbix hostgroup ids
itemlist = zapi.hostgroup.get(output='extend')
groupids = dict()
for item in itemlist:
	groupids.update({item['groupid']: item['name']})

# dictionary for create 'server.json'
d = dict()

# excluded zabbix hostgroups that has no availability of ZBX on configuration
excludes = ['NOT_NECESSARY_GROUP_NAME']

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
			# group name value has to be lowercase and replace whitespace with dash(-)
			group_name = groupids.get(gid).lower().replace(" ", "-")
			d.update({item_name: { "account": "ACCOUNT", "ip": iface_ip, "group": group_name }})

zapi.user.logout()

# create hostname list
with open('serverlist.txt', 'w') as list:
	for ent in d:
		list.write(ent+'\n')
print ("serverlist.txt created")

# create json file
with open('server.json', 'w') as f:
	json.dump(d, f, indent=8)
print ("server.json created")
