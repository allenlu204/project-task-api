# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 06:38:47 2026

@author: User
"""
from ..extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password_hash = db.Column(db.String(255),nullable = False)
    is_active = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    tasks = db.relationship("Task",back_populates = "owner",passive_deletes = True)
    