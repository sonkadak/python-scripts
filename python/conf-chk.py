import configparser

ini = configparser.RawConfigParser()
ini.read('ServUDaemon.ini')

for sec in ini.sections():
    if 'USER' in sec:
        print("USER:",sec[5:-2])
        for k in ini[sec]:
            if k == 'password':
                print("PW: %s" % ini[sec][k])
            if k == 'homedir':
                print("HOME DIR: %s" % ini[sec][k])

import xml.etree.ElementTree as ET

xml = ET.parse('FileZilla Server.xml')
root = xml.getroot()

for user in root.iter('User'):
    print('User:',user.attrib['Name'])
    for opt in user:
        if opt.tag == 'Permissions':
            for p in opt:
                print('HomeDIR:',p.attrib['Dir'])