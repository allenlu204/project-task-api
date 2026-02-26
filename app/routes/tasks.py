# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 14:29:44 2026

@author: User
"""
from flask import Blueprint,request,abort,jsonify
from app.api.v1.helpers import get_current_user_id,get_task_or_404,require_task_owner
from app.extensions import db
from app.models import Task
from app.services.tasks_service import (
    create_task_for_user,
    list_tasks_for_user,
    get_task_by_id,
    update_task,
    delete_task,
    TaskNotFoundError,
    InvalidTaskPayloadError,
    InvalidTaskStatusError)
from ..services.users_service import UserNotFoundError
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.services.tasks_service import ALLOWED_STATUS

bp = Blueprint("tasks",__name__)

ALLOWED_FIELDS = ["title","description","status"]

@bp.post("/users/<int:user_id>/tasks")
def create_tasks_route(user_id:int):
    data = request.get_json(silent = True) or {}
    title = data.get("title")
    description = data.get("description")
    status = data.get("status","todo")
    if not title:
        abort(400)
    try:
        task = create_task_for_user(owner_id = user_id,title = title,description=description,status = status)
    except UserNotFoundError:
        abort(404)
    except InvalidTaskStatusError:
        abort(400)
    return {
        "id":task.id,
        "owner_id":task.owner_id,
        "title":task.title,
        "description":task.description,
        "status":task.status},201

@bp.get("/users/<int:user_id>/tasks")
def list_task_route(user_id:int):
    status = request.args.get("status")
    # request.arg.get()用在 GET ?a=1&b=2 EX 
    # status = request.args.get("status")          # 單一值
    # tags = request.args.getlist("tag")           # 重複 key：?tag=a&tag=b
    # page = request.args.get("page", type=int)    # 自動轉型（失敗回 None）
    try:
        task = list_tasks_for_user(owner_id = user_id,status = status)
    except UserNotFoundError:
        abort(404)
    except (InvalidTaskPayloadError,InvalidTaskStatusError):
        abort(400)
    return [
        {
        "id":t.id,
        "owner_id":t.owner_id,
        "title":t.title,
        "description":t.description,
        "status":t.status,
        }
        for t in task
    ]
    # 轉換結果 for 迭代變數 in 可迭代物件 -> 每個{}代表一個task物件用list輸出 
@bp.get("/tasks/<int:task_id>")
@jwt_required()
def get_task_route(task_id:int):
    user_id = get_current_user_id()
    task = get_task_or_404(task_id)
    require_task_owner(task,user_id)
    return jsonify(task.to_dict()),200
@bp.patch("/tasks/<int:task_id>")
@jwt_required()
def update_task_route(task_id:int):
    user_id = get_current_user_id()
    task = get_task_or_404(task_id)
    require_task_owner(task,user_id)
    
    data = request.get_json(silent = True)
    if not data or not isinstance(data,dict):
        abort(400,description = "Invalid or empty JSON body")  
    try:
        task = update_task(task,data)
    except InvalidTaskPayloadError:
        abort(400, description="Invalid task payload")
    except InvalidTaskStatusError:
        abort(400, description="Invalid task Status")
    return jsonify(task.to_dict()),200
@bp.delete("/tasks/<int:task_id>")
def delete_task_route(task_id:int):
    
    try:
        delete_task(task_id)
    except TaskNotFoundError:
        abort(404)
    return "",204
        