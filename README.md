# A Billboard for Matrix Portal 
This is a simple application which will display a choice of text or images on the Adafruit Matrix Portal 32x64 display. It sets up the Matrix Portal as an Access Point (AP) such that it can receive billboard content from a connected Station (Client)

## Code

* lib - libraries and resources needed to run the bilboard app
    - These can and should be updated to the latest versions 
    - Libraries included here are used to simplify the time to get up and running 
    - [Get the latest libraries](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries)
* `code.py` - the application code which parses and displays the content
* `secrets.py` - contains secrets which will be loaded at boot time
* `content.json` - this (optional) file can contain a set of possible content to be displayed on the billboard. 

## Quick Start
1. [Prepare the MatrixPortal](https://learn.adafruit.com/matrix-portal-new-guide-scroller/prep-the-matrixportal)
1. [Install CircuitPython](https://learn.adafruit.com/matrix-portal-new-guide-scroller/install-circuitpython)
1. Copy all files from this repo into the `CIRCUITPY` directory that was mounted when you installed CircuitPython
1. Power up
1. Connect to the AP with a client (using SSID and Passphrase set in secrets)
1. Send content from the client


## Displaying content

Content can be displayed from the content.json file (hosted) on the Matrix Portal or dynamically (posted). The up/down buttons on the Matrix Portal can be used to switch to and display the next set of content on the device. 

### Hosted Example

* Display the next billboard hosted on the device:
* `curl -X GET http://192.168.4.1/next`

### Posted Example

* Display the message "Hello Billboard" in yellow text against a purple background:
* `curl -X POST http://192.168.4.1 -H 'Content-Type: application/json' -d '{"default": {"text": "Hello\nBillboard", "fg": "0xFFD700", "bg": "0x6C0BA9}}'`



## Content Layout
The `content.json` file contains a list of content which can be cycled through on the Matrix Portal. Content could be text or bitmap images. Or a combination of both. Text can be scrolled orizontally and colors can be set for the foreground and background. The content file must be json formatted.

**NOTE:** Each entry in the `content.json` file must have a unique key. The values of the entry are specfied as one fo the 4 content types. This allows for each content type to be repeated in the file in any order. Python reads dictionaries in without regard to order so sequencing according the the file layout is not possible without further development

### There are 3 content types:

1. `text` can be a simple word or phrase which is shown statically on the display. `text` has 2 attributes `fg` and `bg`. This type can be read from the `content.json` file or from a `url` content type

1. `stext` or scrolling text can be a simple word or phrase which will be scrolled from right to left across the display. `stext` has 3 attributes `fg`, `bg` and `rate`. This type can be read from the `content.json` file or from a `url` content type.

1. `img` is the path to a bitmap image on disk. It is recommended that `img` bitmaps are formatted to the exact size of the display (default 64x32 - WxH). This type can be read from the `content.json` file or from a `url` content type.


### Attributes:
1. `fg` is the foreground color of the text specified as a hex string in RGB - for example 0xFFFFFF is white.
1. `bg` can be either a hex string specified in RGB or a path to a file on disk. 
1. `rate` is the speed at which scrolling text moves from right to left across the screen. Reasonable values appear to be between .04 (fast) and .2 (slow). Any floating point value may be used however the code does not check for 'reasonable' values. 

### Example `content.json`
```
{
	"geeko": {"img": "images/geeko.bmp"},
	"text1": {
		"text" : "howdy",
		"bg": "0x800020",
		"fg": "0x777777"
	},
	"rancher": {"img": "images/rancher.bmp"},
	"scroll-text": {
		"stext" : "scroll this by me",
		"bg": "0x800020",
		"fg": "0xAAAAAA",
		"rate" : ".2"	
	},
	"wrap-example": {
		"text" : "wrap text\nexample",
		"fg" : "0x982200",
		"bg" : "0x000000"
	},
	"file-bg-example": {
		"text" : "GEEKO",
		"fg" : "0xFFFFFF",
		"bg" : "images/geeko.bmp"
	},
	"in-meeting": {
		"text": "IN A\nMEETING",
		"fg" : "0xFF11BB",
		"bg" : "0x000000"
	}

}

```