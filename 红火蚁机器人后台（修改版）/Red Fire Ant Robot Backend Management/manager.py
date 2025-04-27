import config,datetime
from application import Application
from application import Application2
from multiprocessing import Process
import time, pymysql,requests


def Command():
    print("我是第二个进程")
    order_time = ""
    datas = {}
    # 获取当前时间
    while True:
        time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        now_time = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
        print(now_time)
        # 从数据库中查询是否有该时间的命令
        con = config.mysql
        db = pymysql.connect(**con)
        cursor = db.cursor()
        sql = "select * from wait_command where status=1"
        cursor.execute(sql)
        data = cursor.fetchone()
        db.close()
        time.sleep(0.5)
        if data:
            print(data)
            order_time = data[10]
            print(order_time)
            # 将数据拼接成json格式
            command_data = {
                'obj_id': data[1],
                'radius': data[3],
                'height': data[4],
                'speed': data[5],
                'times': data[6],
                'type': config.type_select[data[7]]['name'],
                'angle': data[8],
                'status': data[9],
                'start_time': data[10]
            }
            print(command_data)
            # 如果时间相同，下发指令
            if now_time == order_time:
                print("===========================")

                # 获取token
                url = 'https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens'
                data = {
                    "auth": {
                        "identity": {
                            "methods": ["password"],
                            "password": {
                                "user": {
                                    "name": "NikkoLKR",
                                    "password": "lkr3931978",

                                    "domain": {
                                        "name": "NikkoLKR"
                                    }
                                }
                            }
                        },
                        "scope": {
                            "project": {
                                "name": "cn-north-4"
                            }
                        }
                    }
                }
                headers = {'Content-Type': 'application/json;charset=UTF-8'}
                req = requests.post(url, json=data)
                token = req.headers['X-Subject-Token']

                # 下发命令
                command_url = "https://iotda.cn-north-4.myhuaweicloud.com/v5/iot/0edf44222a80f31d2f60c015ff218024/devices/62ecc0ce3a88483559871f7e_box_01/commands"
                order_data = {
                    "service_id": "plants_box",
                    "command_name": "GET_DATA",
                    "paras": {"GET_DATA": "True"}
                }
                order_headers = {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'X-Auth-Token': token
                }
                result = requests.post(command_url, json=order_data, headers=order_headers)
                print(result)
                return



if __name__ == '__main__':
    p = Process(target=Command)
    p.start()


