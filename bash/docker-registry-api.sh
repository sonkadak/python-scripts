#!/bin/bash
registry='https://localhost'
auth='USER:PASS'
repo='REPO_NAME'

res=$(curl -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -u $auth $registry/v2/$repo/tags/list |jq '.tags')
echo ${res[1]}
curl -v -sSL -X DELETE "https://${registry}/v2/${name}/manifests/$(
    curl -sSL -I \
        -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
        "http://${registry}/v2/${name}/manifests/$(
            curl -sSL "http://${registry}/v2/${name}/tags/list" | jq -r '.tags[0]'
        )" \
    | awk '$1 == "Docker-Content-Digest:" { print $2 }' \
    | tr -d $'\r' \
)"

curl -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -u $auth $registry/v2/$1/tags/list |jq
