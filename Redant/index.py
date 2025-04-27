from database import *

import datetime


def create_time():
        """
            生成一个唯一的时间戳，精确到微秒。
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    
def insert_give_point( carID, lognitude, latitude):
    
    mydb = MySQLConnect()
    mycursor = mydb.cursor(dictionary=True)
    
    time = create_time()
    query = """
    INSERT INTO give_point (carID, longitude, latitude , created_time)
    VALUES (%s, %s, %s,%s)
    """
    values = (carID, lognitude, latitude,time)


    try:
        mycursor.execute(query, values)
        mydb.commit()
        print(f"成功插入 {mydb.sessison.rowcount} 条记录到 car_run_info 表中。")
    except mysql.connector.Error as e:
        mydb.rollback()
        print(f"插入失败: {e}")
    finally:
        mycursor.close()
        mydb.close()


if __name__ == "__main__":
    insert_give_point("334", 145.482030, 64.382360)