 
# -*- coding: utf-8 -*-
from decimal import Decimal
from tornado.web import RequestHandler
from Helper import iPagination
import config
import json
from datetime import datetime
import base64
import io
# from PIL import Image

import tornado.web
from tornado.web import RequestHandler
from UserService import UserService
import config
# 引入统一拦截器
from interceptor import Interceptor

import requests, time
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
class MapHandlers(RequestHandler):
    def initialize(self):
        # 这是一个变量，来记录是否重定向
        self.redir = False

        # 修改全局变量
        config.options['url'] = self.request.path
        # 查询缓存
        flag = self.application.inter.mymain(self.request.path, self)
        print("index_flag:",flag)
        if not flag:
            # self.redirect(config.domain_url['url'])
            self.redir = True
        else:
            self.redir = False


        # 向华为云获取token值并储存在全局变量中

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
        # 将token值存储到全局变量中
        config.options['token'] = token

        return


    def get(self, h):
        if h == 'data_app': #接口，用来给前端js提供数据  有用
            # 如果h等于"index"
            resp_data3 = {}
            carlist = []
            run_list =[]
            run_list = self.application.db.get_all_obj("select * from cars_run_info order by carID", "cars_run_info")
            # list = self.application.db.get_all_obj("select * from cars order by carID" , "cars")

            # 用于存储每个 carID 最新数据的字典
            latest_data = {}

            for entry in run_list:
                carID = entry['carID']
                # 如果当前 carID 还没有记录，或者当前记录的 created_time 比已有记录的 created_time 更新
                if carID not in latest_data or entry['created_time'] > latest_data[carID]['created_time']:
                    latest_data[carID] = entry

            # 转换为列表格式
            carlist = list(latest_data.values())


            print("run_list如下：")
            print(run_list)
            resp_data3['list'] = carlist #resp_data['list'] 是小车基础信息数据
            resp_data3['run_list'] = run_list
            print("carlist如下：")
            print(carlist)
            
            resp_data3['current_user'] = config.options['current_user']
            print("resp_data3如下：")
            print(resp_data3)
            # 将 Decimal 类型转换为 float
            for lst in [resp_data3['list'], resp_data3['run_list']]:
                for item in lst:
                    if 'longitude' in item and isinstance(item['longitude'], Decimal):
                        item['longitude'] = float(item['longitude'])
                    if 'latitude' in item and isinstance(item['latitude'], Decimal):
                        item['latitude'] = float(item['latitude'])
            # 将datetime对象转换为字符串
            for lst in [resp_data3['list'], resp_data3['run_list']]:
                for item in lst:
                    if 'updated_time' in item and isinstance(item['updated_time'], datetime):
                        item['updated_time'] = item['updated_time'].isoformat()
                    if 'created_time' in item and isinstance(item['created_time'], datetime):
                        item['created_time'] = item['created_time'].isoformat()

            # 将数据转换为JSON字符串
            json_data = json.dumps(resp_data3)

            # 设置响应类型为JSON
            self.set_header("Content-Type", "application/json")

            # 输出JSON数据
            self.write(json_data)
            return

        if self.redir == True:
            # print({"left********"})
            self.redirect(config.domain_url['url'])

        else:
            # 获取cookies来进行页面展示
            cookies = self.get_cookie(name=config.cookies_name['name'])
            uid = cookies.split("#")[1]
            # 数据库查询
            sql = "select * from user where uid='%s'" % (uid)
            u_info = self.application.db.get_one(sql)
            info = {
                "nickname": u_info[1],
                'mobile': u_info[2]
            }

            resp_data = {}
            resp_data['current_user'] = config.options['current_user']
        # 处理HTTP GET请求
        resp_data = {}
        # 前端账户展示
        if h == "index":  #有用
            #test
            # sql = "select * from yichao"
            # yichao = self.application.db.get_all_obj(sql, "yichao")
            # print('yichao:',yichao)


            # 如果h等于"index"
            resp_data = {}

            page = self.get_query_argument("p", default="1")  
            # 获取查询参数p的值，默认为1
            mix_kw = self.get_query_argument('mix_kw', default='')  
            # 获取查询参数mix_kw的值，默认为空字符串
            status = self.get_query_argument('status', default='-1')  
            # 获取查询参数status的值，默认为-1

            req = {
                'status': status,
                'mix_kw': mix_kw,
                'p': page
            }
            user_data = []

            # 参数有效性查询
            if status:
                sql = "select * from cars where status='%s'" % (status)
                user_data = self.application.db.get_all_obj(sql, "cars")
                print("222222")
                print(user_data)
                print("222222")

            # 混合查询
            if mix_kw:
                sql = "select * from cars where carID like %s or position like %s"
                params = [('%' + mix_kw + '%'), ('%' + mix_kw + '%')]
                data = self.application.db.or_(sql, params)
                print("11111")
                print(data)
                print("11111")
                user_data = []
                for item in data:
                    tmp = {
                        'carID':item[0],
                        'position': item[1],
                        'workstate': item[2],
                        'time': item[3],
                        'longitude': item[4],
                        'latitude': item[5],
                        'status': item[6],
                    }
                    user_data.append(tmp)

            page_params = {
                'total': len(user_data),
                'page_size': config.page['PAGE_SIZE'],
                'page': page,
                'display': config.page['PAGE_DISPLAY'],
                'url': self.request.uri.replace("&p={}".format(page), "")
            }
            print(self.request.uri)

            pages = iPagination(page_params)

            offset = (int(page) - 1) * config.page['PAGE_SIZE']
            limit = config.page['PAGE_SIZE'] * page

            
            run_list =[]
            run_list = self.application.db.get_all_obj("select * from cars_run_info", "cars_run_info")

            if user_data != []:
                carlist = user_data

            # 用于存储每个 carID 最新数据的字典
            latest_data = {}

            for entry in run_list:
                carID = entry['carID']
                # 如果当前 carID 还没有记录，或者当前记录的 created_time 比已有记录的 created_time 更新
                if carID not in latest_data or entry['created_time'] > latest_data[carID]['created_time']:
                    latest_data[carID] = entry

            # 转换为列表格式
            carlist = list(latest_data.values())

            # else:
            #     if status == -1:
            #         list = self.application.db.get_all_obj("select * from cars order by carID desc limit %s offset %s" % (limit, offset), "cars")
            #     else:
            #         list = self.application.db.get_all_obj("select * from cars where status=0 order by carID desc limit %s offset %s" % (limit, offset), "cars")

            # if status == '-1' and mix_kw == '': #默认状态显示的数据（默认：未选择状态，未搜索词汇）
            #     list = self.application.db.get_all_obj("select * from cars order by carID desc limit %s offset %s" % (limit, offset), "cars")
            #     print(123)
            # if status == '0':
            #     print("I am coming")
            #     list = self.application.db.get_all_obj("select * from cars where status==0 order by carID desc limit %s offset %s" % (limit, offset), "cars")


            resp_data['list'] =carlist #resp_data['list'] 是小车基础信息数据
            resp_data['run_list'] = run_list
            print("list如下：")
            print(list)
            resp_data['pages'] = pages
            resp_data['search_con'] = req
            resp_data['status_mapping'] = config.STATUS_MAPPING
            resp_data['current_user'] = config.options['current_user']
            
            self.render("map/index2.html", resp_data=resp_data)
            # 渲染account/index.html模板并传入resp_data参数

        if h == "set":  # 如果h等于"set"
            resp_data = {}
            resp_data['current_user'] = config.options['current_user']  # 设置当前用户的信息

            carID = self.get_query_argument("carID", default=None)  # 获取查询参数id的值，默认为None
            info = {
                'carID': '',
                'position': '',
                'workstate': ''
                # 'time': '',
                # 'longitude': '',
                # 'latitude': ''
            }
            print(carID)
            if not carID:  # 如果uid为None
                self.render("map/set.html", info=info, resp_data=resp_data)
                # 渲染account/set.html模板并传入info和resp_data参数

            query_info = self.application.db.get_one("select * from cars where carID=%s" % (carID))

            print(query_info)
            info = {
                'carID': query_info[0],
                'position': query_info[1],
                'workstate': query_info[2],
                # 'time': query_info[3],
                # 'longitude': query_info[4],
                # 'latitude': query_info[5]
            }

            self.render("map/set.html", info=info, resp_data=resp_data)
            # 渲染account/set.html模板并传入info和resp_data参数

        if h == "test":  # 如果h等于"test"
            data = self.application.db.get_all_obj("select * from cars", "cars")
            print('data:',data)
            # 转换datetime为可JSON化的字符串（例如ISO格式）
            for item in data:
                item['updated_time'] = item['updated_time'].isoformat()
                item['created_time'] = item['created_time'].isoformat()

            # 将数据转换为JSON字符串
            json_data = json.dumps(data)
            print('json_data:',json_data)
            # 设置响应类型为JSON
            self.set_header("Content-Type", "application/json")

            # 输出JSON数据
            self.write(json_data)
                    
        if h == "api_yicaho":
            yichao_list = self.application.db.get_all_obj("select * from yichao","yichao")
            
            

            def convert_to_json_compatible(value):
                if isinstance(value, Decimal):
                    return float(value)
                elif isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    return value

            # 将'data'部分的tuple转换为dict，并应用转换函数
            keys = ['sequence', 'longitude', 'latitude', 'image', 'date', 'is_sanitized']
            

            if len(yichao_list)==1:
                for k,v in yichao_list:
                    yichao_list[k] = convert_to_json_compatible(v) 
            elif len(yichao_list) > 1:
                for i in range(len(yichao_list)):
                    yichao = yichao_list[i]
                    keys_list = ['id', 'longitude', 'latitude', 'image', 'date', 'is_sanitized']  # 使用不同的变量名
                    for k in keys_list:
                        yichao[k] = convert_to_json_compatible(yichao[k])
                    yichao_list[i] = yichao

            # 更新原响应数据中的'data'部分
            resp_data['yichao'] = yichao_list #resp_data['yichao'] 是所有的蚁巢信息
            resp_data['current_user'] = config.options['current_user']  # 设置当前用户的信息
            json_str = json.dumps(resp_data, ensure_ascii=True)
            # print("resp:", json_str)
            # print("successfully")
            self.write(json_str)  
        if h == "info":  # 如果h等于"info"
            resp_data['current_user'] = config.options['current_user']  # 设置当前用户的信息
            self.render("map/info.html", resp_data=resp_data)
            # 渲染account/info.html模板并传入resp_data参数
        if h == "api":  # 如果h等于"set"
            resp_data = {}
             # 如果h等于"index"
            
            self.render("map/api.html")
            # 渲染account/set.html模板并传入info和resp_data参数
        if h == 'data': #接口，用来给前端js提供数据  有用
            # 如果h等于"index"
            resp_data3 = {}
            carlist = []
            run_list =[]
            run_list = self.application.db.get_all_obj("select * from cars_run_info order by carID", "cars_run_info")
            # list = self.application.db.get_all_obj("select * from cars order by carID" , "cars")

            # 用于存储每个 carID 最新数据的字典
            latest_data = {}

            for entry in run_list:
                carID = entry['carID']
                # 如果当前 carID 还没有记录，或者当前记录的 created_time 比已有记录的 created_time 更新
                if carID not in latest_data or entry['created_time'] > latest_data[carID]['created_time']:
                    latest_data[carID] = entry

            # 转换为列表格式
            carlist = list(latest_data.values())


            print("run_list如下：")
            print(run_list)
            resp_data3['list'] = carlist #resp_data['list'] 是小车基础信息数据
            resp_data3['run_list'] = run_list
            print("carlist如下：")
            print(carlist)
            
            resp_data3['current_user'] = config.options['current_user']
            print("resp_data3如下：")
            print(resp_data3)
            # 将 Decimal 类型转换为 float
            for lst in [resp_data3['list'], resp_data3['run_list']]:
                for item in lst:
                    if 'longitude' in item and isinstance(item['longitude'], Decimal):
                        item['longitude'] = float(item['longitude'])
                    if 'latitude' in item and isinstance(item['latitude'], Decimal):
                        item['latitude'] = float(item['latitude'])
            # 将datetime对象转换为字符串
            for lst in [resp_data3['list'], resp_data3['run_list']]:
                for item in lst:
                    if 'updated_time' in item and isinstance(item['updated_time'], datetime):
                        item['updated_time'] = item['updated_time'].isoformat()
                    if 'created_time' in item and isinstance(item['created_time'], datetime):
                        item['created_time'] = item['created_time'].isoformat()

            # 将数据转换为JSON字符串
            json_data = json.dumps(resp_data3)

            # 设置响应类型为JSON
            self.set_header("Content-Type", "application/json")

            # 输出JSON数据
            self.write(json_data)
    def post(self, h):  # 处理HTTP POST请求
        # 添加账号操作
        if h == "index":
            resp = {
                        'code': 200,
                        'msg': "操作成功",
                        'data': {}
                    }
            #有空研究一下为什么这段跑不通
