# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 06:38:48 2026

@author: User
"""

from ..extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer,primary_key = True)
    owner_id = db.Column(
        db.Integer, 
        db.ForeignKey("users.id", ondelete = "RESTRICT" ),
        nullable = False,
        index = True,
        )
    
    
    title = db.Column(db.String(200),nullable = False)
    description = db.Column(db.Text, nullable = True)
    status = db.Column(db.String(20), nullable = False, default = "todo", index = True)
    created_at = db.Column(db.DateTime,nullable = False, default = datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow,
        onupdate = datetime.utcnow)
    owner = db.relationship("User",back_populates = "tasks")
    # db.relationship用法不確定，需確認
    def to_dict(self):
        return {
            "id":self.id,
            "owner_id":self.owner_id,
            "title":self.title,
            "description":self.description,
            "status":self.status,}