#! /usr/bin/python2

import time
import sys
import requests
import simplejson
import RPi.GPIO as GPIO
#from scale import Scale
from picamera import PiCamera
from time import sleep
import time


# url = "http://192.168.0.100:5000"
# url = "http://192.168.43.178:5000"
url = "http://47.100.28.132:5000"
geturl = url + "/upload"
EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711

changedweight = 0.0
lastweight = 0.0
lastlastweight = []
weightlist = [0.0] * 3
camera = PiCamera()


def countaverage(weilist):
    sum = 0
    for i in range(len(weilist)):
        sum += weilist[i]
    return sum/len(weilist)


def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()


hx = HX711(5, 6)


# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
# hx.set_reference_unit(113)
hx.set_reference_unit(1)

hx.reset()
hx.tare()

while True:
    refresh = 0
    r = requests.post(url + '/clear')
    numcount = [1]
    time_str = 'image_' + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + 'AA_'
    while r != True:
        num = numcount[0]
        try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.

        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string

        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
            val = -float(hx.get_weight(1))/126000
            val = round(val, 3)
            print("val:", val)

            changed = 0
            totalweight = val
            if abs(totalweight) < 0.005:
                totalweight = 0.0

            weightlist.append(totalweight)
            weightlist.pop(0)
            # print("weightlist", weightlist)
            averageweight = countaverage(weightlist)
            if abs(totalweight - lastweight) > 0.05:
                if abs(totalweight - averageweight) < 0.002:
                    lastlastweight.append(round(lastweight,3))
                    changedweight = totalweight - lastweight
                    lastweight = totalweight
                    changed = 1
            # print("changed:", changed)

            if abs(changedweight) < 0.005:
                changedweight = 0.0
            if changed:
                print("{0: 4.3f}g, {1:4.3f}g, {2}g".format(totalweight, \
                 changedweight, lastlastweight))
                weight = {"weight": changedweight}

                image_name = time_str + str(num).zfill(3) + '.jpg'
                camera.capture('/home/pi/Desktop/' + image_name)

                filepath = '/home/pi/Desktop/' + image_name
                numcount[0] += 1
                split_path = filepath.split('/')
                filename = split_path[-1]
                file = open(filepath, 'rb')
                files = {'file': (filename, file, 'image/jpg')}

                r = requests.post(geturl, data=weight, files=files)
                result = r.text
                print(result)

                if abs(val) < 0.01:
                    for i in range(2):
                        r = requests.post(url + '/clear')
                        print("clear successfully")
                    break
           # for i in range(1):
            if abs(val) < 0.01 and refresh == 0:
                r = requests.post(url + '/clear')
                print("clear successfully")
                refresh += 1
                print(refresh)

        # time.sleep(0.001)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
