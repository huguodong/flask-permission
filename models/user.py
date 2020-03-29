# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  user.py
@Description    :  用户表
@CreateTime     :  2020/3/7 14:45
------------------------------------
@ModifyTime     :  
"""
import hashlib

from sqlalchemy import func

from db import db
from models.BaseModel import BaseModel


class User(BaseModel):
    """
    用户表
    """
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="用户ID")
    nickname = db.Column(db.String(30), comment="用户昵称")
    user_name = db.Column(db.String(30), comment="登录账号")
    user_type = db.Column(db.Boolean, default=1, comment="用户类型（1系统用户")
    email = db.Column(db.String(50), comment="用户邮箱")
    phone = db.Column(db.String(20), comment="手机号")
    phonenumber = db.Column(db.String(11), comment="手机号码")
    sex = db.Column(db.INTEGER, default=1, comment="用户性别（1男 2女 3未知）")
    avatar = db.Column(db.String(100), comment="头像路径")
    password = db.Column(db.String(50), comment="密码")
    salt = db.Column(db.String(20), comment="盐加密")
    status = db.Column(db.INTEGER, default=1, comment="帐号状态（1正常 2禁用")
    dept_id = db.Column(db.INTEGER, comment="部门id")
    del_flag = db.Column(db.INTEGER, default=1, comment="删除标志（1代表存在 2代表删除）")
    login_ip = db.Column(db.String(50), comment="最后登陆IP")
    login_date = db.Column(db.TIMESTAMP, comment="最后登陆时间", nullable=False,
                           onupdate=func.now())

    def check_password(self, passwd):
        '''
        检查密码
        :param passwd:
        :return: 0/1
        '''
        # 创建md5对象
        m = hashlib.md5()
        b = passwd.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        if self.password == str_md5:
            return 1
        else:
            return 0
