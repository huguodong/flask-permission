# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :
------------------------------------
@File           :  route.py
@Description    :
@CreateTime     :  2020/2/24 22:08
------------------------------------
@ModifyTime     :
"""
import os
import random
import time

from basic import *

upload = Blueprint('upload', __name__)

#允许的后缀名
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload.route('/head_image', methods=["POST"])
def head_image():
    file = request.files.get('file')
    if file is None:
        return FILE_NO_FOUND(msg="请选择头像!")
    # 格式判断
    if file.content_type != "image/jpeg" and file.content_type != "image/png":
        return ERROR_FILE_TYPE("请上传有效图片文件!")
    # 后缀名判断
    if not allowed_file(file.filename):
        return ERROR_FILE_TYPE()
    # 大小限制判断
    if is_over_size(file, 2):
        return OVER_SIZE(msg="头像文件大小不能超过2MB")
    # 保存文件
    try:
        new_filename = time.strftime('%Y%m%d%H%M%S') + '%d' % random.randint(0, 100)
        new_filename = md5_sum(new_filename)
        new_filename += "." + file.filename.rsplit('.', 1)[1]
        upload_path = os.path.join(UPLOAD_HEAD_FOLDER, new_filename)
        file.save(upload_path)
        image_path = app_url + "/" + upload_path
        return SUCCESS(data=image_path)
    except Exception as e:
        return UPLOAD_FAILD("上传头像失败")



def is_over_size(file, max_size):
    '''
    判断文件大小是否超出限制
    :param file:
    :param M:
    :return:
    '''
    size = len(file.read())
    file.seek(0)
    if size / (1024 * 1024) > int(max_size):
        return True
    else:
        return False
