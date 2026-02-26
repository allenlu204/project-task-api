# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:53:29 2026

@author: User
"""
from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api/v1")

from .users import bp as users_bp
from .tasks import bp as tasks_bp

api.register_blueprint(users_bp,url_prefix = "/users")
api.register_blueprint(tasks_bp)
# route 裡寫完整路徑的寫法

# 另可 route 裡只寫資源本體
# @bp.post("/users/<int:user_id>/tasks")
# @bp.get("/users/<int:user_id>/tasks")
# @bp.get("/<int:task_id>")
# @bp.patch("/<int:task_id>")
# @bp.delete("/<int:task_id>")
# api.register_blueprint(tasks_bp, url_prefix="/tasks")
    