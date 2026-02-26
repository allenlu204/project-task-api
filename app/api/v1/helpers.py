# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 11:20:50 2026

@author: User
"""

from app.extensions import db
from app.models import Task
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select
from flask import abort

def get_current_user_id():
    return int(get_jwt_identity())

def get_task_or_404(task_id:int):
    stmt = select(Task).where(Task.id == task_id)
    task = db.session.execute(stmt).scalar_one_or_none()
    if task is None:
        abort(404)
    return task

def require_task_owner(task,user_id:int):
    if task.owner_id != user_id:
        abort(403)
    