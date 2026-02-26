# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 07:22:29 2026

@author: User
"""
from db_client import DBClient
import pymysql
def main():
    db = DBClient()
    try:
        print("======SHOW TABLES=====")
        tables = db.query("SHOW TABLES;")
        print(tables)
        print("=====SELECT 1=====")
        result = db.query("SELECT 1;")
        print(result)
        
        print("=====DESCRIBE USERS=====")
        try:
            desc = db.query("DESCRIBE users;")
            print(desc)
        except pymysql.MySQLError as e:
            print("Describe user failed",repr(e))
        # SHOW TABLES/SELECT 1 失敗就直接判定「DB 整體有問題」
        # 但 DESCRIBE users 失敗可能只是「users 表還沒建立」，這不是 DB 掛掉
        db.execute("""CREATE TABLE IF NOT EXISTS scrach (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   note VARCHAR(255));"""),
        db.execute("INSERT INTO scrach (note) VALUES (%s);",("hello",))    
        rows = db.query("SELECT * FROM scrach ORDER BY id DESC LIMIT 5;")
        print(rows)
        
        
        
    finally:
        db.close()
    # 不管中間成功或失敗，都一定會執行 db.close()，避免連線資源外洩。
    # 沒有 finally，你的程式遇到 exception 就跳出去，conn 不一定會 close。
# def scrach():
#     create = db.query("CREATE TABLE IF NOT EXIST scrach (id INT AUTO_INCREMENT PRIMARY KEY,note VARCHAR(255));"
#                       )
if __name__ == "__main__":
    main()
    # 只有「直接執行這個檔案」時才跑 main()
    # 被 import 時不會執行
        

