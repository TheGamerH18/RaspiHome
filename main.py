import json
import os.path
import sys
import time
from datetime import datetime

import RPi.GPIO as GPIO
import dht11

# Initialize GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Set sensor Object
sensor = dht11.DHT11(pin=4)

temperatur = ""
humidity = ""
path = os.path.dirname(os.path.abspath(sys.argv[0]))


def main():
    while True:
        getvalues()
        time.sleep(5)


def getvalues():
    global temperatur, humidity
    result = sensor.read()
    if result.is_valid():
        temperatur = result.temperature
        humidity = result.humidity
        print("Temperatur: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
        exportvalues()
    else:
        print("Error: %d" % result.error_code)


def exportvalues():
    currentdate = datetime.now().strftime("%Y-%m-%d")
    try:
        data = json.load(open("{0}/web/data{1}.json".format(path, currentdate)))
    except OSError:
        data = [

        ]
    currenttime = datetime.now().timestamp() * 1000
    data.append({"time": currenttime, "temperatur": temperatur, "humidity": humidity})
    json.dump(data, open("{0}/web/data{1}.json".format(path, currentdate), "w"), indent=4)


if __name__ == "__main__":
    main()
