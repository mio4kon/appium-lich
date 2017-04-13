# -*- coding: utf-8 -*-
__author__ = 'Mio4kon'
from utils.shell import Shell
from utils import L


class Device:
    @staticmethod
    def get_android_devices():
        android_devices_list = []
        for device in Shell.invoke('adb devices').splitlines():
            if 'device' in device and 'devices' not in device:
                device = device.split('\t')[0]
                android_devices_list.append(device)
        return android_devices_list


if __name__ == '__main__':
    devices = Device.get_android_devices()
    L.i("devices: ", devices)
