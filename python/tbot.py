#/root/.venv/bin/python
import telepot
import time
import urllib3
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os
from subprocess import Popen
import re

# You can leave this bit out if you're using a paid PythonAnywhere account
'''proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts
'''
bot = telepot.Bot('YOUR_TOKEN')

rkm = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Yes"), KeyboardButton(text="No")]])

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)

#    if content_type == 'text':
#        bot.sendMessage(chat_id, "You said '{}'".format(msg["text"]))
	if content_type == 'text':
		if msg['text'] == 'c':
			bot.sendMessage(chat_id, "Customs", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="TEST"), KeyboardButton(text="Close")]]))
		if msg['text'] == 'Close':
			bot.sendMessage(chat_id, "Closed", reply_markup=ReplyKeyboardRemove())
		if validate_ip(msg['text']):
			bot.sendMessage(chat_id, "Select what you want to do :"+msg['text'], reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Port check:"+msg['text'])], [KeyboardButton(text="Close")]]))
		patt = re.compile('^Port check')
		if patt.match(msg['text']):
			tmp = ping_test(msg['text'])
			bot.sendMessage(chat_id, tmp)
		if msg['text'].startswith('dig'):
			dmn = msg['text'][4:]
			res = os.popen("sh [SCRIPT_LOCATION]gatest.sh "+dmn).read()
			bot.sendMessage(chat_id, res)
			

def validate_ip(ip):
	tmp = ip.split('.')
	if len(tmp) != 4:
		return False
	for i in tmp:
		if not i.isdigit():
			return False
		n = int(i)
		if n < 0 or n > 255:
			return False
	return True

def ping_test(ip):
	#os.popen("yum install -y nc")
	return os.popen("nc -vz "+ip[11:]+" 8080").read().strip()

bot.message_loop(handle)

print ('Listening ...')
# Keep the program running.
while 1:
	time.sleep(10)
