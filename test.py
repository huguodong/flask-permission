# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  test.py
@Description    :  
@CreateTime     :  2020/3/12 21:41
------------------------------------
@ModifyTime     :  
"""
import hashlib
import os
import random
import time
from datetime import datetime

def create_passwd(passwd):
    # 创建md5对象
    m = hashlib.md5()
    b = passwd.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5

print(create_passwd("admins"))