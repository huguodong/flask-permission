# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  log_conf.py
@Description    :  log配置，实现日志自动按日期生成日志文件
@CreateTime     :  2020/3/7 19:17
------------------------------------
@ModifyTime     :  
"""

import os
import time
import logging
from conf import config


def make_dir(make_dir_path):
    """
    文件生成
    :param make_dir_path:
    :return:
    """
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    return path


log_dir_name = config.LOG_DIR_NAME  # 日志文件夹
log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'  # 文件名
log_file_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + os.sep + log_dir_name
make_dir(log_file_folder)
log_file_str = log_file_folder + os.sep + log_file_name  # 输出格式
log_level = config.LOG_LEVEL  # 日志登记

handler = logging.FileHandler(log_file_str, encoding='UTF-8')
handler.setLevel(log_level)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
