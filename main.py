import json
import os.path
import sys
import time
from datetime import datetime
from threading import Thread

import RPi.GPIO as GPIO
import dht11

# Initialize GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Set sensor Object
sensor = dht11.DHT11(pin=4)

# Initialize variables
temperatur = ""
humidity = ""
path = os.path.dirname(os.path.abspath(sys.argv[0]))

# Data for 7 segment display
# Pins of Segments
segments =  [6, 11, 16, 20, 21, 5, 19, 26]
# Pins of Digits
digits = [12, 7, 8, 13]
# Data to display numbers
num = {' ':[1,1,1,1,1,1,1],
    '0':[0,0,0,0,0,0,1],
    '1':[1,0,0,1,1,1,1],
    '2':[0,0,1,0,0,1,0],
    '3':[0,0,0,0,1,1,0],
    '4':[1,0,0,1,1,0,0],
    '5':[0,1,0,0,1,0,0],
    '6':[0,1,0,0,0,0,0],
    '7':[0,0,0,1,1,1,1],
    '8':[0,0,0,0,0,0,0],
    '9':[0,0,0,0,1,0,0]}
# Init digits
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 0)
# Init segments
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 1)

def main():
    try:
        # Create Thread for Clock
        th = Thread(target=currenttime)
        th.start()
        while True:
            getvalues()
            time.sleep(30)
    finally:
        GPIO.cleanup()


def getvalues():
    global temperatur, humidity
    # fetch new data
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

def currenttime():
    while True:
        # Get current time
        dtstring = datetime.now().strftime("%H%M")
        # Loop through dtstring to get specific Digits
        for index in range(0, len(dtstring)):
            # Select digit
            GPIO.output(digits[index], 1)
            # Show number on Digit
            for integ in range(0, 7):
                # Selects the Segmen 0-7, defines if it is on or off
                GPIO.output(segments[integ], num[dtstring[index]][integ])
            time.sleep(0.002)
            # Close Digit
            GPIO.output(digits[index], 0)

if __name__ == "__main__":
    main()
