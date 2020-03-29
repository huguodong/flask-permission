# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  config.py
@Description    :  
@CreateTime     :  2020/3/7 14:36
------------------------------------
@ModifyTime     :  
"""
# 日志
LOG_LEVEL = "DEBUG"
LOG_DIR_NAME = "logs"

# mysql
MYSQL = {"HOST": "192.168.68.133",
         'PORT': "3306",
         'USER': "root",
         'PASSWD': "root",
         'DB': "devops"}

REDIS = {
    'HOST': '192.168.68.133',
    'PORT': 6379,
    'PASSWD': '',
    'DB': 0,
    "EXPIRE": 60000
}

# token
SECRET_KEY = "jinwandalaohu"
EXPIRES_IN = 9999

# 上传文件
UPLOAD_HEAD_FOLDER = "static/uploads/avatar"
app_url = "http://localhost:5000"
