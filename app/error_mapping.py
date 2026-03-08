# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:47:39 2026

@author: User
"""

from __future__ import annotations
from typing import Callable,TypeVar,Any,cast
from functools import wraps
from app.domain.errors import (DomainError,
                               UserNotFoundError,
                               PermissionDeniedError,
                               EmailAlreadyExistsError,
                               TaskNotFoundError,
                               InvalidTaskPayloadError,
                               InvalidTaskStatusError)
from app.exceptions import (AppError,
                            BadRequestError,
                            UnauthorizedError,
                            ForbiddenError,
                            NotFoundError,
                            ConflictError)
F = TypeVar("F",bound = Callable[...,Any])
# TypeVar泛型型別變數，建立F之任意函式型別，限制須為callable  Any使任意參數任意回傳
def map_domain_error(e:DomainError):
    if isinstance(e, UserNotFoundError):
        return UnauthorizedError("unauthorizedError")
    
    if isinstance(e, PermissionDeniedError):
        return ForbiddenError("forbidden")
    
    if isinstance(e, EmailAlreadyExistsError):
        return BadRequestError("invalid request")
    
    if isinstance(e, TaskNotFoundError):
        return NotFoundError("not found")
    
    if isinstance(e, (InvalidTaskPayloadError,InvalidTaskStatusError)):
        return BadRequestError("invalid request")
    
    return BadRequestError("invalid request")

def handle_domain_errors(fn:F):
    # fn為原本要執行的函式，F限制為輸出callable物件，因此這個函式作用為輸入函式並輸出函式
    @wraps(fn)
    # 把fn的metadata複製到wrapper上
    # wrapper.__init__ 會顯示原本函式名 wrapper.__doc__會保留原函式之docstring
    def wrapper(*args:Any,**kwargs:Any):
        # *args 枚舉位置參數(positional argument)成為tuple **kwargs 枚舉關鍵字參數(keyword argument)成為dict
        # 簡寫
        # *：位置參數的收集/解；也可用來宣告 keyword-only 分界強制「後面只能用關鍵字傳參」（keyword-only）
        # **：關鍵字參數的收集/解；也可用來合併 dict
        try:
            return fn(*args,**kwargs)
        except DomainError as e:
            raise map_domain_error(e)
    return cast(F, wrapper)
        # cast為型別認定，影響 type checker，runtime不變
            
        

        
        
        
        
        
        
        
    