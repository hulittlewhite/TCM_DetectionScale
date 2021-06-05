import sys
import requests
import simplejson
import RPi.GPIO as GPIO
from scale import Scale
from picamera import PiCamera
from time import sleep
import time

# url = "http://192.168.0.101:5000"
url = "http://192.168.43.16:8888"
# geturl = "http://192.168.0.101:5000/upload
geturl = "http://192.168.43.16:8888/upload"

# filepath = '/home/pi/Pictures/example/banana.jpg'
# split_path = filepath.split('/')
# filename = split_path[-1]

scale = Scale()

scale.setReferenceUnit(21)
scale.reset()
scale.tare()

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


# numcount = [0]
while True:
    r = requests.post(url)
    numcount = [1]
    time_str = 'image_' + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + 'AA_'
    while r != True:
        num = numcount[0]
        try:
            totalweight = -scale.getMeasure()/6000
            changed = 0
            if abs(totalweight) < 0.002:
                totalweight = 0.0
            weightlist.append(totalweight)
            weightlist.pop(0)
            averageweight = countaverage(weightlist)
            if abs(totalweight - lastweight) > 0.05:
                if abs(totalweight - averageweight) < 0.002:
                    lastlastweight.append(round(lastweight, 3))
                    changedweight = totalweight - lastweight
                    lastweight = totalweight
                    changed = 1

            # changedweight = totalweight - lastweight
            # changedweight = -changedweight
            # totalweight = -totalweight
            # lastlastweight = -lastlastweight

            # lastweight = totalweight
            if abs(changedweight) < 0.002:
                changedweight = 0.0
            if changed:
                print("{0: 4.3f}kg, {1:4.3f}kg, {2}kg".format(totalweight, \
             changedweight, lastlastweight))
                weight = {"weight": changedweight}


                # camera.resolution = (416, 416)
                # camera.start_preview()
                # sleep(2)
                image_name = time_str + str(num).zfill(3) + '.jpg'
                camera.capture('/home/pi/Desktop/' + image_name)
                # camera.stop_preview()
                filepath = '/home/pi/Desktop/' + image_name
                numcount[0] += 1
                split_path = filepath.split('/')
                filename = split_path[-1]
                file = open(filepath, 'rb')
                files = {'file': (filename, file, 'image/jpg')}

                r = requests.post(geturl, data=weight, files=files)
                result = r.text
                print(result)
                # res = requests.get(geturl)
                # print(simplejson.loads(res.text))
                # res_list = simplejson.loads(res.text)
                # for i in res_list:
                    # print(i)

        except (KeyboardInterrupt, SystemExit):
            GPIO.cleanup()
            sys.exit()

