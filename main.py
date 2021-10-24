import json
import os.path
import sys
import time
from datetime import datetime
from threading import Thread
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735
from PIL import ImageFont
from urllib.request import urlopen

import RPi.GPIO as GPIO
import dht11

# Initialize GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Initialize / Configure Display
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
device = st7735(serial)

# Load Font
fonturl = "https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf"
font24 = ImageFont.truetype(urlopen(fonturl), size=24)
font16 = ImageFont.truetype(urlopen(fonturl), size=16)

# Set sensor Object
sensor = dht11.DHT11(pin=4)

# Initialize variables
temperatur = ""
humidity = ""
path = os.path.dirname(os.path.abspath(sys.argv[0]))

def main():
    try:
        # Create Thread for Clock
        ct = Thread(target=showcurrenttime)
        ct.start()

        # Run Temperature Measurement on Main Thread
        measuretemperatur()

    finally:
        GPIO.cleanup()
        device.cleanup()


def getvalues():
    global temperatur, humidity
    # fetch new data
    result = sensor.read()
    if result.is_valid():
        temperatur = result.temperature
        humidity = result.humidity
        exportvalues()


def exportvalues():
    # Currentdate as file name
    currentdate = datetime.now().strftime("%Y-%m-%d")
    # Try load already fetched data from json file
    try:
        data = json.load(open("{0}/web/data/{1}.json".format(path, currentdate)))
    except OSError:
        # Create new
        data = [

        ]
    # Currenttime as time stamp in data
    currenttime = datetime.now().timestamp() * 1000
    # Add data
    data.append({"time": currenttime, "temperatur": temperatur, "humidity": humidity})
    # Dump to file
    json.dump(data, open("{0}/web/data/{1}.json".format(path, currentdate), "w"), indent=4)


def showcurrenttime():
    while True:
        # Get current time
        timestring = datetime.now().strftime("%H:%M:%S")
        datestring = datetime.now().strftime("%d.%m.%Y")
        with canvas(device) as draw:
            draw.text((5, 5), timestring, font=font24, fill="white")
            draw.text((5,32), datestring, font=font16, fill="white")

def measuretemperatur():
    while True:
        getvalues()
        time.sleep(30)


if __name__ == "__main__":
    main()
