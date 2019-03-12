#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
	This python script created on 2018-10-29
'''
import os, signal
import sys
import re				#regex module
from subprocess import PIPE, Popen	#for bash commands
ipaddr = str(os.popen("hostname -I").read().strip())
smport = os.popen("grep Manager /usr/local/ston/server.xml |awk '{print $2}' |tr -dc '0-9'").read()

def END_OF_SCRIPT():
	try:
		os.remove("./fstab.txt")
	except OSError:
		pass
	try:
		os.remove("./df.txt")
	except OSError:
		pass
	try:
		os.remove("./dfh.txt")
	except OSError:
		pass
	try:
		os.remove("./pdisk.txt")
	except OSError:
		pass
	try:
		os.remove("./hotswap.py")
	except OSError:
		pass
	sys.exit()

#Color sets for output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#print bcolors.WARNING + "Text coloring test" + bcolors.ENDC
'''
Create fstab list for /dev/sd*
'''
patt_dev = re.compile('^/dev')
with open('/etc/fstab') as fp:
	f = open("fstab.txt", 'w')
	for line in fp:
		line.strip()
		devp = patt_dev.match(line)
		if devp:
			f.write(line[:8]+"\n")
	f.close()

'''
Create list for "df -h" command result
'''
tmp = os.popen("df -h |grep /dev/sd |grep -v sda").read().strip()
f = open("df.txt", 'w')
f.write(tmp)
f.close()
patt = re.compile('^/dev')
with open('df.txt') as df:
	for line in df:
		line.strip()
		pchk = patt.match(line)
		if pchk:
			f = open("dfh.txt", 'a')
			f.write(line[:8]+"\n")
			f.close()

'''
Compare fstab.txt and dfh.txt
'''
with open('fstab.txt') as f1:
	t1 = f1.read().splitlines()
	t1s = set(t1)
with open('dfh.txt') as f2:
	t2 = f2.read().splitlines()
	t2s = set(t2)

print "Unmounted disk based on /etc/fstab:"
arr = []
for diff in t1s-t2s:
	print bcolors.WARNING + diff + bcolors.ENDC
	arr.append(diff)
if len(arr) == 0:
	print "There is no unmounted disk"
	os.popen("curl -s 'https://api.telegram.org/bot[BOT_TOKEN]/sendmessage?chat_id=[CHAT_ID]&text=교체 대상 디스크 확인 실패: '"+ipaddr)
	END_OF_SCRIPT()

'''
Check physical disk status via omreport
'''
tmp = os.popen("omreport storage pdisk controller=0 |grep -B3 Ready |grep '^ID' |awk '{print $3}'").read().strip()
f = open('pdisk.txt', 'w')
f.write(tmp)
if tmp != "":
	print "Physical disk which is ready:"
	print bcolors.OKGREEN + tmp + bcolors.ENDC
else:
	print "There is no ready disk, clearing foreign config"
	os.popen("omconfig storage controller action=clearforeignconfig controller=0").read().strip()
	tmp = os.popen("omreport storage pdisk controller=0 |grep -B3 Ready |grep '^ID' |awk '{print $3}'").read().strip()
	f.write(tmp)
	print tmp
f.close()

'''
Create VD and make filesystem on them
'''
try:
	tmp = os.popen("omreport storage controller controller=0 |grep 'Preserved Cache' |awk '{print $4}'").read().strip()
	if tmp.lower() == "yes":
		os.popen("omconfig storage controller action=discardpreservedcache controller=0 force=enabled").read()
except:
	print "No preserved cache on controller"
with open('pdisk.txt') as fp:
	for ent in fp:
		tmp = os.popen("omconfig storage controller action=createvdisk controller=0 raid=r0 size=max stripesize=128kb writepolicy=wb diskcachepolicy=disabled readpolicy=ara pdisk="+ent).read().strip()
		signal.signal(signal.SIGPIPE, signal.SIG_DFL)
		patt = re.compile('Command successful')
		if patt.search(tmp):
			print "VD created with PD "+ bcolors.OKGREEN + ent + bcolors.ENDC
		else:
			print bcolors.FAIL + tmp + bcolors.ENDC
			os.popen("curl -s 'https://api.telegram.org/bot[BOT_TOKEN]/sendmessage?chat_id=[CHAT_ID]&text=VD 생성 실패: '"+ipaddr)
			END_OF_SCRIPT()

for dev in arr:
	try:
		sys.stdout.write(os.popen("yes |mkfs.ext4 "+dev).read())
	except:
		print bcolors.FAIL + "Error occured. Please check your /dev/*" + bcolors.ENDC
		os.popen("curl -s 'https://api.telegram.org/bot748707889:AAEcLCva6BKncZNx4_Z-sPBS_pEHFLzwzCY/sendmessage?chat_id=434965238&text=파일 시스템 생성 실패: '"+ipaddr)
		END_OF_SCRIPT()

'''
Catch mount point which is not mounted based on /etc/fstab
'''
arr2 = []
for disk in arr:
	tmp = os.popen("cat /etc/fstab |grep "+disk+" |awk '{print $2}'").read().strip()
	arr2.append(tmp)

'''
Mount disk with STON API
'''
print "Mount point:"
for ent in arr2:
	print  bcolors.BOLD + ent + bcolors.ENDC
for mntpnt in arr2:
	try:
		os.popen("curl http://127.0.0.1:"+smport+"/command/mount?disk="+mntpnt+" > /dev/null 2>&1")
		chk = os.popen("df -h |grep "+mntpnt).read().strip()
		print "Disk mounted on " + bcolors.OKGREEN + mntpnt + bcolors.ENDC
		print "All sequence is done	[ " + bcolors.OKGREEN + "OK" + bcolors.ENDC + " ]"
		print "Please visit "+bcolors.OKBLUE+"STON WM"+bcolors.ENDC
		sys.stdout.write(os.popen("df -h |grep /dev/sd |grep -v sda |sort").read())
		os.popen("curl -s 'https://api.telegram.org/bot[BOT_TOKEN]/sendmessage?chat_id=[CHAT_ID]&text=핫스왑 완료: '"+ipaddr)
	except:
		print bcolors.FAIL + "Somethings gone wrong" + bcolors.ENDC
		print "Please manually mount disk:\nhttp://127.0.0.1:"+smport+"/command/mount?disk=[MOUNT_POINT]\nor Visit STON WM"
		os.popen("curl -s 'https://api.telegram.org/bot[BOT_TOKEN]/sendmessage?chat_id=[CHAT_ID]&text=스톤 디스크 마운트 API 실패: '"+ipaddr)
		END_OF_SCRIPT()

END_OF_SCRIPT()
