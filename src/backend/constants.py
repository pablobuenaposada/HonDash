WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 5678


def websocket_data_dict(
    ecu,
    iat_unit,
    ect_unit,
    vss_unit,
    o2_unit,
    map_unit,
    analog_function,
    time,
    odometer,
    style,
    version,
    logger,
):
    return {
        "bat": ecu.bat,
        "gear": ecu.gear,
        "iat": ecu.iat[iat_unit],
        "tps": ecu.tps,
        "ect": ecu.ect[ect_unit],
        "rpm": ecu.rpm,
        "vss": ecu.vss[vss_unit],
        "o2": ecu.o2[o2_unit],
        "o2_cmd": ecu.o2_cmd[o2_unit],
        "cam": ecu.cam,
        "mil": ecu.mil,
        "fan": ecu.fanc,
        "bksw": ecu.bksw,
        "flr": ecu.flr,
        "vtp": ecu.vtp,
        "vts": ecu.vts,
        "vtec": ecu.vtec,
        "eth": ecu.eth,
        "scs": ecu.scs,
        "fmw": ecu.firmware,
        "map": ecu.map[map_unit],
        "an0": analog_function(0),
        "an1": analog_function(1),
        "an2": analog_function(2),
        "an3": analog_function(3),
        "an4": analog_function(4),
        "an5": analog_function(5),
        "an6": analog_function(6),
        "an7": analog_function(7),
        "time": time,
        "odo": odometer,
        "style": style,
        "name": ecu.name,
        "ver": version,
        "hddlg": logger.active,
    }
