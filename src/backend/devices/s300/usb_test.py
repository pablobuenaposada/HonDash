#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 11:21:45 2020

@author: ajones
"""
#Returns the vendor and product ids of a usb connected device
import sys  
#print(sys.path)
#sys.path.append('/home/pi/pyusb')

import usb

strVendor = ""
strProduct = ""
hexVendor = ""
hexProduct = ""
arrVendor = []
arrProduct = []

#dev = usb.core.find()
dev = usb.core.find(find_all = True)

if dev is None:
    raise ValueError("No USB devices are connected")

#strVendor = str(hex(dev.idVendor))
#strProduct = str(hex(dev.idProduct))

#print("Connected Device Vendor ID: " + strVendor)
#print('\n')
#print("Connected Device Product ID: " + strProduct) 

# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
i = 0

for cfg in dev:
    i = i + 1
    strVendor = str(cfg.idVendor)
    strProduct = str(cfg.idProduct)
    hexVendor = hex(cfg.idVendor)
    hexProduct = hex(cfg.idProduct)
    
#    arrVendor[i] = strVendor
#    arrProduct[i] = strProduct
    
    print(str(i) + ") Decimal VendorID= " + strVendor + " & ProductID= " + strProduct)
    print("Hex VendorID= " + hexVendor + " & ProductId= " + hexProduct + "\n\n")
    
sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')
  
for cfg in dev:
    sys.stdout
    
#testVendor = input("Enter the vendor ID of the device to test: ")
#testProduct = input("Enter the product ID of the device to test: ")

#testSelect = input("Enter the list number of the test device")
#testMessage = input("Enter the test message to send: ")

#print("Sending " + testMessage + " to VendorID " + arrVendor[testSelect] + ", ProductID " + arrProduct[testSelect])


  