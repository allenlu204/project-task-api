# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 20:18:37 2026

@author: User
"""

import os
from urllib.parse import urlparse
import pymysql

def DBClient():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")
    parsed = urlparse(url)
    # 解析url為字串，但會解出/
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port or 3306
    dbname = parsed.path.lstrip("/")
    # path = "/taskdb"
    # pymysql.connect(database=?)
    # 不接受 "/taskdb"
    # taskdb
    # 所以去掉斜線。
    # 這是 字串格式問題。
    return pymysql.connect(
        user = user,
        password = password,
        host = host,
        port = port,
        dbname = dbname,
        curclass = pymysql.cursors.DictCursor,
        # 不寫會回傳[('users',)] --> [{'Tables_in_taskdb': 'users'}] 為資料結構差異
        )

class DBclient:
    def __init__(self,database_url:str | None = None):
        self.database_url = database_url or os.getenv("DATABASE_URL")
        if not self.database_url:
            raise RuntimeError("DATABASE_URL not set")
        self._conn = None
        
    def connect(self):
        if self._conn is None:
            cfg = DBClient(self.database_url)
            # 把 URL 轉成 pymysql 的參數 dict。
            self._conn = pymysql.connect(
                curclass = pymysql.cursors.DictCursor,
                **cfg)
            # pymysql.cursors.DictCursor讓 fetchall() 回來是 list[dict]，每列用欄位名當 key。
    # 不然預設多半是 tuple，比較不好讀。
    # 只連一次，之後重用
    # 只有在還沒連線時才 connect,connection caching / lazy init。
    # **cfg
    # dict unpacking：把 cfg 的 key/value 展開成命名參數。
    # 等同 host=..., user=..., password=..., port=..., database=...
            return self._conn
            # 不管本次是新連線或舊連線，都回傳 connection。
    
    def query(self,sql:str,params = None):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(sql,params)
            return cur.fetcall()
        
    def execute(self,sql:str,params = None):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(sql,params)
            return cur.commit()
        
    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        