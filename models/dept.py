# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  dept.py
@Description    :  部门表
@CreateTime     :  2020/3/8 17:16
------------------------------------
@ModifyTime     :  
"""
from models.BaseModel import BaseModel
from db import db


class Dept(BaseModel):
    """
    部门表
    """
    __tablename__ = "t_dept"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="部门ID")
    parent_id = db.Column(db.Integer, comment="父部门id")
    dept_name = db.Column(db.String(30), comment="部门名称")
    order_num = db.Column(db.Integer, comment="显示顺序")
    leader = db.Column(db.String(20), comment="负责人")
    phone = db.Column(db.String(11), comment="联系电话")
    email = db.Column(db.String(20), comment="邮箱")
    status = db.Column(db.Integer, default=1, comment="部门状态（1正常 2停用）")