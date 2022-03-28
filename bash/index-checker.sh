#!/bin/bash
SLACK_URL='URL'

indices='INDEX1 INDEX2'
msg=''

today=$(date +%Y.%m.%d)

msg_format () {
    text="Removed old indices: "$target
    escapedText=$(echo $text | sed 's/"/\"/g' | sed "s/'/\'/g" )
    msg="{\"text\": \"$escapedText\"}"
}

for index in $indices
do
    chk=$(curl -s -o /dev/null -I -w "%{http_code}" "localhost:9200/"$index"-"$today)
    if [ $? -eq "0" ]
    then
        if ! [ $chk -eq "200" ]
        then
            echo $index
            echo $chk
            msg=$msg$index$'\n'
        fi
    else
        #curl -X POST --data-urlencode "payload={\"text\": \"ES Cluster not respond\"}" $SLACK_URL
        echo "ES NOT RESPOND"
    fi
done

echo $msg
