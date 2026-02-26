# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 11:17:14 2026

@author: User
"""

from flask import Blueprint, request, abort
from ..services.users_service import (
    create_user,
    get_user_by_id,
    EmailAlreadyExistsError,
    UserNotFoundError,
    )

bp = Blueprint("users", __name__)

@bp.post("/")
# @app.post：body 用 Pydantic model（ItemIn）自動驗證 -->FastAPI 不是Flask
def create_user_route():
    data = request.get_json(silent = True) or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        abort(400)
    try:
        user = create_user(username,email,password_hash = password)
    except EmailAlreadyExistsError:
        abort(400)
    
    return {"id":user.id ,"username":user.username ,"email":user.email }, 201

@bp.get("/<int:user_id>")
# @app.get：query 參數直接用函式參數宣告 limit: int = 10
def get_user_route(user_id:int):
    try:
        user = get_user_by_id(user_id)
    except UserNotFoundError:
        abort(404)
    return {"id":user.id ,"username":user.username ,"email":user.email }