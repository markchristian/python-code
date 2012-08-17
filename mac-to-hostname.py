#!/usr/bin/env python

# better to use IPs since DNS is unreliable
# set COBBLER_SLAVE=cobbler slave IP when deploying to non SJ site.
# uncomment bottom 2 lines too.
# COBBLER_SLAVE="137.57.142.19"
COBBLER_MASTER="137.57.206.151"

import xmlrpclib
import subprocess

server = xmlrpclib.Server("http://" + COBBLER_MASTER + "/cobbler_api")

MAC =  subprocess.Popen("/sbin/ifconfig eth0|/bin/awk '/HWaddr/ {print $5}'", stdout=subprocess.PIPE, shell=True).stdout.read()

SYSTEM = server.find_system({"mac":MAC})

URL = "http://%s/cblr/svc/op/nopxe/system/%s" %  (COBBLER_MASTER , SYSTEM[0])  + " -O /dev/null"

subprocess.call(["/usr/bin/wget", URL])

# uncomment next 2 lines to trigger netboot_enabled toggle "off" on COBBLER_SLAVE
#URL_SLAVE = "http://%s/cblr/svc/op/nopxe/system/%s" %  (COBBLER_SLAVE , SYSTEM[0])
#call(["/usr/bin/wget", URL_SLAVE])
