# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  role.py
@Description    :  角色信息表
@CreateTime     :  2020/3/8 17:00
------------------------------------
@ModifyTime     :  
"""
from db import db
from models.BaseModel import BaseModel


class Role(BaseModel):
    """
    角色信息表
    """
    __tablename__ = "t_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="角色ID")
    role_name = db.Column(db.String(30), comment="角色名称")
    role_key = db.Column(db.String(100), comment="角色权限字符串")
    role_sort = db.Column(db.Integer, comment="显示顺序")
    data_scope = db.Column(db.CHAR(1), default=1, comment="数据范围（1：全部数据权限 2：自定数据权限）")
    status = db.Column(db.CHAR(1), default=1, comment="角色状态（1正常 2停用）")

