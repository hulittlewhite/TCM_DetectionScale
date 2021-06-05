import threading
import paho.mqtt.client as mqtt
import time
from testdb import C_sql

HOST = "192.168.1.107" #emq服务器地址
PORT = 1883

class Mqtt_subscribe(threading.Thread):
    """
    mqtt thread, 完成订阅功能
    """

    def __init__(self, subtopic):
        super(Mqtt_subscribe, self).__init__()
        self.client_id = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(
                time.time()))
        self.client = mqtt.Client(self.client_id)
        self.client.user_data_set(subtopic)
        self.client.username_pw_set("admin", "public")
        self.message = None

    def run(self):
        # ClientId不能重复，所以使用当前时间
        # 必须设置，否则会返回「Connected with result code 4」
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(HOST, PORT, 60)
        self.client.loop_forever(timeout=60)

    def on_connect(self, client, subtopic, flags, rc):
        print("Connected with result code " + str(rc))
        print("topic:" + subtopic)
        client.subscribe(subtopic, 2)
        client.subscribe('weight',0)
        self.sql_lite = C_sql()
        self.sql_lite.connect()

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + msg.payload.decode("utf-8"))
        if msg.topic == 'weight':
            self.sql_lite.insert_to(msg.payload.decode('utf-8'))
            client.publish("weight_recv","gun",2)





