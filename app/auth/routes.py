# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 10:19:48 2026

@author: User
"""
from . import auth_bp
from flask import request,abort
from ..services.users_service import get_user_by_email,UserNotFoundError
from flask_jwt_extended import create_access_token
@auth_bp.post("/login")
def login_route():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email:
        abort(400)
    if not password:
        abort(400)
    try:
        user = get_user_by_email(email)
    except UserNotFoundError:
        abort(404)
    if user.password_hash != password:
        abort(401)
    token = create_access_token(identity = str(user.id))
    return {"access_token":token},200
    
    
