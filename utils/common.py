# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  common.py
@Description    :  
@CreateTime     :  2020/3/7 19:01
------------------------------------
@ModifyTime     :  
"""

# 导入依赖包
import functools
import hashlib

from flask import request, jsonify, current_app as app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from conf import config
from utils.code_enum import Code


def create_token(user_id, user_name, role_list):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(config.SECRET_KEY, expires_in=config.EXPIRES_IN)
    # 接收用户id转换与编码
    token = None
    try:
        token = s.dumps({"id": user_id, "name": user_name, "role": role_list}).decode("ascii")
    except Exception as e:
        app.logger.error("获取token失败:{}".format(e))
    return token


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(config.SECRET_KEY)
    try:
        # 转换为字典
        data = s.loads(token)
        return data
    except Exception as e:
        app.logger.error(f"token转换失败:{e}")
        return None


def login_required(*role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                # 在请求头上拿到token
                token = request.headers["Authorization"]
            except Exception as e:
                # 没接收的到token,给前端抛出错误
                return jsonify(code=Code.NO_PARAMETER.value, msg='缺少参数token')
            s = Serializer(config.SECRET_KEY)
            try:
                user = s.loads(token)
                if role:
                    # 获取token中的权限列表如果在参数列表中则表示有权限，否则就表示没有权限
                    user_role = user['role']
                    result = [x for x in user_role if x in list(role)]
                    if not result:
                        return jsonify(code=Code.ERR_PERMISSOM.value, msg="权限不够")
            except Exception as e:
                return jsonify(code=Code.LOGIN_TIMEOUT.value, msg="登录已过期")
            return func(*args, **kw)
        return wrapper
    return decorator


def model_to_dict(result):
    '''
    查询结果转换为字典
    :param result:
    :return:
    '''
    from collections import Iterable
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')



def construct_page_data(data):
    '''
    分页需要返回的数据
    :param data:
    :return:
    '''
    page = {"page_no": data.page,  # 当前页数
            "page_size": data.per_page,  # 每页显示的属性
            "tatal_page": data.pages,  # 总共的页数
            "tatal_count": data.total,  # 查询返回的记录总数
            "is_first_page": True if data.page == 1 else False,  # 是否第一页
            "is_last_page": False if data.has_next else True  # 是否最后一页
            }
    # result = menu_to_dict(data.items)
    result = model_to_dict(data.items)
    data = {"page": page, "list": result}
    return data


def construct_menu_data(data):
    '''
    菜单分页需要返回的数据
    :param data:
    :return:
    '''
    page = {"page_no": data.page,  # 当前页数
            "page_size": data.per_page,  # 每页显示的属性
            "tatal_page": data.pages,  # 总共的页数
            "tatal_count": data.total,  # 查询返回的记录总数
            "is_first_page": True if data.page == 1 else False,  # 是否第一页
            "is_last_page": False if data.has_next else True  # 是否最后一页
            }
    # result = menu_to_dict(data.items)
    result = menu_to_dict(data.items)
    data = {"page": page, "list": result}
    return data


def SUCCESS(data=None):
    return jsonify(code=Code.SUCCESS.value, msg="ok", data=data)


def NO_PARAMETER(msg="未接收到参数!"):
    return jsonify(code=Code.NO_PARAMETER.value, msg=msg)


def PARAMETER_ERR(msg="参数错误!"):
    return jsonify(code=Code.NO_PARAMETER.value, msg=msg)


def OTHER_LOGIN(msg="其他客户端登录!"):
    return jsonify(code=Code.OTHER_LOGIN.value, msg=msg)


def AUTH_ERR(msg="身份验证失败!"):
    return jsonify(code=Code.ERROR_TOKEN.value, msg=msg)


def TOKEN_ERROR(msg="Token校验失败!"):
    return jsonify(code=Code.ERROR_TOKEN.value, msg=msg)


def REQUEST_ERROR(msg="请求失败!"):
    return jsonify(code=Code.REQUEST_ERROR.value, msg=msg)


def ID_NOT_FOUND(msg="数据不存在!"):
    return jsonify(code=Code.ID_NOT_FOUND.value, msg=msg)


def CREATE_ERROR(msg="创建失败!"):
    return jsonify(code=Code.CREATE_DB_ERROR.value, msg=msg)


def UPDATE_ERROR(msg="更新失败!"):
    return jsonify(code=Code.UPDATE_DB_ERROR.value, msg=msg)


def DELETE_ERROR(msg="删除失败"):
    return jsonify(code=Code.DELETE_DB_ERROR.value, msg=msg)


def FILE_NO_FOUND(msg="请选择文件!"):
    return jsonify(code=Code.FILE_NO_FOUND.value, msg=msg)


def ERROR_FILE_TYPE(msg="无效的格式!"):
    return jsonify(code=Code.ERROR_FILE_TYPE.value, msg=msg)


def UPLOAD_FAILD(msg="上传失败!"):
    return jsonify(code=Code.UPLOAD_FAILD.value, msg=msg)


def OVER_SIZE(msg="文件大小超出限制!"):
    return jsonify(code=Code.OVER_SIZE.value, msg=msg)


def get_diff(old_list, new_list):
    # 计算old_list比new_list多的
    less_list = list(set(old_list) - set(new_list))
    # 计算new_list比old_list多的
    add_list = list(set(new_list) - set(old_list))
    return add_list, less_list


def create_passwd(passwd):
    # 创建md5对象
    m = hashlib.md5()
    b = passwd.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5


def md5_sum(strs):
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5
