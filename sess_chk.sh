#!/bin/bash
ipaddr=$(hostname -I)
chk=$(netstat -ant |grep EST |wc -l)
msg=$ipaddr' 현재 활성 세션 수: '$chk
bot_token=''
chat_id=
curl -s -o /dev/null "https://api.telegram.org/bot$bot_token/sendmessage?chat_id=$chat_id&text=$msg"

rm -f $0
