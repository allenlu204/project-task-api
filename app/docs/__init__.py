# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 21:21:42 2026

@author: User
"""

from flask import Blueprint


docs_bp = Blueprint("docs", __name__)
from app.docs import routes 
# flask的decorartor import時執行