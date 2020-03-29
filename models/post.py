# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  post.py
@Description    :  岗位信息表
@CreateTime     :  2020/3/8 17:23
------------------------------------
@ModifyTime     :  
"""
from models.BaseModel import BaseModel
from db import db


class Post(BaseModel):
    """
    菜单权限表
    """
    __tablename__ = "t_post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="岗位ID")
    post_code = db.Column(db.String(50), comment="岗位编码")
    post_name = db.Column(db.String(50), comment="岗位名称")
    post_sort = db.Column(db.Integer, comment="显示顺序")
    status = db.Column(db.Integer, default=1, comment="状态（1正常 2停用）")
