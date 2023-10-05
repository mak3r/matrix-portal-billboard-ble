import time
import random
import displayio
import digitalio
import terminalio
import adafruit_imageload
import board
import gc

from adafruit_ble import BLERadio
from adafruit_ble import Advertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_clue import clue
from adafruit_display_text import label

# for binding with the matrix portal billboard
BILLBOARD_NAME = "F-nRF52"
# # The background at startup before connection
# STARTUP_BG = "hyvlabs.bmp"

# Display Stuff
display = clue.display
disp_group = displayio.Group()
display.show(disp_group)

# Background BMP pre BLE connection
# hyvbmp = displayio.OnDiskBitmap(open(STARTUP_BG, "rb"))
# image = displayio.TileGrid(hyvbmp, pixel_shader=hyvbmp.pixel_shader)
# disp_group.append(image)

# Billboard content shows up here
in_label = label.Label(terminalio.FONT, text='A'*32, scale=2,
                       color=0xFFFFFF)
in_label.anchor_point = (0, 0)
in_label.anchored_position = (5, 12)
disp_group.append(in_label)

# This is the bluetooth low energy connection
ble_connection = None
ble = BLERadio()
# print("BLE Radio name:", ble.name)
uart = None
billboard = None

def parse_data():
    pass

def update_bg():
    pass

def update_label(text=""):
    in_label.text = text
    print(text)
    print("\n")

update_label("[A+B] to scan\nfor billboard")

def clear_connection():
    global uart
    uart = None
    for connection in ble.connections:
        connection.disconnect()

# Scan for advertisements and return the advertisement 
# that matches BILLBOARD_NAME
def scan() -> Advertisement :
    # A completed scan could be from a successful connection
    # or from a scan timeout
    print("Free memory: %s"%str(gc.mem_free()))
    print("Allocated memory: %s"%str(gc.mem_alloc()))
    # this will be assigned to the Advertisement for the billboard we want to connect with
    ad = None
    try:
        # Keeping buffer size low seems to reduce the memory amount attempting to be allocated
        #   Default is 512
        for advert in ble.start_scan(buffer_size=128,timeout=2):
            print(f"{advert=}")
            if advert.complete_name == BILLBOARD_NAME:
                ad = advert
                update_label("Found {} \n{}".format(ad.complete_name, "[A+B] to connect"))
                break
    except Exception as e:
        print(e)

    ble.stop_scan()
    gc.collect()
    return ad


def connect(billboard=None):
    global uart
    if billboard:
        try:
            ble.connect(billboard)
            billboard = None
            for connection in ble.connections:
                if not connection.connected:
                    continue
                # print("Check connections for uart service")
                if UARTService not in connection:
                    continue
                # print("Connection has uart service")
                uart = connection[UARTService]
                update_label("\0")
                # print("Connected to peripheral via uart.")
                break
        except Exception as e:
            if billboard:
                update_label("Unable to connect \nto {}.\nPlease rescan[A+B].".format(billboard.complete_name))
            else:
                update_label("Connection failed. Try rescan[A+B].")
            print(e)


#NOTE: Consider using Packets for transporting billboard data
button_delay = 0.3
last_time = time.monotonic()
while True:
    if ble.connected:
        if (time.monotonic() - last_time) > button_delay:
            if uart:
                if clue.button_b:
                    clue.start_tone(587)
                    uart.write(b'n')
                    byte_count = uart.in_waiting
                    if byte_count > 0:
                        data = uart.read(byte_count)
                        if data:
                            parse_data()
                            update_label(data.decode('utf-8'))
                            # print(data, flush=True)

                if clue.button_a:
                    clue.start_tone(523)
                    uart.write(b'p')
                    byte_count = uart.in_waiting
                    if byte_count > 0:
                        data = uart.read(byte_count)
                        if data:
                            parse_data()
                            update_label(data.decode('utf-8'))
                            # print(data, flush=True)

            if clue.button_a and clue.button_b:
                clue.start_tone(459)
                clear_connection()

            last_time = time.monotonic()
        


    else: #BLE not connected
        if clue.button_a and clue.button_b:
            if not billboard:
                billboard = scan()
            else:
                connect(billboard=billboard)
    
    clue.stop_tone()


