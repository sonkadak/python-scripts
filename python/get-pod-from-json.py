# parse json file
import json

# kubectl get --all-namespaces -o json
with open('pods.json', 'r') as f:
        j = json.load(f)

for i in j["items"]:
        # get pod name
        for k in i["spec"]:
                if k == "volumes":
                        for v in i["spec"]["volumes"]:
                                # volume fstype is ceph
                                if 'flexVolume' in v:
                                        if v['flexVolume']['fsType'] == 'ceph':
                                                print(i["metadata"]["name"])
                                # PVC name has nfs1
                                if 'persistentVolumeClaim' in v:
                                        if "nfs1" in v['persistentVolumeClaim']['claimName']:
                                                print(i["metadata"]["name"])
