#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 09:29:10 2020

Tutorials from here:
    https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst

@author: ajones
"""

import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x1C40, idProduct=0x0432)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('test')


#import usb.core
#
#dev = usb.core.find(idVendor=0x1C40, idProduct=0x0432)
#if dev is None:
#    raise ValueError('Our device is not connected')
