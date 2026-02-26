# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:53:29 2026

@author: User
"""
from flask import Flask
import os
from .extensions import init_extensions
from .routes import api
from .auth import auth_bp
def create_app(config_override=None):
    app = Flask(__name__)
    # 用app factory方式寫，不放在全域
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS",False)
    app.config.setdefault("TESTING",False)
    app.config.setdefault(
                          "JWT_SECRET_KEY",
                          os.getenv("JWT_SECRET_KEY","dev-only-change-me"))
    # 開發用 fallback
    # fallback 只在 dev / testing 允許。production 缺就炸（raise）或至少在非 dev 環境炸掉。
    if os.getenv("DATABASE_URL"):
        app.config.setdefault("SQLALCHEMY_DATABASE_URI",os.getenv("DATABASE_URL"))
    # set default再override避免override被蓋掉
    if config_override :
        app.config.update(config_override)
    
    
    database_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    if not database_url:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI/DATABASE_URL not set")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    
    init_extensions(app)  
        
    # ensure models are registered for migrations / metadata
    from . import models
    
    @app.get("/health")
    def health():
        return {"status":"ok"}
    
    app.register_blueprint(api)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    return app

    
    
    
    