# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  menu.py
@Description    :  菜单表
@CreateTime     :  2020/3/8 16:29
------------------------------------
@ModifyTime     :  
"""
from models.BaseModel import BaseModel
from db import db


class Menu(BaseModel):
    """
    菜单权限表
    """
    __tablename__ = "t_menu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="菜单ID")
    menu_name = db.Column(db.String(50), comment="菜单名称")
    parent_id = db.Column(db.Integer, comment="父菜单ID")
    order_num = db.Column(db.Integer, comment="显示顺序")
    url = db.Column(db.String(200), comment="请求地址")
    menu_type = db.Column(db.Integer, default=1, comment="菜单类型（1,目录 2,菜单 3,按钮")
    visible = db.Column(db.Integer, default=1, comment="菜单状态（1显示 2隐藏）")
    perms = db.Column(db.String(100), comment="权限标识")
    icon = db.Column(db.String(100), comment="菜单图标")
    is_frame = db.Column(db.Integer, default=2, comment="是否外链")
    route_name = db.Column(db.String(100), default="", comment="路由名称")
    route_path = db.Column(db.String(100), default="", comment="路由地址")
    route_cache = db.Column(db.Integer, default=0, comment="路由缓存")
    route_component = db.Column(db.String(100), default="", comment="路由组件")
