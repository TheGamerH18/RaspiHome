import json
import os.path
import sys
import time
from datetime import datetime
from threading import Thread
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735

import RPi.GPIO as GPIO
import dht11

# Initialize GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
device = st7735(serial)

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
        dtstring = datetime.now().strftime("%S:%H:%M %D.%m.%Y")
        with canvas(device) as draw:
            draw.text((5, 5), dtstring, fill="white")


def measuretemperatur():
    while True:
        getvalues()
        time.sleep(30)


if __name__ == "__main__":
    main()
