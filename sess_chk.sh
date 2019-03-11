#!/bin/bash
ipaddr=$(hostname -I)
chk=$(netstat -ant |grep EST |wc -l)
msg=$ipaddr' 현재 활성 세션 수: '$chk
bot_token='MY_TOKEN'
chat_id=CHAT_ID
curl -s -o /dev/null "https://api.telegram.org/bot$bot_token/sendmessage?chat_id=$chat_id&text=$msg"
if [ -z "$1" ]
then
        max=10
else
        max=$1
fi

while true
do
        chk=$(netstat -ant |grep EST |wc -l)
        if [ $chk -lt $max ]
        then
                msg=$ipaddr'작업 가능! '$max' 미만 현재 활성 세션 수: '$chk
                curl -s -o /dev/null "https://api.telegram.org/bot$bot_token/sendmessage?chat_id=$chat_id&text=$msg"
                break
        fi
done

rm -f $0
