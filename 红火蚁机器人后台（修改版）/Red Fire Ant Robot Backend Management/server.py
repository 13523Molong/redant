import tornado.web
import tornado.ioloop
import tornado.httpserver
import config
from application import Application
import requests
import mysql.connector
import time
from views import index

# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "Hyx20040415",
#     "database": "MyNew"
# }

# API endpoints and headers
# api_endpoint = "http://192.168.137.84:9090/api/plugins/telemetry/DEVICE/b9c3a9f0-2e0b-11ee-8316-6565c6f8daff/values/timeseries"
# headers = {
#     "accept": "application/json",
#     "X-Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwidXNlcklkIjoiNGZlY2RlNzAtMWM3Yy0xMWVlLWFlM2ItN2Y4MjM5Y2MwMmYyIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiJjNjFkZmU3Ny04ZDY4LTRhYjMtYWRhZi1lN2JkOGVhZTdiNGMiLCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTY5MjgzOTc2MywiZXhwIjoxNjkyODQ4NzYzLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiNGQ0NjlkYTAtMWM3Yy0xMWVlLWFlM2ItN2Y4MjM5Y2MwMmYyIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.rs1HMJ4HMt8Dw7Wj5YSFWOy0ybJeNthLwZqcZAIjTXqS53YgK2V4BLVIUuYX06mtHoAyjkFyxyLlQExKERRLdA"
# }


def update_box_data(api_response):
    # Parse API response JSON
    response_data = api_response.json()
    e_heat = response_data["humidity"][0]["value"]
    e_wet = response_data["temperature"][0]["value"]

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    update_query = "UPDATwE box SET e_heat = %s, e_wet = %s WHERE id = 1"
    data = (e_heat, e_wet)

    cursor.execute(update_query, data)
    connection.commit()

    cursor.close()
    connection.close()
    print("Box data updated successfully")

# def data_update():
#     response = requests.get(api_endpoint, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         update_box_data(response)
#     else:
#         print(f"API request failed with status code: {response.status_code}")

#     # Wait for 1 second before making the next request
#     time.sleep(1)
    


if __name__ == '__main__':
    app = Application()
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(config.options["port"])


    # 开启两个进程
    # httpServer.bind(config.options['port'])
    # httpServer.start(2)
    tornado.ioloop.IOLoop.current().start()
    


