# 这是一个测试接口文件

import requests

import json

# 面向对象

class  HttpAppTest :

    #实例方法

    def test_get(self,url,json_data={}): #声明默认参数 data没有数据改变的默认为空对象

    # 发起请
        res = requests.get(url,params=json_data)

        return res.text 

    def test_post(self, url, json_data={}):
        headers = {'Content-Type': 'application/json'}
        res = requests.post(url, json=json_data)
        return res.status_code , res.text

    def test_delete(self, url, json_data={}):
        headers = {'Content-Type': 'application/json'}
        res = requests.delete(url, json=json_data)
        return res.text
    

    def test_put(self, url, json_data={}):
        headers = {'Content-Type': 'application/json'}
        res = requests.put(url, json=json_data)
        return res.text
    

if __name__ == '__main__':
    http1 = HttpAppTest()
    
    
#     data ={
#         'carID': "13680",
#   "points": [
#     {
#       "latitude": "28.174492",
#       "longitude": "112.945643"
#     },
#     {
#       "latitude": "28.174892",
#       "longitude": "112.945743"
#     },
#     {
#       "latitude": "28.174992",
#       "longitude": "112.945843"
#     },
#     {
#       "latitude": "28.175092",
#       "longitude": "112.945943"
#     },
#     {
#       "latitude": "28.175192",
#       "longitude": "112.946043"
#     }
#   ]

# }


# ' http://172.30.235.77:5001'


    data ={
      'robot_position': {'longitude': '39.123123', 'latitude': '121.4737'},

      'target_position':{'longitude':'39.123123','latitude':'121.4737'}

    }

    res = http1.test_post("http://172.28.221.16:5003/navigation/", json_data=data)   
   
    print(res)

'''
    data = {
       
        
            "userLocation": {
                "latitude": 31.2304,
                "longitude": 121.4737
            },
            "waypoints": [
                {
                "latitude": 31.2345,
                "longitude": 121.4789,
                "peopleCount": 150
                },
                {
                "latitude": 31.2200,
                "longitude": 121.4600,
                "peopleCount": 200
                },
                {
                "latitude": 31.2400,
                "longitude": 121.4800,
                "peopleCount": 100
                },
                {
                "latitude": 31.2300,
                "longitude": 121.4700,
                "peopleCount": 50
                }
            ]
            

        }
'''