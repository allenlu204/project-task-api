# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 11:38:03 2026

@author: User
"""
import os
import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture(scope = "function")
def app():
    test_db_url = os.getenv("TEST_DATABASE_URL")
    if not test_db_url:
        raise RuntimeError("TEST_DATABASE_URL not set. Refusing to run tests to avoid dropping dev DB.")
    # 如果未設定"TEST_DATABASE_URL"測試就會直接crash，避免drop到dev db
    app = create_app({
        "TESTING":True,
        "SQLALCHEMY_DATABASE_URI":test_db_url
    })
    return app

@pytest.fixture(scope = "function")
def client(app):
    return app.test_client()

@pytest.fixture(scope = "function",autouse = True)    
#autouse = True-> 每個 test 自動執行，不用手動傳參數。
def reset_db(app):
    with app.app_context():
# pytest 看到參數名稱 app：
# → 會去找一個叫 app 的 fixture
# → 先執行 app fixture
# → 把結果傳進來
# dependency injection。        
        db.drop_all()
        db.create_all()
# fixture 只是為了執行 setup / teardown，不需要提供物件給 test。
# 有些 fixture 需要 return（例如 client）
# 有些 fixture 只做副作用（例如 reset_db）
    yield
# yield這是 fixture 的分界線。
# before yield  -> setup
# after yield   -> teardown
# 這段沒有 teardown。
# 意思是:setup：drop + create
# 測試開始/測試結束/沒有後處理
# 因為下一個 test 又會 drop + create。
@pytest.fixture
def create_user(app):
    def _create_user(username:str,email:str,password:str):
        with app.app_context():
            user = User(
                username = username,
                email = email,
                password_hash = password)
            db.session.add(user)
            db.session.commit()
            return user.id
    return _create_user
@pytest.fixture(scope = "function")
def login_token(client,create_user):
    def _login_token(username:str,email:str,password:str):
        user_id = create_user(username=username,email=email,password=password)
        resp = client.post("/api/v1/auth/login",json = {"email":email,"password":password})
        assert resp.status_code == 200
        token = resp.get_json()["access_token"]
        headers = { "Authorization" : f"Bearer {token}" }
        return headers,user_id
    return _login_token
        