import mysql.connector
import pymysql


class usrSQL():
    def __init__(self, host, user, passwd, dbName):
        self.host = host
        self.port = 3306
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        
    def connect(self):
        # 连接数据库
        self.db = mysql.connector.connect(
            host=self.host,
            port = 3306,
            user=self.user,
            password=self.passwd,
            database=self.dbName,
        )
        self.cursor = self.db.cursor()
        # 测试代码以下：
        current_database = self.db.database
        print("当前数据库名称：", current_database)

    def close(self):
        # 关闭数据库连接和游标
        self.cursor.close()
        self.db.close()

    def get_one(self, sql):
        # 执行查询，并返回查询结果的第一行
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print("查询失败1")
        return res

    def get_all(self, sql):
        # 执行查询，并返回查询结果的所有行
        res = ()
        try:
            try:
                self.connect()
                print("连接数据库成功。")
            except mysql.connector.Error as error:
                print("连接到MySQL时出错:", error)
            try:
                self.cursor.execute(sql)
                print("sql注入成功。")
            except mysql.connector.Error as error:
                print("执行MySQL时出错:", error)
            # self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
            
            # try:
            #     self.cursor.fetchall()
            #     print("2成功。")
            # except mysql.connector.Error as error:
            #     print("fetchall MySQL时出错:", error)
            # try:
            #     self.close()
            #     print("3成功。")
            # except mysql.connector.Error as error:
            #     print("关闭MySQL时出错:", error)
        except:
            print("查询失败2")
        return res

    def get_all_obj(self, sql, tableName, *args):
        # 执行查询，并返回查询结果的所有行作为字典的列表
        resList = []
        fieldsList = []
        if len(args) > 0:
            for item in args:
                fieldsList.append(item)
        else:
            fieldsSql = "select COLUMN_NAME from information_schema.COLUMNS where table_name ='%s'and table_schema = '%s' ORDER BY ORDINAL_POSITION" % (
                tableName, self.dbName)
            fields = self.get_all(fieldsSql)
            for item in fields:
                fieldsList.append(item[0])

        res = self.get_all(sql)
        for item in res:
            obj = {}
            count = 0
            for x in item:
                obj[fieldsList[count]] = x
                count += 1
            resList.append(obj)
        return resList

    def insert(self, sql):
        # 执行插入操作，并返回受影响的行数
        return self.__edit(sql)

    def update(self, sql):
        # 执行更新操作，并返回受影响的行数
        return self.__edit(sql)

    def delete(self, sql):
        # 执行删除操作，并返回受影响的行数
        return self.__edit(sql)

    def __edit(self, sql):
        # 执行插入、更新、删除操作的辅助方法
        count = 0
        try:
            self.connect()
            self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except mysql.connector.Error as error:
            print("执行MySQL时出错:", error)
            print("事务提交失败")
            self.db.rollback()
        return count

    def or_(self, sql, params):
        # 执行带有参数的查询，并返回查询结果的所有行
        self.connect()
        num = self.cursor.execute(sql, params)
        db = []
        for x in range(num):
            tmp = self.cursor.fetchone()
            db.append(tmp)
        return db

