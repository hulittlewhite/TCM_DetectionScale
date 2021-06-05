import requests
import os
import time
import datetime


def upload_image():
    url = "http://127.0.0.1:5000"

    filepath = 'F:/yandiansai_tcm/original_tcm/aiye/aiye_0001.jpg'
    split_path = filepath.split('/')
    filename = split_path[-1]
    print(filename)
    weight = {"weight": 1.5}
    info = {"info": "background"}
    info = {"info": "chinese medicine"}
    file = open(filepath, 'rb')
    files = {'file': (filename, file, 'image/jpg')}

    r = requests.post(url, data=weight, files=files)
    result = r.text
    print(result)


def upload_image_with_args(filepath, w):
    url = "http://127.0.0.1:5000/upload"

    # filepath = 'F:/yandiansai_tcm/original_tcm/aiye/aiye_0001.jpg'
    split_path = filepath.split('/')
    filename = split_path[-1]
    print(filename)
    weight = {"weight": w}
    info = {"info": "background"}
    info = {"info": "chinese medicine"}
    file = open(filepath, 'rb')
    files = {'file': (filename, file, 'image/jpg')}

    r = requests.post(url, data=weight, files=files)
    result = r.text
    print(result)


def upload_background():
    url = "http://127.0.0.1:5000/getbackground"
    filepath = ''
    # filename = 'background_image.jpg'
    # filename = os.path.split(filepath)
    split_path = filepath.split('/')
    filename = split_path[-1]
    file = open(filepath, 'rb')
    files = {'file': (filename, file, 'image/jpg')}
    r = requests.post(url, files=files)
    result = r.text
    print(result)


def clear_shoplist():
    url = 'http://127.0.0.1:5000/clear'
    r = requests.post(url)
    print(r.text)


def test():
    path = ''
    weight = [0.216, 1.5, -1.5, -1.5]
    for i in range(1):
        time_1 = datetime.datetime.now()
        upload_image_with_args(path + '%s' % str(i + 1).zfill(3) + '.jpg', weight[i])
        time_2 = datetime.datetime.now()
        print(time_2 - time_1)
        time.sleep(5)


def test2():
    path = ''
    weight = [1.5, 1.5, 1.5, -1.5]
    for i in range(4):
        time_1 = datetime.datetime.now()
        upload_image_with_args(path + '%s' % str(i + 1).zfill(3) + '.jpg', weight[i])
        time_2 = datetime.datetime.now()
        print(time_2 - time_1)
        time.sleep(5)


def test3():
    path = ''
    weight = [0.216, 0.166, 0.316]
    for i in range(3):
        upload_image_with_args(path + '%s' % str(i + 1).zfill(3) + '.jpg', weight[i])
        time.sleep(4)


def test4():
    path = ''
    weight = [0.216, -0.216, 0.216, 0.256, 0.289, 0.32, -0.32, -0.289, -0.256, -0.216]
    for i in range(10):
        upload_image_with_args(path + '%s' % str(i + 1).zfill(3) + '.jpg', weight[i])
        time.sleep(4)
# upload_background()
# upload_image()


def test5():
    path = ''
    weight = [1.5, -1.5, 1.5, -1.5, 1.5, -1.5, 1.5, 1.5, 1.5]
    for i in range(4):
        upload_image_with_args(path + '%s' % str(i + 1).zfill(3) + '.jpg', weight[i])
        time.sleep(4)


clear_shoplist()
test5()
# clear_shoplist()
