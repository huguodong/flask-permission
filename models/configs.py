# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  configs.py
@Description    :  参数表
@CreateTime     :  2020/3/22 14:31
------------------------------------
@ModifyTime     :  
"""
from models.BaseModel import BaseModel
from db import db


class Configs(BaseModel):
    """
    参数表
    """
    __tablename__ = "t_configs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="参数ID")
    config_name = db.Column(db.String(100), comment="参数名称")
    config_type = db.Column(db.String(100), comment="系统内置（1是 2否")
    config_key = db.Column(db.String(100), comment="参数键名")
    config_value = db.Column(db.Integer, default=1, comment="标识")
