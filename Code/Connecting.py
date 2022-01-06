import ipaddress
from subprocess import Popen, PIPE

ip_address = ipaddress.ip_network(u'192.168.0.1/24', strict=False)


# looping to find devices connected to network.
for ips in ip_address.hosts():
    ips = str(ips)
    ip_ping = Popen(['ping', '-c', '1', '-W', '50', ips], stdout=PIPE)
    output = ip_ping.communicate()[0]
    drone_live = ip_ping.returncode

    if drone_live == 0:
        print(ips, "Drone is online and connected")
    else:
        print(ips, "Drone is offline")
