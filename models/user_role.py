# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  user_role.py
@Description    :  
@CreateTime     :  2020/3/8 17:01
------------------------------------
@ModifyTime     :  
"""
from db import db
from models.BaseModel import BaseModel


class User_Role(BaseModel):
    """
    用户角色关联表
    """
    __tablename__ = "t_user_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = db.Column(db.Integer, comment="用户ID")
    role_id = db.Column(db.Integer, comment="角色ID")
    create_by = None
    created_at = None
    update_by = None
    updated_at = None
    remark = None
