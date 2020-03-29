# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  role_dept.py
@Description    :  角色和部门关联表
@CreateTime     :  2020/3/8 17:25
------------------------------------
@ModifyTime     :  
"""
from db import db
from models.BaseModel import BaseModel


class Role_Dept(BaseModel):
    """
    角色和部门关联表
    """
    __tablename__ = "t_role_dept"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    role_id = db.Column(db.Integer, comment="角色ID")
    dept_id = db.Column(db.Integer, comment="部门ID")
    create_by = None
    created_at = None
    update_by = None
    updated_at = None
    remark = None
