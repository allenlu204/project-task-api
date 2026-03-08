# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:39:50 2026

@author: User
"""

class DomainError(Exception):
    pass

class PermissionDeniedError(DomainError):
    pass

class UserNotFoundError(DomainError):
    pass

class EmailAlreadyExistsError(DomainError):
    pass

class TaskNotFoundError(DomainError):
    pass

class InvalidTaskPayloadError(DomainError):
    pass

class InvalidTaskStatusError(DomainError):
    pass

