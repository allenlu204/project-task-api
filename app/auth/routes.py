# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 10:19:48 2026

@author: User
"""
from . import auth_bp
from flask import request
from ..services.users_service import get_user_by_email
from app.domain.errors import UserNotFoundError
from flask_jwt_extended import create_access_token
from app.exceptions import BadRequestError,UnauthorizedError
@auth_bp.post("/login")
def login_route():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not isinstance(email,str) or not email.strip():
        raise BadRequestError("invalid request")
    if not password or not isinstance(password,str) or not password.strip():
        raise BadRequestError("invalid request")
    try:
        user = get_user_by_email(email)
    except UserNotFoundError:
        raise UnauthorizedError("unauthorized")
    if not user.check_password(password):
        raise UnauthorizedError("unauthorized")
    token = create_access_token(identity = str(user.id))
    return {"access_token":token,"user_id":user.id},200
    
    
