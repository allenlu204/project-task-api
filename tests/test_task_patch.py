# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 19:12:47 2026

@author: User
"""
# from tests import conftest
from sqlalchemy import select
from app.extensions import db
from app.models import Task

def test_patch_owner_ok(client,login_token):
    headers,user_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{user_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    # with app.app_context():
    #     stmt = select(Task).where(Task.id == task_id)
    #     task = db.session.execute(stmt).scalar_one()
    #     assert task.status_code == 200
    #     assert task.title == "new"
    task_id = resp.get_json()["id"]
    task_patch = client.patch(f"/api/v1/tasks/{task_id}",
                             json = {"title":"new"},
                             headers = headers)
    assert task_patch.status_code == 200
    data = task_patch.get_json()
    assert data["title"] == "new"
    
def test_patch_non_owner_403(client,login_token,app):
    owner_headers,owner_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{owner_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]
    with app.app_context():
        stmt = select(Task).where(Task.id == task_id)
        task_before = db.session.execute(stmt).scalar_one()
        original_updated_at = task_before.updated_at
    other_headers,other_user_id = login_token(
        username = "Other",
        email = "Other@example.com",
        password = "123456")
    resp_patch = client.patch(f"/api/v1/tasks/{task_id}",
                             json = {"title":"hacked"},
                             headers = other_headers)
    assert resp_patch.status_code == 403
    with app.app_context():
        stmt = select(Task).where(Task.id == task_id)
        task_after = db.session.execute(stmt).scalar_one()
        after_updated_at = task_after.updated_at
        assert after_updated_at == original_updated_at
def test_patch_no_token_401(client,login_token):
    owner_headers,owner_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{owner_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]
    task_patch = client.patch(f"/api/v1/tasks/{task_id}",
                             json = {"title":"new"},
                             )
    assert task_patch.status_code == 401
def test_patch_no_json_400(client,login_token):
    headers,user_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{user_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]
    task_patch = client.patch(f"/api/v1/tasks/{task_id}",
                             json = {},
                             headers = headers)
    assert task_patch.status_code == 400
def test_patch_invalid_json_400(client,login_token):
    headers,user_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{user_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]
    task_patch = client.patch(f"/api/v1/tasks/{task_id}",
                              data = "{title",
                              content_type = "application/json",
                             headers = headers)
    assert task_patch.status_code == 400
def test_patch_invalid_status_400(client,login_token):
    headers,user_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{user_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]
    task_patch = client.patch(f"/api/v1/tasks/{task_id}",
                             json = {"title":"new",
                                     "status":"mad"},
                             headers = headers)
    assert task_patch.status_code == 400
def test_patch_title_null_400(client,login_token,app):
    headers,user_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{user_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]
    task_patch = client.patch(f"/api/v1/tasks/{task_id}",
                             json = {"title":None},
                             headers = headers)
    assert task_patch.status_code == 400
    with app.app_context():
        stmt = select(Task).where(Task.id == task_id)
        task = db.session.execute(stmt).scalar_one()
        assert task.title == "old"
    
def test_patch_status_null_400(client,login_token,app):
    headers,user_id = login_token(
        username = "John",
        email = "John@example.com",
        password = "123456")
    resp = client.post(f"/api/v1/users/{user_id}/tasks",
                       json = {"title":"old",
                               "description":"N",
                               "status":"todo"})
    assert resp.status_code == 201
    task_id = resp.get_json()["id"]
    task_patch = client.patch(f"/api/v1/tasks/{task_id}",
                             json = {"title":"old",
                                     "status":None},
                             headers = headers)
    assert task_patch.status_code == 400
    with app.app_context():
        stmt = select(Task).where(Task.id == task_id)
        task = db.session.execute(stmt).scalar_one()
        assert task.status == "todo"
    
    
    