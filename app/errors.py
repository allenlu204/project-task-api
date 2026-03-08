# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:26:15 2026

@author: User
"""

from exceptions import NotFoundError

e = NotFoundError("User not found")
print(e)          # 看 __str__
print(repr(e))    # 看 __repr__
print(e.__dict__) # 看欄位