# remove tags from private docker registry
import requests
import sys
import json


registry = "https://P_REGISTRY_DOMAIN/v2/"
user = 'USER'
pw = 'PW'
try:
    repo = sys.argv[1]
except IndexError as e:
    print('I need a repo name')
    sys.exit()

api_url = registry + repo


def create_session(repo):
    s = requests.Session()
    s.headers.update({'Accept': 'application/vnd.docker.distribution.manifest.v2+json'})

    return s


def delete_all_tags(session):
    tags = s.get(api_url + "/tags/list", auth=(user, pw)).text

    d = json.loads(tags)
    if d['tags'] is not None:
        for i in d["tags"]:
            digest = s.get(api_url + "/manifests/" + i, auth=(user, pw)).headers["Docker-Content-Digest"]
            delete_tag = s.delete(api_url + "/manifests/" + digest, auth=(user, pw))
            print("tag deleted:", i)
        print(s.get(api_url + "/tags/list", auth=(user, pw)).text)
    else:
        print("The repo is empty now.")


if __name__ == "__main__":
    s = create_session(repo)
    delete_all_tags(s)
