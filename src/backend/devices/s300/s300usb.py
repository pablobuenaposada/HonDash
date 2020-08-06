#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 10:33:01 2020

@author: pi
"""

import usb
import sys

# Find S300v3
dev = usb.core.find(idVendor = 0x1C40, idProduct = 0x0432)

# Was it found?
if dev is None:
    raise ValueError("S300v3 not found!")
else: print("S300 found")
    
# Set the active configuration. With no arguments, the first
# configurtion will be the active one
#dev.set_configuration()
#
## Get an endppoint instance
#cfg = dev.get_active_configuration()
#intf = cfg[(0,0)]

#Let's gather some info about the S300 configuration:
#@staticmethod
#def _establish_connection(dev):
#    dev.set_configuration()
#    cfg = dev.get_active_configuration()
#    intf = cfg[(0, 0)]
#    entry_point = usb.util.find_descriptor(
#        intf,
#        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
#        == usb.util.ENDPOINT_OUT,
#    )
#    return entry_point
#
#_establish_connection(dev)
#
#for cfg in dev:
#    sys.stdout.write('Config #: ' + \
#                     str(cfg.bConfigurationValue) + '\n')
#    for intf in cfg:
#        sys.stdout.write('\t' + \
#                         'Interface: ' + \
#                         str(intf.bInterfaceNumber) + \
#                         ',' + \
#                         str(intf.bAlternateSetting) + \
#                         '\n')
#        for ep in intf:
#            sys.stdout.write('\t\t' + \
#                             'Endpoint: ' + \
#                             hex(ep.bEndpointAddress) + \
#                             '\n')
#            #Let's test every 16 bit message we can send to the s300 on each endpoint:          
#            for i in range(256):
#                print('\t\t msg: ' + hex(i))
#                dev.write(ep, hex(i))
#                print(dev.read(0x82, 1000))
#Find the entry point:
dev.set_configuration()
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]
entry_point = usb.util.find_descriptor(
        intf,
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
        == usb.util.ENDPOINT_OUT,
    )
print(entry_point)    
    
