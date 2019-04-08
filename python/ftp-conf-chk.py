from ftplib import FTP

import configparser

ini = configparser.RawConfigParser()
ini.read('ServUDaemon.ini')

# find USER, password, homedir from ServUDaemon.ini
for sec in ini.sections():
    if 'USER' in sec:
        print("USER:",sec[5:-2])
        for k in ini[sec]:
            if k == 'password':
                print("PW: %s" % ini[sec][k])
                # try FTP
                try:
                    # login
                    ftpt = FTP()
                    ftpt.connect('101.79.254.174', 7777)
                    ftpt.login(sec[5:-2], ini[sec][k])
                    ftpt.pwd()
                    # dir test
                    ftpt.mkd('ftptest')
                    ftpt.rmd('ftptest')
                    # upload test
                    f = open('ftptest.png', 'r')
                    ftpt.storbinary('STOR ftptest.png', f)
                    # download test
                    h = open('ftptest.png', 'wb')
                    ftpt.retrbinary('RETR ftptest.png', h.write)
                    # delete test
                    ftpt.delete('ftptest.png')
                    ftpt.quit()
                except:
                    print("FTP Error. Closing FTP")
                    ftpt.close()
            if k == 'homedir':
                print("HOME DIR: %s" % ini[sec][k])

import xml.etree.ElementTree as ET

xml = ET.parse('FileZilla Server.xml')
root = xml.getroot()

# the password is encrypted with salt
# find Name, HomeDIR inf FileZilla Server.xml
for user in root.iter('User'):
    print('User:',user.attrib['Name'])
    for opt in user:
        if opt.tag == 'Permissions':
            for p in opt:
                print('HomeDIR:',p.attrib['Dir'])
