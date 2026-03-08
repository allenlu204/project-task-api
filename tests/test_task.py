# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:09:49 2026

@author: User
"""

def test_create_task_ok(client,login_token):
    headers,user_id = login_token("John","John@example.com","123456")
    
    task_payload = {
        "title":"test task",
        "description":"~",
        "status":"todo"}
    
    resp = client.post(f"/api/v1/users/{user_id}/tasks",json = task_payload,headers = headers)
    
    assert resp.status_code == 201
    
    data = resp.get_json()
    
    assert data["title"] == "test task"
    assert data["status"] == "todo"
    assert data["owner_id"] == user_id
    
def test_create_task_forbidden_when_user_not_me(client,login_token):
    headers,user_id = login_token("John","John@example.com","123456")
    task_payload = {
        "title":"test task",
        "description":"~",
        "status":"todo"}
    resp = client.post("/api/v1/users/999/tasks",json = task_payload,headers = headers)
    assert resp.status_code == 403
    assert resp.is_json
    err = resp.get_json()["error"]
    assert err["code"] == 403
    assert err["type"] == "forbidden"
    
def test_create_task_invalid_status(client,login_token):
    headers,user_id = login_token("John","John@example.com","123456")
    task_payload = {
        "title":"test task",
        "description":"~",
        "status":"not yet"}
    resp = client.post(f"/api/v1/users/{user_id}/tasks",json = task_payload,headers = headers)
    assert resp.status_code == 400
    
def test_create_task_no_token(client,create_user):
    user_id = create_user("John","John@example.com","123456")
    task_payload = {
        "title":"test task"}
    resp = client.post(f"/api/v1/users/{user_id}/tasks",json = task_payload)
    assert resp.status_code == 401
    assert resp.is_json
    err = resp.get_json()["error"]
    assert err["code"] == 401
    assert err["type"] == "unauthorized"
    assert isinstance(err.get("message"),str) and err["message"].strip()  

def test_list_tasks_required_auth(client,create_user):
    user_id = create_user("John","John@example.com","123456")
    resp = client.get(f"/api/v1/users/{user_id}/tasks")
    assert resp.status_code == 401
    
def test_list_task_ok(client,login_token):
    headers,user_id = login_token("John","John@example.com","123456")
    task_payload = {
        "title":"test task",
        "description":"~",
        "status":"todo"}
    resp = client.post(f"/api/v1/users/{user_id}/tasks",json = task_payload,headers = headers)
    assert resp.status_code == 201
    resp = client.get(f"/api/v1/users/{user_id}/tasks",headers = headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data,list)
    assert len(data) == 1
    assert data[0]["title"] == "test task"

def test_delete_task_no_auth(client,login_token):
    headers,user_id = login_token("John","John@example.com","123456")
    resp = client.get(f"/api/v1/users/{user_id}/tasks")
    assert resp.status_code == 401
    # current_user_id = get_current_user_id()
    # if current_user_id != user_id:
    #     abort(403)
    
    