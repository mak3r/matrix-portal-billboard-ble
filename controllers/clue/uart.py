from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_clue import clue
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
a = SolicitServicesAdvertisement()
a.complete_name = "UARTController"
a.solicited_services.append(UARTService)
ble.start_advertising(a)

while not ble.connected:
    pass

print("connected")

while ble.connected:
    for connection in ble.connections:
        if not connection.paired:
            connection.pair()
            print("paired")
        uart = connection[UARTService]
        uart.write(b'n')
    time.sleep(1)

print("disconnected")