# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:53:29 2026

@author: User
"""
import logging
from werkzeug.exceptions import HTTPException
from flask import Flask,jsonify
import os
from app.extensions import init_extensions
from app.routes import api
from app.auth import auth_bp
from app.docs import docs_bp
from app.page import page_bp
from app.exceptions import AppError
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
    
    if os.getenv("AUTO_CREATE_DB") == "1":
        with app.app_context():
            from app.extensions import db
            db.create_all()
        
    
    @app.get("/health")
    def health():
        return {"status":"ok"}
    
    app.register_blueprint(api)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(docs_bp)
    app.register_blueprint(page_bp)
    logging.basicConfig(
        level=logging.INFO,
        format= "%(asctime)s %(name)s %(levelname)s %(message)s" )
    register_error_handler(app)
    return app

def register_error_handler(app:Flask):
    @app.errorhandler(AppError)
    def handle_app_error(e:AppError):
        payload = {
            "error" : {
                "code" : e.status_code,
                "type" : e.error_type,
                "message" : e.message,
                "details" : e.details},
            "request_id": None
            }
        return jsonify(payload), e.status_code
    @app.errorhandler(HTTPException)
    def handle_HTTP_Exception(e:HTTPException):
        payload = {
            "error" : {
                "code" : e.code,
                "type" : (e.name or "http_exception").lower().replace(" ","_"),
                "message" : e.description,
                "details" : None},
            "request_id": None
            }
        return jsonify(payload), e.code
    @app.errorhandler(Exception)
    def handle_unexpected_error(e:Exception):
        logging.exception("Unhandled Exception")
        payload = {
            "error" : {
                "code" : 500,
                "type" : "internal_server_error",
                "message" : "internal server error",
                "details" : None},
            "request_id": None
            }
        return jsonify(payload), 500

    
    
    
    