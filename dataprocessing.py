import pymysql

# 定义仓库
repository = dict()
# 定义采购药材清单对象
shop_list = []
name_id = dict()
current_list = []


# 定义一个函数来初始化药材
def init_repository():
    db = pymysql.connect("localhost", "root", "1234", "tcmshop")
    # db = pymysql.connect("localhost", "root", "123456", "tcmshop")
    cursor = db.cursor()
    sql = "select * from tcm_table"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            name = row[1]
            information = row[2]
            priceperkilo = row[3]
            picurl = row[4]
            # 打印结果
            # print("id=%s,name=%s,information=%s,price=%s,picurl=%s" % (id, name, information, priceperkilo, picurl))
            repository[id] = (id, name, priceperkilo)
            name_id[name] = id
    except:
        print("Error: unable to fetch data")
    db.close()


def show_goods():
    print("欢迎来到智能中药房")
    print('中草药清单：')
    print("%13s%40s%10s" % ("编号", "名称", "单价"))
    # 遍历repository的所有value来显示商品清单
    for goods in repository.values():
        print("%15s%40s%12s" % goods)


# 显示采购药材清单，就是遍历代表药材清单的list列表


def make_list():
    sum = 0.0
    the_list = []
    print(shop_list)
    for i, item in enumerate(shop_list):
        id = i + 1
        code = item[0]
        name = repository[code][1]
        price = repository[code][2]
        price = round(price, 2)
        number = float(item[1])
        number = round(number, 2)
        amount = price * number
        amount = round(amount, 2)
        sum = sum + amount
        sum = round(sum, 2)
        line = "%-4s|%8s|%15s|%8s|%6s|%8s" % \
               (id, code, name, price, number, amount)
        the_list.append(line)
    the_list.append("sum: %8s" % sum)
    return the_list


def show_list():
    print("=" * 100)
    # 如果清单不为空的时候，输出清单的内容
    if not shop_list:
        print("还未购买中药材")
    else:
        title = "%-5s|%15s|%40s|%10s|%4s|%10s" % \
                ("ID", "编号", "名称", "单价", "重量", "小计")
        print(title)
        print("-" * 100)
        # 记录总计的价钱
        sum = 0.0
        # 遍历代表药材清单的list列表
        for i, item in enumerate(shop_list):
            # 转换id为索引加1
            id = i + 1
            # 获取该购物项的第1个元素：编号
            code = item[0]
            # 获取编号读取中药信息，再获取中药的名称
            name = repository[code][1]
            # 获取编号读取中药信息，再获取中药的单价
            price = repository[code][2]
            # 获取该购物项的第2个元素：药材重量
            number = float(item[1])
            # 小计
            amount = price * number
            # 计算总计
            sum = sum + amount
            line = "%-5s|%17s|%40s|%12s|%6s|%12s" % \
                   (id, code, name, price, number, amount)
            print(line)
        print("-" * 100)
        print("                          总计: ", sum)
    print("=" * 100)


def make_web_list():
    the_list = []
    sum = 0.0
    for i, item in enumerate(shop_list):
        id = i + 1
        code = item[0]
        name = repository[code][1]
        price = repository[code][2]
        price = round(price, 2)
        number = float(item[1])
        number = round(number, 3)
        amount = price * number
        amount = round(amount, 2)
        sum = sum + amount
        sum = round(sum, 2)
        # the_list[i].extend([name, price, amount])
        the_list.append([name, price, number, amount])
    if len(current_list) > 0 and current_list[0][0] == '1000':
        the_list.append(['1000', 0, 0, 0])
    return the_list, sum


def make_web_new():
    the_list = []
    if len(current_list) == 0:
        print('no new chinese medicine')
        return []
    else:
        if current_list[0][0] == '1000':
            the_list.append(['1000', 0, current_list[0][1], 0])
            return the_list
        for i in range(len(current_list)):
            code = current_list[i][0]
            name = repository[code][1]
            price = repository[code][2]
            price = round(price, 2)
            weight = float(current_list[0][1])
            weight = round(weight, 3)
            amount = round(price * weight, 2)
            the_list.append([name, price, weight, amount])
        return the_list


# 添加购买中药，就是向代表用户采购药材清单的list列表中添加一项。
def add():
    code = input("请输入中药编号:\n")
    # 没有找到对应的中药，条码错误
    if code not in repository:
        print("编号错误，请重新输入")
        return
    # 根据条码找中药
    goods = repository[code]
    # 等待输入数量
    number = input("请输入重量:\n")
    # 把中药和购买数量封装成list后加入购物清单
    shop_list.append([code, number])


def add_medicine(id, weight):
    # goods = repository[id]
    # weight = weight
    changed = 0
    for i in range(len(shop_list)):
        if shop_list[i][0] == id:
            edit_weight(id, i, weight)
            changed = 1
    if changed == 0:
        shop_list.append([id, weight])
    #     if len(current_list) != 0:
    #         current_list.pop(0)
    #     current_list.append([id, weight])
    # # print(shop_list)


