import board
import displayio
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from binascii import unhexlify

TARGET = 'e8:9f:6d:d2:74:2a'  # CHANGE TO BLE ADDRESS OF TARGET BILLBOARD
target_address = TARGET.split(":")  # Convert address string to list of bytes
target_address.reverse()  # Reverse bytes to match Address class little-endian
target_address = unhexlify(''.join(target_address))  # Convert list to bytes

ble = BLERadio()
# ble.name = "Billboard Controller"
print("Device BLE identity: ",  ble.name)
# advs = {}
# for adv in ble.start_scan(ProvideServicesAdvertisement, timeout = 5):
# 	print(type(adv))
# 	print("Adv: ", adv)
# 	advs[adv.address] = adv

# display = board.DISPLAY
# clue_group = displayio.Group()

# connected_dot = Circle(220, 220, 5, fill=clue.RED, outline=clue.RED)
# clue_group.append(connected_dot)

# display.show(clue_group)
# display.auto_refresh = True

uart_connection = None
uart_service = UARTService()

# Turn off the neopixel
# clue.pixel.fill(clue.BLACK)


if not uart_connection:
    print("Trying to connect...")
    for adv in ble.start_scan(ProvideServicesAdvertisement):
        print("Advertiser: ", adv.complete_name)
        # if adv.address.address_bytes == target_address:
        if UARTService in adv.services:
            uart_connection = ble.connect(adv)
            print("Connection type:", type(uart_connection))
            print("Connected status:", uart_connection.connected)
            print("Connection interval: ", uart_connection.connection_interval)
            break
    ble.stop_scan()

if uart_connection and uart_connection.connected:
    print("get uart_service")
    # uart_service = uart_connection[UARTService]
    # print(uart_service)
    try:
        print("managed")
        # connected_dot.fill = clue.GREEN
        # connected_dot.outline = clue.GREEN
        print("green dot displayed")
        uart_service = uart_connection[UARTService]
        #uart_service.write(b'n')
        print("uart_service retrieved")
        #uart_connection.disconnect()
        if uart_connection.connected:
            print("connected ..")
        # while uart_connection.connected:
        #     s = input("Eval: ")
        #     uart_service.write(s.encode("utf-8"))
        #     uart_service.write(b'\n')
        #     print(uart_service.readline().decode("utf-8"))
    except Exception as e:
        print("exception:", e)


# while True:
#     # x, y, _ = clue.acceleration
#     pass