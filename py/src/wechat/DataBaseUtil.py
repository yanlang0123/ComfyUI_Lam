# -*- coding: utf-8 -*-
import sys
import os
import folder_paths
import time
import threading
import sqlite3
import hashlib
import secrets
from contextlib import contextmanager
from typing import Optional, List, Tuple, Any, Union, Dict
from .config import singleton

lock = threading.Lock()

def run_with_lock(func):
    """线程锁装饰器"""
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper

def generate_salt() -> str:
    """生成随机盐值"""
    return secrets.token_hex(16)

def hash_password(password: str, salt: str) -> str:
    """使用sha256加密密码"""
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password: str, salt: str, hashed: str) -> bool:
    """验证密码"""
    return hash_password(password, salt) == hashed

@singleton
class DataBaseUtil:
    """
    简单sqlite数据库工具类
    封装sqlite数据库操作，提供常用的CRUD方法
    """
    
    # 表结构定义
    USERS_TABLE_SQL = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,              
            openId TEXT NOT NULL,
            type TEXT NOT NULL,
            command TEXT NOT NULL,              
            prompt_id TEXT NOT NULL,
            status TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            outputs TEXT
        )
    '''
    
    USER_RECHARGE_TABLE_SQL = '''
        CREATE TABLE IF NOT EXISTS user_recharge (
            id INTEGER PRIMARY KEY,              
            openId TEXT NOT NULL,
            frequency INTEGER NOT NULL,
            recharge_time TEXT NOT NULL
        )
    '''
    
    USER_ACCOUNT_TABLE_SQL = '''
        CREATE TABLE IF NOT EXISTS user_account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            openId TEXT,
            nickname TEXT,
            avatar_url TEXT,
            status TEXT DEFAULT 'active',
            user_type TEXT DEFAULT 'normal',
            created_time TEXT NOT NULL,
            last_login_time TEXT,
            login_count INTEGER DEFAULT 0,
            frequency INTEGER DEFAULT 0,
            CONSTRAINT username_unique UNIQUE (username),
            CONSTRAINT email_unique UNIQUE (email)
        )
    '''

    def __init__(self, db_name: str = "lamWeChat.db"):
        """
        初始化数据库连接
        
        Args:
            db_name: 数据库文件名，以'.db'结尾
        """
        self.isUsable = True
        self._conn = None
        self._cur = None
        
        try:
            base_path = folder_paths.folder_names_and_paths['custom_nodes'][0][0]
            self.db_path = os.path.join(base_path, 'ComfyUI_Lam', 'config', db_name)
            is_new = not os.path.exists(self.db_path)
            
            # 连接数据库，允许多线程
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._cur = self._conn.cursor()
            
            # 创建表
            self._initialize_tables()
                
        except Exception as e:
            self.isUsable = False
            print(f'[DataBaseUtil] SQLite数据库初始化失败: {e}')

    def _initialize_tables(self) -> None:
        """初始化数据库表"""
        try:
            self.create_table(self.USERS_TABLE_SQL)
            self.create_table(self.USER_RECHARGE_TABLE_SQL)
            self.create_table(self.USER_ACCOUNT_TABLE_SQL)
            
            # 为用户表创建索引以提高查询性能
            self._create_indexes()
            print("[DataBaseUtil] 数据库表初始化成功")
        except Exception as e:
            print(f"[DataBaseUtil] 数据库表初始化失败: {e}")
            raise

    def _create_indexes(self) -> None:
        """创建索引"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_user_account_username ON user_account(username)",
            "CREATE INDEX IF NOT EXISTS idx_user_account_email ON user_account(email)",
            "CREATE INDEX IF NOT EXISTS idx_user_account_openId ON user_account(openId)",
            "CREATE INDEX IF NOT EXISTS idx_users_openId ON users(openId)",
            "CREATE INDEX IF NOT EXISTS idx_users_prompt_id ON users(prompt_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_recharge_openId ON user_recharge(openId)"
        ]
        
        for index_sql in indexes:
            try:
                self._cur.execute(index_sql)
            except Exception as e:
                print(f"[DataBaseUtil] 创建索引失败: {e}")

    @contextmanager
    def _get_cursor(self):
        """获取游标的上下文管理器，确保游标正确关闭"""
        cursor = self._conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def close_con(self) -> None:
        """关闭数据库连接"""
        try:
            if self._cur:
                self._cur.close()
            if self._conn:
                self._conn.close()
            print("[DataBaseUtil] 数据库连接已关闭")
        except Exception as e:
            print(f"[DataBaseUtil] 关闭数据库连接时出错: {e}")

    def __del__(self):
        """析构函数，确保连接被关闭"""
        self.close_con()

    def _check_connection(self) -> bool:
        """检查数据库连接是否可用"""
        if not self.isUsable or not self._conn:
            print("[DataBaseUtil] 数据库连接不可用")
            return False
        return True

    def create_table(self, sql: str) -> bool:
        """
        创建数据表
        
        Args:
            sql: CREATE TABLE SQL语句
            
        Returns:
            bool: 创建成功返回True，失败返回False
        """
        if not self._check_connection():
            return False
            
        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print(f"[DataBaseUtil] 创建表失败: {e}")
            return False

    def drop_table(self, sql: str) -> bool:
        """
        删除数据表
        
        Args:
            sql: DROP TABLE SQL语句
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        if not self._check_connection():
            return False
            
        try:
            self._cur.execute(sql)
            self._conn.commit()
            print("[DataBaseUtil] 删除表成功")
            return True
        except Exception as e:
            print(f"[DataBaseUtil] 删除表失败: {e}")
            return False

    @run_with_lock
    def operate_one(self, sql: str, value: tuple) -> bool:
        """
        插入或更新单条表记录
        
        Args:
            sql: INSERT 或 UPDATE SQL语句
            value: 参数值元组
            
        Returns:
            bool: 操作成功返回True，失败返回False
        """
        if not self._check_connection():
            return False
            
        with self._get_cursor() as cursor:
            try:
                cursor.execute(sql, value)
                self._conn.commit()
                return True
            except Exception as e:
                print(f"[DataBaseUtil] 操作记录失败: {e}")
                self._conn.rollback()
                return False

    @run_with_lock
    def operate_many(self, sql: str, value: list) -> bool:
        """
        插入或更新多条表记录
        
        Args:
            sql: INSERT 或 UPDATE SQL语句
            value: 参数值列表
            
        Returns:
            bool: 操作成功返回True，失败返回False
        """
        if not self._check_connection():
            return False
            
        with self._get_cursor() as cursor:
            try:
                cursor.executemany(sql, value)
                self._conn.commit()
                return True
            except Exception as e:
                print(f"[DataBaseUtil] 操作多条记录失败: {e}")
                self._conn.rollback()
                return False

    @run_with_lock
    def delete_record(self, sql: str, params: tuple = None) -> bool:
        """
        删除表记录
        
        Args:
            sql: DELETE SQL语句
            params: 参数值元组
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        if not self._check_connection():
            return False
            
        if 'DELETE' not in sql.upper():
            print("[DataBaseUtil] SQL语句不是DELETE操作")
            return False
            
        with self._get_cursor() as cursor:
            try:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                self._conn.commit()
                return True
            except Exception as e:
                print(f"[DataBaseUtil] 删除记录失败: {e}")
                return False

    def query_one(self, sql: str, params: tuple = None) -> Optional[Tuple]:
        """
        查询单条数据
        
        Args:
            sql: SELECT SQL语句
            params: 查询参数
            
        Returns:
            Optional[Tuple]: 查询结果，失败返回None
        """
        if not self._check_connection():
            return None
            
        try:
            if params:
                self._cur.execute(sql, params)
            else:
                self._cur.execute(sql)
            return self._cur.fetchone()
        except Exception as e:
            print(f"[DataBaseUtil] 查询单条记录失败: {e}")
            return None

    def query_many(self, sql: str, params: tuple = None) -> List[Tuple]:
        """
        查询多条数据
        
        Args:
            sql: SELECT SQL语句
            params: 查询参数
            
        Returns:
            List[Tuple]: 查询结果列表，失败返回空列表
        """
        if not self._check_connection():
            return []
            
        try:
            if params:
                self._cur.execute(sql, params)
            else:
                self._cur.execute(sql)
            return self._cur.fetchall()
        except Exception as e:
            print(f"[DataBaseUtil] 查询多条记录失败: {e}")
            return []

    # 用户账户相关方法
    @run_with_lock
    def register_user(self, username: str, password: str, email: str = None, 
                     phone: str = None, nickname: str = None, openId: str = None,
                     avatar_url: str = None, user_type: str = "normal") -> Dict[str, Any]:
        """
        用户注册
        
        Args:
            username: 用户名
            password: 密码
            email: 邮箱
            phone: 手机号
            nickname: 昵称
            openId: 微信openId
            avatar_url: 头像URL
            user_type: 用户类型
            
        Returns:
            Dict: 注册结果
        """
        try:
            # 检查用户名是否已存在
            if self.get_user_by_username(username):
                return {"success": False, "message": "用户名已存在"}
            
            # 检查邮箱是否已存在
            if email and self.get_user_by_email(email):
                return {"success": False, "message": "邮箱已被注册"}
            
            # 生成盐值和密码哈希
            salt = generate_salt()
            password_hash = hash_password(password, salt)
            created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # 插入用户记录
            sql = """
                INSERT INTO user_account 
                (username, password_hash, salt, email, phone, openId, nickname, avatar_url, user_type, created_time, frequency) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (username, password_hash, salt, email, phone, openId, nickname, avatar_url, user_type, created_time, 0)
            
            if self.operate_one(sql, params):
                user_id = self._cur.lastrowid
                return {
                    "success": True, 
                    "message": "注册成功", 
                    "user_id": user_id,
                    "username": username
                }
            else:
                return {"success": False, "message": "注册失败"}
                
        except Exception as e:
            print(f"[DataBaseUtil] 用户注册失败: {e}")
            return {"success": False, "message": f"注册失败: {str(e)}"}

    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户登录
        
        Args:
            username: 用户名或邮箱
            password: 密码
            
        Returns:
            Dict: 登录结果
        """
        try:
            # 首先尝试用用户名查找
            user = self.get_user_by_username(username)
            if not user:
                # 如果用户名没找到，尝试用邮箱查找
                user = self.get_user_by_email(username)
            
            if not user:
                return {"success": False, "message": "用户不存在"}
            
            # 解包用户数据
            user_id, db_username, password_hash, salt, email, phone, openId, nickname, \
            avatar_url, status, user_type, created_time, last_login_time, login_count, frequency = user
            
            # 检查用户状态
            if status != 'active':
                return {"success": False, "message": "账户已被禁用"}
            
            # 验证密码
            if not verify_password(password, salt, password_hash):
                return {"success": False, "message": "密码错误"}
            
            # 更新登录信息
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            update_sql = """
                UPDATE user_account 
                SET last_login_time = ?, login_count = login_count + 1 
                WHERE id = ?
            """
            self.operate_one(update_sql, (current_time, user_id))
            
            # 返回用户信息（不包含敏感信息）
            user_info = {
                "user_id": user_id,
                "username": db_username,
                "email": email,
                "phone": phone,
                "nickname": nickname,
                "avatar_url": avatar_url,
                "user_type": user_type,
                "last_login_time": current_time,
                "login_count": login_count + 1,
                "frequency": frequency
            }
            
            return {
                "success": True, 
                "message": "登录成功", 
                "user_info": user_info
            }
            
        except Exception as e:
            print(f"[DataBaseUtil] 用户登录失败: {e}")
            return {"success": False, "message": f"登录失败: {str(e)}"}

    def get_user_by_username(self, username: str) -> Optional[Tuple]:
        """根据用户名获取用户信息"""
        return self.query_one("SELECT * FROM user_account WHERE username = ?", (username,))

    def get_user_by_email(self, email: str) -> Optional[Tuple]:
        """根据邮箱获取用户信息"""
        return self.query_one("SELECT * FROM user_account WHERE email = ?", (email,))

    def get_user_by_id(self, user_id: int) -> Optional[Tuple]:
        """根据用户ID获取用户信息"""
        return self.query_one("SELECT * FROM user_account WHERE id = ?", (user_id,))

    def get_user_by_openid(self, openId: str) -> Optional[Tuple]:
        """根据openId获取用户信息"""
        return self.query_one("SELECT * FROM user_account WHERE openId = ?", (openId,))

    @run_with_lock
    def update_user_profile(self, user_id: int, **kwargs) -> bool:
        """
        更新用户资料
        
        Args:
            user_id: 用户ID
            **kwargs: 要更新的字段
            
        Returns:
            bool: 更新成功返回True
        """
        allowed_fields = ['email', 'phone', 'nickname', 'avatar_url', 'user_type', 'status']
        update_fields = []
        params = []
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                update_fields.append(f"{field} = ?")
                params.append(value)
        
        if not update_fields:
            return False
        
        params.append(user_id)
        sql = f"UPDATE user_account SET {', '.join(update_fields)} WHERE id = ?"
        
        return self.operate_one(sql, tuple(params))

    @run_with_lock
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        修改密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            Dict: 修改结果
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "message": "用户不存在"}
        
        _, username, password_hash, salt, *_ = user
        
        # 验证旧密码
        if not verify_password(old_password, salt, password_hash):
            return {"success": False, "message": "旧密码错误"}
        
        # 生成新密码哈希
        new_salt = generate_salt()
        new_password_hash = hash_password(new_password, new_salt)
        
        # 更新密码
        sql = "UPDATE user_account SET password_hash = ?, salt = ? WHERE id = ?"
        if self.operate_one(sql, (new_password_hash, new_salt, user_id)):
            return {"success": True, "message": "密码修改成功"}
        else:
            return {"success": False, "message": "密码修改失败"}

    @run_with_lock
    def reset_password(self, email: str, new_password: str) -> Dict[str, Any]:
        """
        重置密码
        
        Args:
            email: 邮箱
            new_password: 新密码
            
        Returns:
            Dict: 重置结果
        """
        user = self.get_user_by_email(email)
        if not user:
            return {"success": False, "message": "邮箱不存在"}
        
        user_id = user[0]
        
        # 生成新密码哈希
        new_salt = generate_salt()
        new_password_hash = hash_password(new_password, new_salt)
        
        # 更新密码
        sql = "UPDATE user_account SET password_hash = ?, salt = ? WHERE id = ?"
        if self.operate_one(sql, (new_password_hash, new_salt, user_id)):
            return {"success": True, "message": "密码重置成功"}
        else:
            return {"success": False, "message": "密码重置失败"}

    @run_with_lock
    def update_user_frequency(self, user_id: int, frequency_change: int) -> bool:
        """
        更新用户使用次数
        
        Args:
            user_id: 用户ID
            frequency_change: 次数变化量（正数为增加，负数为减少）
            
        Returns:
            bool: 更新成功返回True
        """
        sql = "UPDATE user_account SET frequency = frequency + ? WHERE id = ?"
        return self.operate_one(sql, (frequency_change, user_id))

    @run_with_lock
    def bind_openid(self, user_id: int, openId: str) -> bool:
        """
        绑定微信openId
        
        Args:
            user_id: 用户ID
            openId: 微信openId
            
        Returns:
            bool: 绑定成功返回True
        """
        sql = "UPDATE user_account SET openId = ? WHERE id = ?"
        return self.operate_one(sql, (openId, user_id))

    # 原有的业务方法保持不变
    def insert_data(self, openId: str, type_name: str, command: str, prompt_id: str, 
                   status: str, start_time: str, end_time: str = None, outputs: str = None) -> bool:
        """插入用户数据"""
        return self.operate_one(
            "INSERT INTO users (openId, type, command, prompt_id, status, start_time, end_time, outputs) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            (openId, type_name, command, prompt_id, status, start_time, end_time, outputs)
        )

    def get_data(self, openId: str, prompt_id: str) -> Optional[Tuple]:
        """根据openId和prompt_id获取数据"""
        return self.query_one("SELECT * FROM users WHERE openId = ? AND prompt_id = ?", (openId, prompt_id))

    def update_data(self, status: str, end_time: str, outputs: str, prompt_id: str) -> bool:
        """更新用户数据"""
        return self.operate_one(
            "UPDATE users SET status = ?, end_time = ?, outputs = ? WHERE prompt_id = ?",
            (status, end_time, outputs, prompt_id)
        )

    def delete_data(self, prompt_id: str) -> bool:
        """根据prompt_id删除数据"""
        return self.delete_record("DELETE FROM users WHERE prompt_id = ?", (prompt_id,))

    def get_many_data(self, openId: str, type_name: str, page_number: int = 1, page_size: int = 10) -> List[Tuple]:
        """分页查询用户数据"""
        offset = (page_number - 1) * page_size
        return self.query_many(
            "SELECT * FROM users WHERE openId = ? AND type = ? ORDER BY start_time DESC LIMIT ? OFFSET ?", 
            (openId, type_name, page_size, offset)
        )

    def user_recharge(self, openId: str, frequency: int) -> bool:
        """用户充值"""
        recharge_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return self.operate_one(
            "INSERT INTO user_recharge (openId, frequency, recharge_time) VALUES (?, ?, ?)", 
            (openId, frequency, recharge_time)
        )

    def get_user_frequency(self, openId: str) -> Optional[Tuple]:
        """获取用户总充值次数"""
        return self.query_one("SELECT SUM(frequency) FROM user_recharge WHERE openId = ?", (openId,))

    def get_user_task_count(self, openId: str) -> Optional[Tuple]:
        """获取用户任务数量"""
        return self.query_one("SELECT COUNT(*) FROM users WHERE openId = ?", (openId,))