def add_empty(weight):
    if len(current_list) != 0:
        current_list.pop(0)
    current_list.append(['1000', weight])


def remove_empty(weight):
    if len(current_list) != 0:
        current_list.pop(0)
    current_list.append(['1000', weight])


def edit_weight(id, i, weight):
    oldweight = float(shop_list[i][1])
    shop_list[i][1] = oldweight + float(weight)
    if shop_list[i][1] < 0.02:
        del shop_list[i]
    # if len(current_list) != 0:
    #     current_list.pop(0)
    # current_list.append([id, weight])


def remove_medicine(id, weight):
    changed = 0
    # print('shoplist:', shop_list)
    for i in range(len(shop_list)):
        if shop_list[i][0] == id:
            changed = 1
            shop_list[i][1] = float(shop_list[i][1]) + float(weight)
            # if len(current_list) != 0:
            #     current_list.pop(0)
            # current_list.append([id, weight])
            if shop_list[i][1] < 0.02:
                del shop_list[i]
                break

    if changed == 0:
        print("remove error")


def edit_kind(id, true_kind_id):
    if len(current_list) > 0:
        weight = current_list[0][1]
    else:
        weight = 0
    if id == '1000':
        if weight > 0:
            add_medicine(true_kind_id, weight)
        else:
            remove_medicine(true_kind_id, weight)
    else:
        remove_medicine(id, -weight)
        add_medicine(true_kind_id, weight)
    if len(current_list) != 0:
        for i in range(len(current_list)):
            if id == current_list[i][0]:
                current_list[i] = [true_kind_id, weight]
                break
        new_list = list(set([i[0] for i in current_list]))
        copy_current_list = [i for i in current_list]
        while len(current_list) > 0:
            del current_list[0]
        print('copy_current_list:', copy_current_list)
        for i in range(len(new_list)):
            current_list.append([new_list[i], sum([j[1] for j in copy_current_list if j[0] == new_list[i]])])
            print('current_list.append:', current_list[i])

    # if len(current_list) != 0:
    #     current_list.pop(0)
    # current_list.append([true_kind_id, weight])


def clear_shoplist():
    while len(shop_list) != 0:
        del shop_list[0]
    while len(current_list) != 0:
        current_list.pop()


# 修改购买中药的数量，就是修改代表用户采购药材清单的list列表的元素
def edit():
    id = input("请输入要修改的采购药材明细项的ID:\n")
    # id减1得到购物明细项的索引
    index = int(id) - 1
    # 根据索引获取某个购物明细项
    item = shop_list[index]
    # 提示输入新的购买数量
    number = input("请输入新的重量:\n")
    # 修改item里面的number
    item[1] = number


def store_order(orderlist):
    id = orderlist[0]
    data = orderlist[1]
    status = orderlist[2]
    price = orderlist[3]
    weight = orderlist[4]
    info = orderlist[5]
    db = pymysql.connect("localhost", "root", "1234", "tcmshop")
    cursor = db.cursor()
    sql = "insert into order_info(orderid, orderdate, status, price, weights, info) values (%s, %s, %s, %s, %s, %s)"
    try:
        # 执行SQL语句
        cursor.execute(sql, (id, data, status, price, weight, info))
        # 获取所有记录列表
        # results = cursor.fetchall()
        db.commit()  # 提交数据
        cursor.close()
    except:
        print("Error: unable to store data")
    db.close()


# 删除购买的中药明细项，就是删除代表用户采购药材清单的list列表的一个元素。
def delete():
    id = input("请输入要删除采购药材明细项的ID: ")
    index = int(id) - 1
    # 直接根据索引从清单里面删除掉采购药材明细项
    del shop_list[index]


def getshoplist():
    the_list = []
    for i, item in enumerate(shop_list):
        id = item[0]
        # name = repository[code][1]
        # weight = float(item[1])
        the_list.append(id)
    return the_list


def add_list(the_list, weight):
    per_weight = round(float(weight) / len(the_list), 3)
    while len(current_list) != 0:
        current_list.pop(0)
    for i in range(len(the_list)):
        add_medicine(the_list[i], per_weight)
        current_list.append([the_list[i], per_weight])


def remove_list(the_list, weight):
    per_weight = round(float(weight) / len(the_list), 3)
    while len(current_list) != 0:
        current_list.pop(0)
    for i in range(len(the_list)):
        remove_medicine(the_list[i], per_weight)
        current_list.append([the_list[i], per_weight])


# cmd_dict = {'a': add, 'e': edit, 'd': delete, 'p': payment, 's': show_goods}

# 显示清单和操作命令提示
if __name__ == '__main__':
    # init_repository()
    # show_goods()
    # while True:
    #     show_list()
    #     # show_command()
    # order_info(orderid, orderdate, status, price, weights, info)
    list = ['10001', '20210601', 'success', '58.88', '12.3', 'aiye:7.5']
    # store_order(list)
