# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:45:45 2026

@author: User
"""
from app.page import page_bp
from flask import url_for, redirect, render_template

@page_bp.route("/")
def home():
    return redirect(url_for("page.login"))
    
@page_bp.route("/login")
def login():
    return render_template("login.html")
    
@page_bp.route("/tasks")
def tasks():
    return render_template("tasks.html")