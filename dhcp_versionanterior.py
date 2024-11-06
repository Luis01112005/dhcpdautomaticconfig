import os

dhcpconf = 'dhcpd.conf.txt'
security = 'securitydhcpdconf.txt'
grupodesktop = 'grupodesktop.txt'
scgrupodesktop = 'scgrupodesktop.txt'
gruposerver = 'gruposerver.txt'
scgruposerver = 'scgruposerver.txt'
grupowireless = 'grupowireless.txt'
scgrupowireless = 'scgrupowireless.txt'

with open(security, 'r') as scdhcp, open(dhcpconf, 'w') as dhcp, open(scgrupodesktop, 'r') as scgd, open(grupodesktop, 'w') as gd, open(scgruposerver, 'r') as scgs, open(gruposerver, 'w') as gs, open(scgrupowireless, 'r') as scgw, open(grupowireless, 'w') as gw:
    backdhcp = scdhcp.read()
    backwireless = scgw.read()
    backserver = scgs.read()
    backdesktop = scgd.read()
    dhcp.write(backdhcp)
    gw.write(backwireless)
    gs.write(backserver)
    gd.write(backdesktop)

print(os.popen('sudo systemctl stop isc-dhcp-server').read())
print(os.popen('sudo systemctl start isc-dhcp-server').read())
print(os.popen('sudo systemctl status isc-dhcp-server').read())