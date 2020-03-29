# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  dict_data.py
@Description    :  字典类型表
@CreateTime     :  2020/3/14 16:34
------------------------------------
@ModifyTime     :  
"""
from models.BaseModel import BaseModel
from db import db


class Dict_Type(BaseModel):
    """
    字典类型表
    """
    __tablename__ = "t_dict_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    dict_name = db.Column(db.String(100), comment="字典名称")
    dict_type = db.Column(db.String(100), index=True, comment="字典类型")
    dict_value_type = db.Column(db.Integer, comment="标识")
    status = db.Column(db.Integer, default=1, comment="状态（1正常 2停用）")
