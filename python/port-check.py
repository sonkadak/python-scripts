# check the remote host's port until it open and send message

import socket
import time, datetime
import requests

ipaddr = 'IPADDRESS'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = '''
https://api.telegram.org/bot[BOT_TOKEN]/sendmessage?chat_id=[CHAT_ID]&text='''+ipaddr+''':'''+str(port)+''' opened !
'''
print (datetime.datetime.now())
while True:
    result = sock.connect_ex((ipaddr,port))
    if result == 0:
        requests.get(url)
        break
    time.sleep(30)
