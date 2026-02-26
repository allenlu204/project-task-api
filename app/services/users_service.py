# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 11:17:14 2026

@author: User
"""

from ..extensions import db
from ..models import User
from sqlalchemy.exc import NoResultFound
class EmailAlreadyExistsError(ValueError):
    pass
    
class UserNotFoundError(ValueError):
    pass

def create_user(username:str, email:str, password_hash:str):
    existing = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()
    
    if existing:
        raise EmailAlreadyExistsError("email exists")
    
    user = User(username = username, email = email, password_hash = password_hash)
    db.session.add(user)
    db.session.commit()
    return user
    # 回傳格式於route決定，service只決定例如商業邏輯任務分層，所以return物件而非run起來不衝突的dict
    # 另外改格式的話這層會直接卡到
    # service不處理是否會做為api回應的問題
def get_user_by_id(user_id:int):
    user = db.session.get(User,user_id)
    if user is None:
        raise UserNotFoundError("user not found")
    return user
def get_user_by_email(email:str):
    stmt = db.select(User).where(User.email == email)
    try:
        user = db.session.execute(stmt).scalar_one()
    except NoResultFound:
        raise UserNotFoundError("user not found")
    # 回應格式（HTTP狀態碼）這是 route 的責任。
    # 商業錯誤語意（Domain Error）這是 service 的責任。
    # .scalar_one() 丟的是sqlalchemy.exc.NoResultFound這是 ORM 層的技術例外(SQLAlchemy 內部例外)。
    
    return user


