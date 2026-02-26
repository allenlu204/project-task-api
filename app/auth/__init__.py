# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 20:52:05 2026

@author: User
"""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/ping")
def ping():
    return {"ok":True}
from . import routes