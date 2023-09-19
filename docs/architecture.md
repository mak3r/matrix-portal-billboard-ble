# Matrix Portal Billboard and Controller

Rationionale for implementation on the M5StickC Plus:
* I have a few of them laying around
* They have several buttons and a display for human interaction
* They have WiFi (a means to communicate with the billboard)

## Basic architecture

* `[billboard] <==== ble (uart) ====> [controller]`
* This is a closed loop system where the controller and billboard become tightly coupled

    * The billboard creates a BLE Announcement
    * The controller identifies the the billboard BLE device and connects
    * The controller's function is to send send simple message to the billboard to change the display content
    * The billboard will respond with a json object indicating what is currently on display
    * The billboard displays the screen until duration has elapsed or a screen change command is sent
    * If the `screen` duration expires the 'default' `screen` is displayed on the billboard

* `screens` 

    * are the set of options to display on the billboard
    * may include metadata about scrolling or duration
    * encoded in json format - see the main [README.MD](../README.md)

## Implementation

* Controller:

    * has a known set of 'screens' written to its memory
    * has ble access
    * connects to billboard ble
    * may display a representation of the current screen
        * may display it's connection status
    * has a way for human interaction to be converted into screen change commands

* Billboard

    * Has BLE 
    * Responds to single character commands 'p'revious and 'n'ext
    * Replies with the `screen` currently displayed

## Usage

*  Can vary by controller