#             print()
             
#             longitude = self.get_body_argument("longitude")  # 获取表单参数经度的值
#             latitude = self.get_body_argument("latitude")  # 获取表单参数经度的值
#             print('longitude:',longitude)
#             print('latitude:',latitude)
#             point_msg= self.application.db.get_one("select * from yichao where latitude='%s' AND longitude='%s'" % (latitude,longitude))
#             # point_msg= self.application.db.get_one("select * from yichao where longitude='113.936783'")
#             sql = "select * from yichao"
#             all = self.application.db.get_all_obj(sql, "yichao")
#             print('all:',all)
#             print('point_msg:',point_msg)


#             def convert_to_json_compatible(value):
#                 if isinstance(value, Decimal):
#                     return float(value)
#                 elif isinstance(value, datetime):
#                     return value.strftime('%Y-%m-%d %H:%M:%S')
#                 elif isinstance(value, bytes):
#                     return value.decode('utf-8')  # 假定字节串是UTF-8编码的字符串
#                 else:
#                     return value

# # 将'data'部分的tuple转换为dict，并应用转换函数
#             keys = ['sequence', 'longitude', 'latitude', 'image', 'date', 'is_sanitized']
#             converted_data = {
#                 keys[i]: convert_to_json_compatible(value) 
#                 for i, value in enumerate(point_msg)
#             }

