# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:53:29 2026

@author: User
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
db = SQLAlchemy()
migrate = Migrate()
# 宣告 extension 但尚未綁定 app

jwt = JWTManager()
def init_extensions(app):
    # 統一在這裡初始化所有 extensions。
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    
    # 先把 extension 綁定 app，再載入 models，確保 ORM metadata 在正確的 app context 下建立。
    # 這樣 migration 掃描 metadata 才穩定。

    # models 裡的 db.Model 需要「已初始化的 db」
    # 如果models 在 import 時就已經建立 class
    # 但 db 還沒綁 app
    # 在 migration 或 metadata 掃描時可能出問題。
    
    # (partially initialized module)circular import 是模組之間互相依賴尚未完成初始化(定義)的物件所導致。