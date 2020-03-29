# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  user_post.py
@Description    :  
@CreateTime     :  2020/3/8 17:29
------------------------------------
@ModifyTime     :  
"""
from db import db
from models.BaseModel import BaseModel


class User_Post(BaseModel):
    """
    用户与岗位关联表
    """
    __tablename__ = "t_user_post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = db.Column(db.Integer, comment="用户ID")
    post_id = db.Column(db.Integer, comment="岗位ID")
    create_by = None
    created_at = None
    update_by = None
    updated_at = None
    remark = None

