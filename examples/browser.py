#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of browsing for a service (in this case, HTTP) """

import socket

from six.moves import input

from zeroconf import ServiceBrowser, Zeroconf, InterfaceChoice

import logging
FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger()

class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        logger.info("Service removed: {n}".format(n=name))

    def add_service(self, zeroconf, type, name):
        logger.info("Service added: %s (type is %s)", name, type)
        info = zeroconf.get_service_info(type, name)
        if info:
            logger.info("{name} service info: address={addr}{port}; weight={weight}; priority={pri}; server={server}".format(addr=socket.inet_ntoa(info.address),
                                                                                                                             port=info.port,
                                                                                                                             weight=info.weight,
                                                                                                                             pri=info.priority,
                                                                                                                             server=info.server,
                                                                                                                             name=name,
                                                                                                                         ))
            if info.properties:
                for key, value in info.properties.items():
                    logger.info("{name} property: {k}={v}".format(name=name, k=key, v=value))
        else:
            logger.info("Service has no info")

if __name__ == '__main__':
    zeroconf = Zeroconf(interfaces=InterfaceChoice.All)
    logger.info("Browsing services...")
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    try:
        input("Waiting (press Enter to exit)...\n\n")
    finally:
        zeroconf.close()
    logger.info("Done.")
