# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  __init__.py.py
@Description    :  
@CreateTime     :  2020/2/24 22:07
------------------------------------
@ModifyTime     :  
"""
from flask import Blueprint,  jsonify, request, current_app as app

from conf.config import UPLOAD_HEAD_FOLDER, app_url
from utils.common import *
