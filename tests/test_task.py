# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:09:49 2026

@author: User
"""
from flask import abort
def test_create_task_ok(client):
    user_payload = {
        "username":"John",
        "email":"John@example.com",
        "password":"123456"}
    response = client.post("/api/v1/users/",json = user_payload)
    
    assert response.status_code == 201
    
    data = response.get_json()
    user_id = data["id"]
    
    task_payload = {
        "title":"test task",
        "description":"~",
        "status":"todo"}
    
    response = client.post(f"/api/v1/users/{user_id}/tasks",json = task_payload)
    
    assert response.status_code == 201
    
    data = response.get_json()
    
    assert data["title"] == "test task"
    assert data["status"] == "todo"
    
def test_create_task_user_not_found(client):
    
    task_payload = {
        "title":"test task",
        "description":"~",
        "status":"todo"}
    response = client.post("/api/v1/users/999/tasks",json = task_payload)
    assert response.status_code == 404
    
def test_create_task_invalid_status(client):
    user_payload = {
        "username":"John",
        "email":"John@example.com",
        "password":"123456"}
    response = client.post("/api/v1/users/",json = user_payload)
    
    assert response.status_code == 201
    
    data = response.get_json()
    user_id = data["id"]
    
    task_payload = {
        "title":"test task",
        "description":"~",
        "status":"not yet"}
    response = client.post(f"/api/v1/users/{user_id}/tasks",json = task_payload)
    
    assert response.status_code == 400
    