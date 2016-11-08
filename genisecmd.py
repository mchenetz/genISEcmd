from netmiko import ConnectHandler
from ciscoconfparse import CiscoConfParse
import sys

noAP= False
allAPs = []
allRouters = []
filteredPorts = []
skip = False
args = sys.argv

if (len(args) < 3):
    print("""Usage: genisecmd.py [ip] [username] [password]""")
    exit(1)


cisco_device = {
    'device_type':'cisco_ios',
    'ip':args[1],
    'username':args[2],
    'password':args[3],
    'secret':args[3]
}

print ("""Cisco ISE Port Configurator
Michael Chenetz 2016
---------------------------------
Usage: genisecmd.py [ip] [username] [password]

""")

net_connect = ConnectHandler(**cisco_device)
net_connect.find_prompt()
net_connect.enable()
output = net_connect.send_command("show run")
wireless = net_connect.send_command("show cdp nei | section include AIR-").splitlines()
arp = net_connect.send_command("sh arp | section Internet").splitlines()
macs = net_connect.send_command("sh mac address-table | section include Gi").splitlines()
for ap in wireless:
    allAPs.append([ap.split()[2]])

for l3 in arp:
    currentMac = (l3.split()[3])
    for mac in macs:
        matchedMac = mac.split()[1]
        if (currentMac == matchedMac):
            macPort = mac.split()[3].split('Gi')[1]
            if macPort not in filteredPorts:
                filteredPorts.append(macPort)
parse = CiscoConfParse(config=str(output).splitlines(), syntax='ios', factory=True)
interfaces = parse.find_objects_w_child('interface Gigabit','switchport mode access')
for int in interfaces:
    for port in filteredPorts:
        if (int.text.endswith(port)):
            skip=True
            break
        else:
            skip=False
            for chap in allAPs:
                if str(int.text).endswith(chap[0]):
                    noAP=False
                    break
                else:
                    noAP=True

    if (noAP == False and skip==False):
        print (int.text)
        print (' authentication event server dead action reinitialize vlan ' + str(int.access_vlan))
        print (' authentication event server dead action authorize voice')
        print (""" authentication event fail action next-method
 authentication host-mode multi-host
 authentication open
 authentication order dot1x mab
 authentication priority dot1x mab
 authentication port-control auto
 mab
 dot1x pae authenticator
 spanning-tree portfast
 shut
 no shut
 """)
        print('!')

    elif(noAP == True and skip == False):
            print (int.text)
            print (' authentication event server dead action reinitialize vlan ' + str(int.access_vlan))
            print (' authentication event server dead action authorize voice')
            print (""" authentication event fail action next-method
 authentication host-mode multi-auth
 authentication open
 authentication order dot1x mab
 authentication priority dot1x mab
 authentication port-control auto
 authentication timer inactivity 30
 mab
 dot1x pae authenticator
 spanning-tree portfast
 shut
 no shut""")
            print ('!')

net_connect.disconnect()
