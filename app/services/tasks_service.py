# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 11:17:14 2026

@author: User
"""
from flask import jsonify
from ..extensions import db
from ..models import Task
from .users_service import get_user_by_id
from app.domain.errors import (PermissionDeniedError,
                               UserNotFoundError,
                               EmailAlreadyExistsError,
                               TaskNotFoundError,
                               InvalidTaskPayloadError,
                               InvalidTaskStatusError)

ALLOWED_STATUS = {"todo","doing","done"}
ALLOWED_FIELDS = ["title","description","status"]



def create_task_for_user(actor_user_id:int,owner_id:int,title:str,description:str|None = None,status = "todo"):
    if actor_user_id != owner_id:
        raise PermissionDeniedError()
    get_user_by_id(owner_id)
    
    if not isinstance(title, str) or not title.strip():
        raise InvalidTaskPayloadError("title is required")
    
    if status not in ALLOWED_STATUS:
        raise InvalidTaskStatusError("invalid status")
    
    task = Task(owner_id = owner_id, title = title, description = description, status = status)
    db.session.add(task)
    db.session.commit()
    return task
    # 回傳格式於route決定，service只決定例如商業邏輯任務分層，所以return物件而非run起來不衝突的dict
    # 另外改格式的話這層會直接卡到
    # service不處理是否會做為api回應的問題
    
def list_tasks_for_user(actor_user_id:int,owner_id:int, status:str|None = None):
    if actor_user_id != owner_id:
        raise PermissionDeniedError()
    get_user_by_id(owner_id)
    if status is not None and status not in ALLOWED_STATUS:
        raise InvalidTaskStatusError("invalid status")
    
    stmt = db.select(Task).where(Task.owner_id == owner_id)
    if status is not None:
        stmt = stmt.where(Task.status == status)
    stmt = stmt.order_by(Task.id.desc())
    tasks = db.session.execute(stmt).scalars().all()
    # 先取得一串物件再用all
    return tasks

def get_task_by_id(task_id:int):
    task = db.session.get(Task,task_id)
    if task is None:
        raise TaskNotFoundError("task not found")  
    return task

def get_task_for_actor(*,actor_user_id:int,task_id:int):
    task = get_task_by_id(task_id)
    if task.owner_id != actor_user_id:
        raise PermissionDeniedError()
    return task

def update_task(task:Task,data:dict):
    if not isinstance(data, dict):
        raise InvalidTaskPayloadError()
    updates = {k:v for k,v in data.items() if k in ALLOWED_FIELDS }
    # for k, v in data.items():
    #     if k in ALLOWED_FIELDS:
    #         update[k] = v
    if not updates:
        raise InvalidTaskPayloadError()
    if not isinstance(data,dict):
        raise InvalidTaskPayloadError()
        
    if "title" in updates:
        if updates["title"] is None:
            raise InvalidTaskPayloadError()
        if not isinstance(updates["title"],str):
            raise InvalidTaskPayloadError()
        if updates["title"].strip() == "":
            raise InvalidTaskPayloadError()
    if "status" in updates:
        if updates["status"] is None:
            raise InvalidTaskPayloadError()
        if not isinstance(updates["status"],str):
            raise InvalidTaskPayloadError()
        if updates["status"] not in ALLOWED_STATUS:
            raise InvalidTaskStatusError()

    if "description" in updates:
        if updates["description"] is not None and not isinstance(updates["description"],str):
            raise InvalidTaskPayloadError()
    
    changed = False
    for k,v in updates.items():
        old = getattr(task,k)
        if old != v:
            setattr(task,k,v)
            changed = True
    
        # 將object(task)的k("  ")之屬性(attribute)設定為v，動態更新屬性
        # 但task需屬於物件允許動態新增屬性者(isinstance有slot)，dict list tuple str int內建型別無
        # 若 task 具有 __dict__，可動態新增屬性
        # 若使用 __slots__，只能設定 slots 內定義的屬性
    if changed:
        db.session.commit()
    # 單一資源、單一動作 → commit 在 service（A）
    # 多資源、多步驟、需要原子性 → commit 在 更上層（route / use-case）（B）
    return task

def delete_task(*,actor_user_id:int,task_id:int):
    task = get_task_for_actor(actor_user_id = actor_user_id,task_id = task_id)
    db.session.delete(task)
    db.session.commit()

