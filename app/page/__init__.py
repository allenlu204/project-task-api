# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:42:17 2026

@author: User
"""

from flask import Blueprint

page_bp = Blueprint("page",__name__)

from app.page import routes