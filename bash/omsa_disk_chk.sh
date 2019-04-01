#!/bin/bash
ipaddr=$(hostname -I)
bot_token='[BOT_TOKEN]'
chat_id=[CHAT_ID]

# check predicted failure disks
chk=$(omreport storage pdisk controller=0 |egrep -B7 'Failure Predicted               : Yes' |egrep Name |awk -F': ' '{print $2}')
if [ -z "$chk" ]
then
        echo 'No problem'
else
        msg=$ipaddr' Predicted Failure: '$chk
        curl -s -o /dev/null "https://api.telegram.org/bot$bot_token/sendmessage?chat_id=$chat_id&text=$msg"
fi

# check vdisk status
chk=$(omreport storage vdisk controller=0 |egrep -i -A10 critical |egrep '\/dev' |awk '{print $4}')
if [ -z "$chk" ]
then
        echo 'No problem'
else
        msg=$ipaddr' Critical VDISK: '$chk
        curl -s -o /dev/null "https://api.telegram.org/bot$bot_token/sendmessage?chat_id=$chat_id&text=$msg"
fi
rm -f $0
