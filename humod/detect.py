"""Methods helpful for detecting modems on Linux."""

import dbus

BUS_NAME = 'org.freedesktop.Hal'
MGR_OBJ = '/org/freedesktop/Hal/Manager'
HAL_DEV_IFACE = 'org.freedesktop.Hal.Device'
HAL_MGR_IFACE = 'org.freedesktop.Hal.Manager'
BUS = dbus.SystemBus()

def _find_huawei_ports():
    """Find Serial interfaces for Huawei USB modems on a system."""
    # Huawei vendor ID
    vendor_id = '12d1'
    hal_mgr_obj = BUS.get_object(BUS_NAME, MGR_OBJ)
    hal_mgr = dbus.Interface(hal_mgr_obj, HAL_MGR_IFACE)
    all_dev = hal_mgr.FindDeviceByCapability('serial')
    devices = []
    for device in all_dev:
        if vendor_id in device:
            devices.append(device)
    return devices

def _get_hal_info(udi):
    """Return Huawei interface name and short description."""
    hal_dev = BUS.get_object(BUS_NAME, udi)
    dev_property = hal_dev.GetProperty
    serial_port = dev_property('serial.device', dbus_interface=HAL_DEV_IFACE)
    info_product = dev_property('info.product', dbus_interface=HAL_DEV_IFACE)

    return info_product, serial_port

def get_modem_devices():
    """Group serial ports by modem name."""
    modems = {}
    devices = _find_huawei_ports()
    if devices:
        for dev in devices:
            name, port = _get_hal_info(dev)
            if name in modems:
                modems[str(name)].append(str(port))
            else:
                modems[str(name)]=[str(port)]
    else:
        return {}

    return modems

def suggest_devices():
    """Suggests a pair of serial devices (data and control port)."""
    modems = get_modem_devices()
    for mod in modems:
        port_list = modems[mod]
        if len(port_list) >= 2:
            # Data port comes usually first.
            port_list.sort()
            data_port = port_list[0]
            ctrl_port = port_list[-1]
            return (data_port, ctrl_port)
    else:
        return []
