# Echo server for BLE 
# This device is the peripheral

import board
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_airlift.esp32 import ESP32

esp32 = ESP32()
adapter = esp32.start_bluetooth()
ble = BLERadio(adapter)
print("BLE Radio name:", ble.name)

uart = UARTService()
advert = ProvideServicesAdvertisement(uart)
print("Services provided: ")
for ad in advert.services:
	print("\t- :", ad)

advert.complete_name = "F-nRF52"

if ble.advertising:
	ble.stop_advertising()
while True:
	if not ble.connected:
		if not ble.advertising:
			print("Start Advertising")
			ble.start_advertising(advert)
	if ble.connected:
		# NOTE: if the central disconnects but the device is still awake, it does not disconnect the BLEConnection.
		#       This seems like a bug in the CircuitPython code.
		if ble.advertising:
			print("Stop Advertising")
			ble.stop_advertising()
		# TODO: After a certain amount of time, reset the radio
		#		For some reason, the connection gets stale after a central reset
		#		And the peripheral needs to be restarted.
		for connection in ble.connections:
			print("Check connections for uart service")
			if UARTService not in connection:
				continue
			print("Connection has uart service")
			uart = connection[UARTService]
			print("Connected with central.")
			if uart.in_waiting > 0:
				data = uart.read(uart.in_waiting)
				if data:
					uart.write(data)
					print(data)
				print("bytes remaining:", uart.in_waiting)