#             # 更新原响应数据中的'data'部分
#             resp['data']= converted_data

#             # 转换为JSON字符串
#             json_str = json.dumps(resp, ensure_ascii=False)
#             resp['data']= point_msg
            
#             print("index_resp:",json_str)
#             print("successfully")
#             self.write(json_str)  # 将resp作为HTTP响应返回

            try:
                # 解析请求体中的 JSON 数据
                body = self.request.body.decode('utf-8')
                data = json.loads(body)
                print('body:',body)
                longitude = data.get('longitude')
                latitude = data.get('latitude')
            except json.JSONDecodeError:
                self.set_status(400)
                self.write({'code': 400, 'msg': 'Invalid JSON format'})
                return
            except Exception as e:
                self.set_status(400)
                self.write({'code': 400, 'msg': str(e)})
                return

            if longitude is None or latitude is None:
                self.set_status(400)
                self.write({'code': 400, 'msg': 'Missing longitude or latitude'})
                return

            print('longitude:', longitude)
            print('latitude:', latitude)
            
            point_msg = self.application.db.get_one("select * from yichao where latitude=%s AND longitude=%s"%(latitude, longitude))

            def convert_to_json_compatible(value):
                if isinstance(value, Decimal):
                    return float(value)
                elif isinstance(value, datetime):
                    return value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, bytes):
                    return  base64.b64encode(value).decode()
                else:
                    return value

            # 将'data'部分的tuple转换为dict，并应用转换函数
            keys = ['sequence', 'longitude', 'latitude', 'image', 'date', 'is_sanitized']
            converted_data = {
                keys[i]: convert_to_json_compatible(value) 
                for i, value in enumerate(point_msg)
            }

            # 更新原响应数据中的'data'部分
            resp['data'] = converted_data

            # 转换为JSON字符串
            json_str = json.dumps(resp, ensure_ascii=True)
            print("resp:", json_str)
            print("successfully")
            self.write(json_str)  # 将resp作为HTTP响应返回

        if h == "set":  # 如果h等于"set"
            default_position = "深圳大学"  # 设置默认工作地点
            resp = {
                
            }

            position = self.get_body_argument("position", default=default_position)  # 获取表单参数nickname的值，默认为空字符串
            carID = self.get_body_argument("carID", default="1")  # 获取表单参数id的值，默认为0
            workstate = self.get_body_argument("workstate", default='0')
            # time = self.get_body_argument("position", default='')
            # longitude = self.get_body_argument("longitude", default='')
            # latitude = self.get_body_argument("latitude", default='')
            if position is None or len(position) < 1:  # 如果nickname为None或长度小于1
                resp['code'] = -1
                resp['msg'] = "请输入地名"
                self.write(resp)  # 将resp作为HTTP响应返回
            if workstate is None or len(workstate) < 1:  # 如果nickname为None或长度小于1
                resp['code'] = -1
                resp['msg'] = "请输入工作状态"
                self.write(resp)  # 将resp作为HTTP响应返回
            # if time is None or len(time) < 1:  # 如果nickname为None或长度小于1
            #     resp['code'] = -1
            #     resp['msg'] = "请输入时间戳"
            #     self.write(resp)  # 将resp作为HTTP响应返回
            # if longitude is None or len(longitude) < 1:  # 如果nickname为None或长度小于1
            #     resp['code'] = -1
            #     resp['msg'] = "请输入经度"
            #     self.write(resp)  # 将resp作为HTTP响应返回
            # if latitude is None or len(latitude) < 1:  # 如果nickname为None或长度小于1
            #     resp['code'] = -1
            #     resp['msg'] = "请输入纬度"
            #     self.write(resp)  # 将resp作为HTTP响应返回
            user_info = self.application.db.get_one("select * from cars where carID='%s'" % (carID))

            if user_info:  # 如果用户信息已存在
                self.application.db.update("UPDATE cars SET carID='%s',position='%s',workstate='%s' where carID='%s'" % (carID,position, workstate, carID))
            else:  # 如果用户信息不存在
               self.application.db.insert("insert into cars (carID,position,workstate) values ('%s','%s','%s')" % (carID,position, workstate))

            print("successfully")
            self.write(resp)  # 将resp作为HTTP响应返回

        if h == "api":  # 如果h等于"api"
            resp = {
                
            }
            print(resp)

            carID = self.get_body_argument("carID", default="1")
            workstate = self.get_body_argument("workstate", default='0')
            time = self.get_body_argument("time", default=0)
            longitude = self.get_body_argument("longitude", default=0)
            latitude = self.get_body_argument("latitude", default=0)
            is_sanitized = self.get_body_argument("is_sanitized", default=0)
            
            if "image" not in self.request.files:
                resp['code'] = -1
                resp['msg'] = "请输入图片"
                self.write(resp)
                return
            
            image_file = self.request.files["image"][0]
            image = image_file["body"]
            
            if not carID:
                resp['code'] = -1
                resp['msg'] = "请输入小车编号"
                self.write(resp)
                return
            if not workstate:
                resp['code'] = -1
                resp['msg'] = "请输入工作状态"
                self.write(resp)
                return
            if not time:
                resp['code'] = -1
                resp['msg'] = "请输入时间戳"
                self.write(resp)
                return
            if not longitude:
                resp['code'] = -1
                resp['msg'] = "请输入经度"
                self.write(resp)
                return
            if not latitude:
                resp['code'] = -1
                resp['msg'] = "请输入纬度"
                self.write(resp)
                return
            if not is_sanitized:
                resp['code'] = -1
                resp['msg'] = "请输入复查情况"
                self.write(resp)
                return

            self.application.db.insert("INSERT INTO cars_run_info (carID, time, workstate, longitude, latitude) VALUES (%s, %s, %s, %s, %s)"% (carID, time, workstate, longitude, latitude))
            # self.application.db.update("UPDATE cars SET workstate=%s WHERE carID=%s"%(workstate, carID))
            if workstate == "2" and image:
                image = base64.b64encode(image).decode()
                print(image)
                self.application.db.insert("INSERT INTO yichao (carID,longitude, latitude, image, is_sanitized) VALUES (%s,%s, %s, '%s', %s)"%(carID,longitude, latitude, image, is_sanitized))
                print("图片保存成功")
            print("successfully")
            self.write(json.dumps(resp))

        if h == "pause":
            resp = {
                'code': 200,
                'msg': "操作成功",
                'data': {}
            }
            try:
                body = json.loads(self.request.body)
                carID = body.get("carID", "1")
                start = body.get("start",0)
            except json.JSONDecodeError:
                resp['code'] = -1
                resp['msg'] = "无效的请求数据"
                self.write(json.dumps(resp))
                return

            if not carID:
                resp['code'] = -1
                resp['msg'] = "请输入小车编号"
                self.write(json.dumps(resp))
                return
            # if not start:
            #     resp['code'] = -1
            #     resp['msg'] = "请输入状态"
            #     self.write(json.dumps(resp))
            #     return
            

            # pause_list = self.application.db.get_all_obj("select * from pause_state", "pause_state")
            # self.application.db.insert("INSERT INTO pause_state (carID,start) VALUES (%s, %d)" % (carID, start))
            # self.application.db.update("UPDATE pause_state SET start=%d WHERE carID=%s"%(start, carID))
            self.write(json.dumps(resp))
        
        if h == "recall":
            resp = {
                'code': 200,
                'msg': "操作成功",
                'data': {}
            }
            try:
                body = json.loads(self.request.body)
                carID = body.get("carID", "1")
                longitude = body.get("longitude", 0)
                latitude = body.get("latitude", 0)
            except json.JSONDecodeError:
                resp['code'] = -1
                resp['msg'] = "无效的请求数据"
                self.write(json.dumps(resp))
                return

            if not carID:
                resp['code'] = -1
                resp['msg'] = "请输入小车编号"
                self.write(json.dumps(resp))
                return
            if not longitude:
                resp['code'] = -1
                resp['msg'] = "请输入经度"
                self.write(json.dumps(resp))
                return
            if not latitude:
                resp['code'] = -1
                resp['msg'] = "请输入纬度"
                self.write(json.dumps(resp))
                return

            give_point_list = self.application.db.get_all_obj("select * from give_point", "give_point")
            self.application.db.insert("INSERT INTO give_point (carID, longitude, latitude) VALUES (%s, %s, %s)" % (carID, longitude, latitude))
            self.write(json.dumps(resp))
    def delete(self, h):
        if h == "index":
                resp = {
                            'code': 200,
                            'msg': "操作成功",
                            'data': {}
                        }
                print(resp)
            
                carID = self.get_body_argument("carID", default="1")  # 获取表单参数id的值，默认为0
                # user_info = self.application.db.get_one("select * from cars where carID='%s'" % (carID))
                self.application.db.delete("DELETE from cars where carID='%s'" % (carID))
                self.application.db.delete("DELETE from cars_run_info where carID='%s'" % (carID))
                # self.application.db.delete("TRUNCATE TABLE yichao")
                

                print("successfully")
                self.write(resp)  # 将resp作为HTTP响应返回

    