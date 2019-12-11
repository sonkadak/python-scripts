# python script to edit host group for automatically discovered hosts
# Usage:
# python zabbix-edit-group.py
from pyzabbix import ZabbixAPI


# zabbix API set up
zapi = ZabbixAPI('ZABIX_SERVER_URL')
zapi.session.auth = ('ADMIN', 'PW')
zapi.login('ADMIN', 'PW')

# get info about group 'Linux Auto Registration'
itemlist = zapi.hostgroup.get(output='extend')
group_list = []
for item in itemlist:
    group_list.append(item['name'])
    if 'Linux Auto Registration' == str(item['name']):
        dc_hosts_grp_id = item['groupid']

dc_hosts = zapi.host.get(groupids=dc_hosts_grp_id, output='extend')
dc_hosts_host_ids = []

def update_group(hostid, groupid):
    zapi.hostgroup.massadd(groups=str(groupid), hosts=str(hostid))
    dc_hosts_host_ids.append(h['hostid'])

# print out zabbix host groups
for g in group_list:
    print(str(group_list.index(g)) + '. ' + g)
selected_grp = int(input("Which group do you want to update?"))
print("Start updating host group: ", group_list[selected_grp])

# get hostname pattern from user input
host_patt = input("Enter hostname pattern to add: ")

# add each host to accurate group
for h in dc_hosts:
    for item in itemlist:
        if item['name'] == group_list[selected_grp]:
            if host_patt in str(h['host']).lower():
                update_group(h['hostid'], item['groupid'])

# remove hosts that add accurate groups from the group 'Discovered hosts'
zapi.hostgroup.massremove(groupids=dc_hosts_grp_id, hostids=dc_hosts_host_ids)
