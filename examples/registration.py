#!/usr/bin/env python

""" Example of announcing a service (in this case, a fake HTTP server) """

import socket

from six.moves import input

from zeroconf import ServiceInfo, Zeroconf, InterfaceChoice

import logging
FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(name)s%(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger()

desc = {'path': '/~paulsm/'}

info = ServiceInfo("_http._tcp.local.",
                   "Paul's Test Web Site._http._tcp.local.",
                   socket.inet_aton("10.0.1.2"), 80, 0, 0,
                   desc, "ash-2.local.")

zeroconf = Zeroconf(interfaces=InterfaceChoice.All)
logger.info("Registration of a service...")
zeroconf.register_service(info)
try:
    input("Waiting (press Enter to exit)...")
finally:
    logger.info("Unregistering...")
    zeroconf.unregister_service(info)
    zeroconf.close()
    logger.info("Done.")
