#!/usr/bin/env python

# better to use IPs since DNS is unreliable
# set COBBLER_SLAVE=cobbler slave IP when deploying to non SJ site.
# uncomment bottom 2 lines too.
# COBBLER_SLAVE="137.57.142.19"
COBBLER_MASTER="137.57.206.151"

import xmlrpclib
import fcntl, socket, struct
import subprocess
#from subprocess import call

server = xmlrpclib.Server("http://" + COBBLER_MASTER + "/cobbler_api")

#def getHwAddr(ifname): 
#  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#  info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
#  return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

#MAC =  getHwAddr('eth0')
# Or skip the def and just do:
MAC =  subprocess.Popen("/sbin/ifconfig eth0|/bin/awk '/HWaddr/ {print $5}'", stdout=subprocess.PIPE, shell=True).stdout.read()

SYSTEM = server.find_system({"mac":MAC})

URL = "http://%s/cblr/svc/op/nopxe/system/%s" %  (COBBLER_MASTER , SYSTEM[0]) 
# below does not work, why?
# why can't i pass "-O"?: URL = "http://%s/cblr/svc/op/nopxe/system/%s" %  (COBBLER_MASTER , SYSTEM[0]) + " -O /dev/null"

subprocess.call(["/usr/bin/wget", URL])

# uncomment next 2 lines to trigger netboot_enabled toggle "off" on COBBLER_SLAVE
#URL_SLAVE = "http://%s/cblr/svc/op/nopxe/system/%s" %  (COBBLER_SLAVE , SYSTEM[0])
#call(["/usr/bin/wget", URL_SLAVE])
