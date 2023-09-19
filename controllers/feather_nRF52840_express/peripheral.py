# Echo server for BLE 
# This device is the peripheral

import board
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

ble = BLERadio()
uart = UARTService()
advert = ProvideServicesAdvertisement(uart)

while True:
	if not ble.connected:
		if not ble.advertising:
			print("Start Advertising")
			ble.start_advertising(advert)
	if ble.connected:
		if ble.advertising:
			print("Stop Advertising")
			ble.stop_advertising()
		while uart.in_waiting > 0:
			data = uart.read(uart.in_waiting)
			if data:
				uart.write(data)
				print(data)
