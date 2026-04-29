# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:53:30 2026

@author: User
"""

import os
import re
import uuid

import requests
from playwright.sync_api import expect, sync_playwright

BASE_URL = os.getenv("E2E_BASE_URL", "http://127.0.0.1:5000")

def create_test_user():
    unique = uuid.uuid4().hex[:8]
    payload = {
        "username": f"e2euser_{unique}",
        "email": f"e2e_{unique}@example.com",
        "password": "test1234",
        }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/users/",
        json = payload,
        timeout = 10,
        )
    
    assert response.status_code == 201, response.text
    return payload

def test_login_and_create_task_happy_path():
    user = create_test_user()
    task_title = f"E2E Task {uuid.uuid4().hex[:6]}"
    
    headless = os.getenv("HEADLESS", "1") != "0"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = headless)
        page = browser.new_page()
        
        page.goto(f"{BASE_URL}/login")
        
        page.fill("#login-email",user["email"])
        page.fill("#login-password",user["password"])
        page.click("#login-submit")
        
        page.wait_for_url(re.compile(r".*/tasks$"))
        expect(page).to_have_url(re.compile(r".*/tasks$"))
        expect(page.locator("body")).to_contain_text("我的任務列表")
        
        page.fill("#task-title-input",task_title)
        page.select_option("#task-status-select","todo")
        page.click("#task-create-button")
        
        expect(page.locator("#task-table-body")).to_contain_text(task_title)
        
        browser.close()
        