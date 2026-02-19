
# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example scans for any BLE advertisements and prints one advertisement and one scan response
# from every device found. This scan is more detailed than the simple test because it includes
# specialty advertising types.

from adafruit_ble import BLERadio

import adafruit_ble.advertising
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
print("scanning")
found = set()
scan_responses = set()
# By providing Advertisement as well we include everything, not just specific advertisements.
for advertisement in ble.start_scan(ProvideServicesAdvertisement):
    addr = advertisement.address
    svcs = advertisement.services
    if advertisement.scan_response and addr not in scan_responses:
        scan_responses.add(addr)
    elif not advertisement.scan_response and addr not in found:
        found.add(addr)
    else:
        continue
    print(addr, advertisement)
    print("\t" + repr(advertisement))
    print("\t" + repr(svcs))
    print("\t" + repr(adafruit_ble.advertising.decode_data(b"\x11\x06\x9e\xca\xdc\x24\x0e\xe5\xa9\xe0\x93\xf3\xa3\xb5\x01\x00\x40\x6e\x02\x01\x06")))
    print()

print("scan done")