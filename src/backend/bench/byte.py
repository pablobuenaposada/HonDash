import usb
import time

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
    
#    i = int(input("enter a dec message to send to S300: "))

    while True:
#        ep.write(bytes([i]))
        ep.write("\x90")
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


                