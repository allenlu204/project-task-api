# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 16:09:49 2026

@author: User
"""

# pytest 的 fixture 不能手動 import。
# fixture 是：
# 由 pytest 自動注入
# 透過參數名稱取得
def make_user_payload(username="John", email="John@example.com", password="123456"):
    payload = {
    "username" : username,
    "email" : email,
    "password" : password
    }
    return payload

def test_create_user_ok(client):
    payload = make_user_payload()
# pytest 看到 client→ 去找 fixture→ 自動傳進來
    response = client.post("/api/v1/users/",json = payload)
    # json = payload它會自動：dumps設 content_type
    
    assert response.status_code == 201
    
    data = response.get_json()
    
    assert data["username"] == "John"
    assert data["email"] == "John@example.com"
    assert "id" in data
def test_get_user_not_found(client):
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    # assert 是「開發期檢查條件是否成立的工具」。
    # 條件為 False → 丟出 AssertionError。
    # assert condition
    # assert condition, "error message"
    # 等於
    # if not condition:
    # raise AssertionError("error message")
    # 在 pytest 裡，assert 是核心語法。
    # pytest 會自動幫你做 diff 顯示。
def test_create_user_missing_field_400(client):
    payload = {
        "username" : "John",
        "email" : "John@example.com",
        }
    response = client.post("/api/v1/users/",json = payload)
    assert response.status_code == 400
def test_create_user_duplicate_email_400(client):
    payload = make_user_payload()
# pytest 看到 client→ 去找 fixture→ 自動傳進來
    response = client.post("/api/v1/users/",json = payload)
    # json = payload它會自動：dumps設 content_type
    
    assert response.status_code == 201
    
    payload = {
        "username" : "Alice",
        "email" : "John@example.com",
        "password" : "2345678"
        }
# pytest 看到 client→ 去找 fixture→ 自動傳進來
    response = client.post("/api/v1/users/",json = payload)
    # json = payload它會自動：dumps設 content_type
    
    assert response.status_code == 400
    
    
    