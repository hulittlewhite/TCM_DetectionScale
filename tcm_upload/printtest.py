from escpos import *
import requests
import json
import os
import datetime
import time
from PIL import Image, ImageFont, ImageDraw

usb = printer.Usb(0x0fe6, 0x811e, 0, out_ep=0x02)
fruits_dict = {"apple": "苹果", "banana": "香蕉", "orange": "橙子", "kiwifruit": "奇异果", "pineapple": "菠萝", "pitaya": "火龙果", "hamimelon": "哈密瓜", "watermelon": "西瓜"}
def get_print():
    path = 'http://47.103.155.60:5000/print_order'
    r = requests.post(path)
    return r.text

while True:
    data = get_print()
    # data = '{"fruits":[{"name":"apple","netweight":0.297,"subtotal":5.93,"unitprice":19.96},{"name":"orange","netweight":0.154,"subtotal":1.53,"unitprice":9.96},{"name":"banana","netweight":0.731,"subtotal":8.74,"unitprice":11.96}],"total":16.2}'
    # print('data:', data)
    text = json.loads(data)
    # print('text:', text)
    if text is None:
        print('data is None')
        pass
    else:
        print('data is not none')
        # print(text)
        print(type(text))
        fruits = text['fruits']
        totalprice = '¥' + str(text['total'])
        totalprice = totalprice.rjust(8)
        print('fruits:', fruits)
        print('totalprice:', totalprice)

        info = []
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info.append(nowTime + "   自助结算A01")
        # info.append("订单编号：")
        info.append("==================================")
        info .append("名称     单价       重量     小计 ")
        info.append("==================================")

        for i in fruits:
            fruit_name = fruits_dict[i['name']].ljust(3)
            fruit_price = '¥' + str(i['unitprice']) + '/kg '
            fruit_price = fruit_price.center(12)
            fruit_weight = str(i['netweight']) + 'kg'
            fruit_weight = fruit_weight.center(9)
            price = '¥' + str(i['subtotal'])
            price = price.center(8)
            info.append(fruit_name + fruit_price + fruit_weight + price)
        print(info)
        info.append("==================================")
        info.append(("总价：" + totalprice).rjust(30))
        im = Image.new('RGB', (380, 30 + 20 * len(info)), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype('simsun.ttc', 20)
        for i in range(len(info)):
            text = info[i]
            dr.text((10, 20*i), text, font=font, fill="#000000")
        
       
        ntime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        pic_path = ntime + '.bmp'
        im.save(pic_path)
        #time.sleep(2)
        usb.image(pic_path)
        #
        # #usb.qr(‘值’)#打印二维码
        # #usb.set(codepage=None, align='center')#设置页面居中
        usb.cut()#切纸
usb.close()#关闭连接