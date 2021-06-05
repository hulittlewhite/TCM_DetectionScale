#! /usr/bin/python2

import time
import sys
import requests
import simplejson
import RPi.GPIO as GPIO
# from scale import Scale
from picamera import PiCamera
from time import sleep


import socket
import threading


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


def fun(weight):
    changedweight = weight
    lastweight = 0.0
    refresh = 0
    # r = requests.post(url + '/clear')
    numcount = [1]
    time_str = 'image_' + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + 'AA_'
    # while r != True:
    num = numcount[0]
    try:
        print(changedweight)
        if abs(changedweight) < 0.01:
            changedweight = 0.0

        else:
            changed = 1
        print(changed)
        if changed:

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

        # time.sleep(0.001)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


"""创建TCP服务端一般需要五个步骤
1、创建Socket，绑定Socket到本地的IP与端口
2、开始监听连接
3、进入循环，不断接收客户端的连接请求
4、接收传来的数据，并发送给对方数据
5、传输完毕后，关闭Socket
"""

if __name__ == '__main__':
    requests.post(url + '/clear')
    # 第一步：创建一个基于IPV4和TCP协议的Socket
    # Socket绑定IP（127.0.0.1为本机）与端口
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('127.0.0.1', 888))
    s.bind(('', 8888))
    # 第二步：监听连接
    s.listen(5)
    print('Waiting for connection...')
    # 第三步：接收一个新的连接：
    sock, addr = s.accept()
    while True:
        data = sock.recv(1024)
        weight = data.decode('utf-8')
        try:
            weight = float(weight)
            print('收到--->>> %s!' % weight)

            fun(weight)
            # if weight > 20:
        except Exception as e:
            print(e)




