import usb

if usb.core.find(idVendor=0x403, idProduct=0xF5F8) is not None:
    dev = usb.core.find(idVendor=0x403, idProduct=0xF5F8)
    version = 2
elif usb.core.find(idVendor=0x1C40, idProduct=0x0434) is not None:  # kpro4
    dev = usb.core.find(idVendor=0x1C40, idProduct=0x0434)
    version = 4
elif usb.core.find(idVendor=0x1C40, idProduct=0x0432) is not None:  # s300v3
    dev = usb.core.find(idVendor=0x1C40, idProduct=0x0432)
    version = 3003

if dev is not None:
    try:
        dev.set_configuration()
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]
        ep = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_OUT,
        )
    except Exception:
        pass

i = bytes([176])
    
while True:
    print(str(i))
    ep.write(i)
#    ep.write("\xb0")
    try:
        if version == 2:
            temp = dev.read(0x81, 10000, 1000)  # kpro2
            print(temp)
            # elif version == 4:
            #     temp = dev.read(0x82, 10000, 1000)  # kpro4
            #     print(temp)
            # ep.write('\x65')
            # if version == 2:
            #     temp = dev.read(0x81, 10000, 1000)  # kpro2
            #     print(temp)
            # elif version == 4:
            #     temp = dev.read(0x82, 128, 1000)  # kpro4
            #     print(temp)
        elif version == 3003:
            temp = dev.read(0x82, 256, 1000)  # s300v3
            print(temp)
        f = open('/home/pi/Desktop/AN_Responses.txt', 'a')
        f.write("Msg: " + str(i) + "\r\n")
        f.write("Reply: \r\n")
        f.write(str(temp))
        f.write("\r\n")
    except:
        print("No Response")
#    time.sleep(.0001)
        
f.close
                