# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  dict_data.py
@Description    :  字典数据表
@CreateTime     :  2020/3/14 16:34
------------------------------------
@ModifyTime     :  
"""
from models.BaseModel import BaseModel
from db import db


class Dict_Data(BaseModel):
    """
    字典数据表
    """
    __tablename__ = "t_dict_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="id")
    dict_id = db.Column(db.Integer, nullable=False, comment="dict_id")
    dict_sort = db.Column(db.Integer, comment="字典排序")
    dict_label = db.Column(db.String(100), comment="字典标签")
    dict_number = db.Column(db.Integer, comment="字典值")
    dict_value = db.Column(db.String(100), default="", comment="字典键值")
    dict_type = db.Column(db.String(100), comment="字典类型")
    dict_value_type = db.Column(db.Integer, comment="标识")
    css_class = db.Column(db.String(100), comment="样式属性（其他样式扩展）")
    list_class = db.Column(db.String(100), comment="表格回显样式")
    is_default = db.Column(db.Integer, default=1, comment="是否默认（1是 0否）")
    status = db.Column(db.INTEGER, default=1, comment="状态（1正常 2停用）")
