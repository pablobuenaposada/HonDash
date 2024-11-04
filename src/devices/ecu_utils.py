import usb


def find_device(ids):
    for id in ids:
        device = usb.core.find(idVendor=id["id_vendor"], idProduct=id["id_product"])
        if device:
            version = id["version"]
            return device, version
    return None, None


def establish_connection(device):
    device.set_configuration()
    cfg = device.get_active_configuration()
    intf = cfg[(0, 0)]
    return (
        usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_OUT,
        ),
        intf[0].bEndpointAddress,
    )


def get_value_from_ecu(version, indexes, data, default=0):
    """
    Get the value from the chosen index and data array depending on the current ecu version.
    If something goes wrong return a predefined default value.
    """
    try:
        return data[indexes[version]]
    except (KeyError, IndexError):
        return default
