# parse json file
import json

# kubectl get --all-namespaces -o json
'''
pods.json
cronjob.json
deploy.json
'''
with open('pod.json', 'r') as f:
        p = json.load(f)

#with open('cronjob.json', 'r') as f:
#        j = json.load(f)
#
#with open('deploy.json', 'r') as f:
#        d = json.load(f)

# for pods.json
print('Pod list')
for i in p["items"]:
        # get pod name
        for k in i["spec"]:
                if k == "volumes":
                        for v in i["spec"]["volumes"]:
                                # volume fstype is ceph
                                if 'flexVolume' in v:
                                        if v['flexVolume']['fsType'] == 'ceph':
                                                print(i["metadata"]["name"])
                                # # PVC name has nfs1
                                # if 'persistentVolumeClaim' in v:
                                #         if "nfs1" in v['persistentVolumeClaim']['claimName']:
                                #                 print(i["metadata"]["name"])

                                # # volume has hostPath
                                # if 'hostPath' in v:
                                #         print(v['hostPath']['path'])


## for cronjob.json
#print('\nCronjob list')
#for i in j["items"]:
#        for k in i["spec"]:
#                if k == "jobTemplate":
#                        for l in i["spec"]["jobTemplate"]:
#                                for m in i["spec"]["jobTemplate"]["spec"]["template"]["spec"]:
#                                        if m == "volumes":
#                                                for n in i["spec"]["jobTemplate"]["spec"]["template"]["spec"]['volumes']:
#                                                        if 'flexVolume' in n:
#                                                                if n["flexVolume"]["fsType"] == 'ceph':
#                                                                        print(i['metadata']['name']+" in "+i['metadata']['namespace'])
#
#
## for deploy
#print('\nDeployment list')
#for i in d["items"]:
#        for k in i["spec"]:
#                if k == 'template':
#                        for l in i['spec']['template']['spec']:
#                                if l == "volumes":
#                                        for m in i['spec']['template']['spec']['volumes']:
#                                                if 'flexVolume' in m:
#                                                        if m["flexVolume"]["fsType"] == 'ceph':
#                                                                print(i['metadata']['name']+" in "+i['metadata']['namespace'])
