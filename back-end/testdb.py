#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/4 15:33
# @Author  : Tianle Hu
# @Site    :
# @File    : testdb.py
# @Software: PyCharm
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/4 15:09
# @Author  : Tianle Hu
# @Site    :
# @File    : db.py.py
# @Software: PyCharm
import pymysql
class C_sql():
    def connect(self):
        self.db = pymysql.connect(host='127.0.0.1', port=3306, database='tcm', user='root',
                       password='123456', charset='utf8')
    def insert_to(self,weight):
        sql = """INSERT INTO tcm_dis (classType, conf, weight, unit_g) VALUES ('as',0.982, {},8.0)""".format(weight)
        self.db.ping(reconnect=True)
        cursor = self.db.cursor()
        cursor.execute(sql)
        cursor.connection.commit()
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        self.db.close()
