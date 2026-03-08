# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 21:21:42 2026

@author: User
"""
from flask import render_template,send_from_directory,current_app
from app.docs import docs_bp

@docs_bp.get("/docs")
def swagger_ui():
    return render_template("docs/swagger_ui.html")
    
    
@docs_bp.get("/openapi.yaml")
def openapi_yaml():
    return send_from_directory(current_app.static_folder, "openapi.yaml")
