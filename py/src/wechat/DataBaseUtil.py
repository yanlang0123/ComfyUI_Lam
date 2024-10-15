# -*- coding: utf-8 -*-
import sys
import os
import folder_paths
import time
class DataBaseUtil():
    """
       简单sqlite数据库工具类
       编写这个类主要是为了封装sqlite，继承此类复用方法
       """

    def __init__(self, dbName="lamWeChat.db"):
        """
        初始化连接——使用完需关闭连接
        :param dbName: 连接库的名字，注意，以'.db'结尾
        """
        self.isUsable=True
        try:
            import sqlite3
            basePath = folder_paths.folder_names_and_paths['custom_nodes'][0][0]
            self.db_path = os.path.join(basePath, 'ComfyUI_Lam', 'config', dbName)
            isNew=os.path.exists(self.db_path)
            # 连接数据库
            self._conn = sqlite3.connect(self.db_path)
            # 创建游标
            self._cur = self._conn.cursor()
            if isNew==False:
                # 创建数据表 用户任务表
                users_tb_sql ='''
                                CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,              
                                    openId TEXT  NOT NULL,
                                    command TEXT NOT NULL,              
                                    prompt_id TEXT NOT NULL,
                                    status TEXT NOT NULL,
                                    start_time TEXT NOT NULL,
                                    end_time TEXT,
                                    outputs TEXT
                                )
                            '''
                self.create_tabel(users_tb_sql)
                # 用户充值记录表
                user_recharge_sql ='''
                                CREATE TABLE IF NOT EXISTS user_recharge (
                                    id INTEGER PRIMARY KEY,              
                                    openId TEXT  NOT NULL,
                                    frequency INTEGER NOT NULL,
                                    recharge_time TEXT NOT NULL
                                )
                            '''
                self.create_tabel(user_recharge_sql)
        except:  
            self.isUsable=False
            print('sqlite数据库不可用')



    def close_con(self):
        """关闭连接对象——主动调用
            :return:
            """
        self._cur.close()
        self._conn.close()
    # 创建数据表
    def create_tabel(self, sql: str):
        """
            创建表
            :param sql: create sql语句
            :return: True表示创建表成功
            """
        try:
            self._cur.execute(sql)
            self._conn.commit()
            print("[create table success]")
            return True
        except Exception as e:
            print("[create table error]", e)
    # 删除数据表
    def drop_table(self, sql: str):
        """
            删除表
            :param sql: drop sql语句
            :return: True表示删除成功
            """
        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print("[drop table error]", e)
            return False
    # 插入或更新表数据，一次插入或更新一条数据
    def operate_one(self, sql: str, value: tuple):
        """
            插入或更新单条表记录
            :param sql: insert语句或update语句
            :param value: 插入或更新的值，形如（）
            :return: True表示插入或更新成功
            """
        try:
            self._cur.execute(sql, value)
            self._conn.commit()
            if 'INSERT' in sql.upper():
                print("[insert one record success]")
            if 'UPDATE' in sql.upper():
                print("[update one record success]")
            return True
        except Exception as e:
            print("[insert/update one record error]", e)
            self._conn.rollback()
            return False
    # 插入或更新表数据，一次插入或更新多条数据
    def operate_many(self, sql: str, value: list):
        """
            插入或更新多条表记录
            :param sql: insert语句或update语句
            :param value: 插入或更新的字段的具体值，列表形式为list:[(),()]
            :return: True表示插入或更新成功
            """
        try:
            # 调用executemany()方法
            self._cur.executemany(sql, value)
            self._conn.commit()
            if 'INSERT' in sql.upper():
                print("[insert many  records success]")
            if 'UPDATE' in sql.upper():
                print("[update many  records success]")
            return True
        except Exception as e:
            print("[insert/update many  records error]", e)
            self._conn.rollback()
            return False
    # 删除表数据
    def delete_record(self, sql: str):
        """
            删除表记录
            :param sql: 删除记录SQL语句
            :return: True表示删除成功
            """
        try:
            if 'DELETE' in sql.upper():
                self._cur.execute(sql)
                self._conn.commit()
                #print("[detele record success]")
                return True
            else:
                print("[sql is not delete]")
                return False
        except Exception as e:
            print("[detele record error]", e)
            return False
    # 查询一条数据
    def query_one(self, sql: str, params=None):
        """
            查询单条数据
            :param sql: select语句
            :param params: 查询参数，形如()
            :return: 语句查询单条结果
            """
        try:
            if params:
                self._cur.execute(sql, params)
            else:
                self._cur.execute(sql)
            # 调用fetchone()方法
            r = self._cur.fetchone()
            #print("[select one record success]")
            return r
        except Exception as e:
            print("[select one record error]", e)
    # 查询多条数据
    def query_many(self, sql: str, params=None):
        """
            查询多条数据
            :param sql: select语句
            :param params: 查询参数，形如()
            :return: 语句查询多条结果
            """
        try:
            if params:
                self._cur.execute(sql, params)
            else:
                self._cur.execute(sql)
            # 调用fetchall()方法
            r = self._cur.fetchall()
            #print("[select many records success]")
            return r
        except Exception as e:
            print("[select many records error]", e)
    def insert_data(self, openId, command, prompt_id,status,start_time, end_time, outputs):
        self.operate_one("INSERT INTO users (openId, command,prompt_id,status, start_time, end_time, outputs) VALUES (?, ?,?, ?, ?, ?,?)", (
            openId, command, prompt_id,status,start_time, end_time, outputs))

    def get_data(self, openId,prompt_id):
        return self.query_one("SELECT * FROM users WHERE openId = ? and prompt_id=? ", (openId,prompt_id))

    def update_data(self, status, end_time, outputs,prompt_id):
        self.operate_one("UPDATE users SET status=?,end_time = ?, outputs = ? WHERE prompt_id = ?",
                          (status, end_time, outputs, prompt_id))
        
    def delete_data(self,prompt_id):
        self.operate_one("DELETE FROM users WHERE prompt_id = ?",
                          (prompt_id,))
    
    def get_many_data(self, openId,page_number = 1,page_size = 10):
        offset = (page_number - 1) * page_size
        return self.query_many("SELECT * FROM users WHERE openId=? ORDER BY start_time DESC LIMIT ? OFFSET ?", (openId,page_size,offset))

    def user_recharge(self,openId,frequency):
        now = time.localtime()
        recharge_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        self.operate_one("INSERT INTO user_recharge (openId,frequency,recharge_time) VALUES (?, ?,?)", (openId, frequency, recharge_time))

    def get_user_frequency(self,openId):
        return self.query_one("SELECT sum(frequency) FROM user_recharge WHERE openId=? ", (openId,))
    
    def get_user_task_count(self,openId):
        return self.query_one("SELECT count(*) FROM users WHERE openId=? ", (openId,))
    

# db=DataBaseUtil()
# db.delete_data("ba5d5d71-13b3-4c19-b2ce-7a60a0f0b2e7")
#db.delete_record('DELETE FROM users where command="图生视频"')
#data=db.get_user_task_count('oJNTS6vtlfGKyivfY6loLLScQ3FQ')
#data=db.get_data('oJNTS6vtlfGKyivfY6loLLScQ3FQ','02b73c61-6f18-4432-837a-dd64d9424ed7')
#print(data)


    
   
