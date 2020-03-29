# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  code_enum.py
@Description    :  返回码枚举类
@CreateTime     :  2020/3/7 19:48
------------------------------------
@ModifyTime     :  
"""

import enum


class Code(enum.Enum):
    # 成功
    SUCCESS = 0
    # 获取信息失败
    REQUEST_ERROR = 400
    # 504错误
    NOT_FOUND = 404
    # 500错误
    INTERNAL_ERROR = 500
    # 登录超时
    LOGIN_TIMEOUT = 50014
    # 无效token
    ERROR_TOKEN = 50008
    # 别的客户端登录
    OTHER_LOGIN = 50012
    # 权限不够
    ERR_PERMISSOM = 50013
    # 更新数据库失败
    UPDATE_DB_ERROR = 1000
    # 更新数据库失败
    CREATE_DB_ERROR = 1001
    # 更新数据库失败
    DELETE_DB_ERROR = 1002
    # 不能为空
    NOT_NULL = 1003
    # 缺少参数
    NO_PARAMETER = 1004
    # 用户密码错误
    ERR_PWD = 1005

    # 数据不存在
    ID_NOT_FOUND = 1006
    # 参数错误
    PARAMETER_ERROR = 1007
    # 文件不存在
    FILE_NO_FOUND = 1008
    # 无效的格式
    ERROR_FILE_TYPE = 1009
    # 超出文件限制
    OVER_SIZE = 1010
    # 上传失败
    UPLOAD_FAILD = 1011
