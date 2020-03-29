# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  role_menu.py
@Description    :  角色菜单关联表
@CreateTime     :  2020/3/8 17:01
------------------------------------
@ModifyTime     :  
"""
from db import db
from models.BaseModel import BaseModel


class Role_Menu(BaseModel):
    """
    角色菜单关联表
    """
    __tablename__ = "t_role_menu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    role_id = db.Column(db.Integer, comment="角色ID")
    menu_id = db.Column(db.Integer, comment="菜单ID")
    create_by = None
    created_at = None
    update_by = None
    updated_at = None
    remark = None
