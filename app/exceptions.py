# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:32:19 2026

@author: User
"""
from __future__ import annotations
# 版本過渡機制，在舊版本 Python 提前使用新語法特性
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class AppError(Exception):
    status_code: int
    error_type: str
    message: str
    details: Optional[Any] = None
    
    def __str__(self):
        return self.message

class BadRequestError(AppError):
    def __init__(self, message:str = "bad request",details:Any = None):
        # 正確的參數語法 參數名: 型別 = 預設值 None為值型別是Nonetype
        super().__init__(400,"bad_request",message,details)
class UnauthorizedError(AppError):
    def __init__(self, message:str = "unauthorized",details:Any = None):
        # 正確的參數語法 參數名: 型別 = 預設值 None為值型別是Nonetype
        super().__init__(401,"unauthorized",message,details)
class ForbiddenError(AppError):
    def __init__(self, message:str = "forbidden",details:Any = None):
        # 正確的參數語法 參數名: 型別 = 預設值 None為值型別是Nonetype
        super().__init__(403,"forbidden",message,details)
class NotFoundError(AppError):
    def __init__(self, message:str = "not found",details:Any = None):
        # 正確的參數語法 參數名: 型別 = 預設值 None為值型別是Nonetype
        super().__init__(404,"not_found",message,details)
class ConflictError(AppError):
    def __init__(self, message:str = "conflict",details:Any = None):
        # 正確的參數語法 參數名: 型別 = 預設值 None為值型別是Nonetype
        super().__init__(409,"conflict",message,details)
        