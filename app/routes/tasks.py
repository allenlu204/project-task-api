# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 14:29:44 2026

@author: User
"""
from flask import Blueprint,request,jsonify
from app.api.v1.helpers import get_current_user_id
from app.services.tasks_service import (
    create_task_for_user,
    list_tasks_for_user,
    get_task_by_id,
    get_task_for_actor,
    update_task,
    delete_task)
from flask_jwt_extended import jwt_required
from app.error_mapping import handle_domain_errors
from app.exceptions import BadRequestError

bp = Blueprint("tasks",__name__)

ALLOWED_FIELDS = ["title","description","status"]

@bp.post("/users/<int:user_id>/tasks")
@jwt_required()
@handle_domain_errors
def create_tasks_route(user_id:int):
    actor_user_id = get_current_user_id()
    data = request.get_json(silent = True)
    if not isinstance(data,dict):
        raise BadRequestError("invalid request")
        
    title = data.get("title")
    description = data.get("description")
    status = data.get("status","todo")
    
    if not title or not isinstance(title, str) or not title.strip():
        raise BadRequestError("invalid request")
    task = create_task_for_user(
            actor_user_id = actor_user_id,
            owner_id = user_id,
            title = title,
            description=description,
            status = status)
   
    return {
        "id":task.id,
        "owner_id":task.owner_id,
        "title":task.title,
        "description":task.description,
        "status":task.status},201

@bp.get("/users/<int:user_id>/tasks")
@jwt_required()
@handle_domain_errors
def list_task_route(user_id:int):
    actor_user_id = get_current_user_id()
    status = request.args.get("status")
    # request.arg.get()用在 GET ?a=1&b=2 EX 
    # status = request.args.get("status")          # 單一值
    # tags = request.args.getlist("tag")           # 重複 key：?tag=a&tag=b
    # page = request.args.get("page", type=int)    # 自動轉型（失敗回 None）
    tasks = list_tasks_for_user(actor_user_id = actor_user_id,owner_id = user_id,status = status)
    return [
        {
        "id":t.id,
        "owner_id":t.owner_id,
        "title":t.title,
        "description":t.description,
        "status":t.status,
        }
        for t in tasks
    ],200
    # 轉換結果 for 迭代變數 in 可迭代物件 -> 每個{}代表一個task物件用list輸出 
@bp.get("/tasks/<int:task_id>")
@jwt_required()
@handle_domain_errors
def get_task_route(task_id:int):
    actor_user_id = get_current_user_id()
    task = get_task_for_actor(actor_user_id = actor_user_id,task_id = task_id)
    return jsonify(task.to_dict()),200
@bp.patch("/tasks/<int:task_id>")
@jwt_required()
@handle_domain_errors
def update_task_route(task_id:int):
    actor_user_id = get_current_user_id()
    
    data = request.get_json(silent = True)
    if not data or not isinstance(data,dict):
        raise BadRequestError("invalid request")
    
    task = get_task_for_actor(actor_user_id = actor_user_id,task_id = task_id)
    task = update_task(task,data) 
    return jsonify(task.to_dict()),200
@bp.delete("/tasks/<int:task_id>")
@jwt_required()
@handle_domain_errors
def delete_task_route(task_id:int):
    actor_user_id = get_current_user_id()
    _ = get_task_for_actor(actor_user_id = actor_user_id,task_id = task_id)
    delete_task(actor_user_id = actor_user_id,task_id = task_id)
    return "",204
        