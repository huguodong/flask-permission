# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  config.py
@Description    :  参数设置
@CreateTime     :  2020/3/22 13:39
------------------------------------
@ModifyTime     :  
"""
from permission import *

configs = Blueprint('configs', __name__)


@configs.route('/index', methods=["POST"])
def index():
    '''
    获取参数信息
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    config_name = res_dir.get("config_name")
    config_type = res_dir.get("config_type")
    config_key = res_dir.get("config_key")
    config_value = res_dir.get("config_value")
    order_column_name = res_dir.get("order_column_name")
    order_type = res_dir.get("order_type")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    try:
        model = Configs.query
        if config_name:
            model = model.filter(Configs.config_name.like("%" + config_name + "%"))
        if config_key:
            model = model.filter(Configs.config_key.like("%" + config_key + "%"))
        if config_value:
            model = model.filter(Configs.config_value.like("%" + config_value + "%"))
        if config_type:
            model = model.filter(Configs.config_type == config_type)
        if order_column_name and order_type and order_type.lower() in ['asc', 'desc']:
            model = model.order_by(text(f"{order_column_name} {order_type}"))
        if not page or page <= 0:
            page = 1
        if not page_size or page_size <= 0:
            page_size = 10
        result = model.paginate(page, page_size, error_out=False)
        data = construct_page_data(result)
        return SUCCESS(data=data)
    except Exception as e:
        app.logger.error(f"获取参数信息失败：{e}")
        return REQUEST_ERROR()


@configs.route('/update', methods=["POST", "PUT"])
def update():
    '''
       更新参数
       POST方法根据id返回数据
       PUT方法更新
       :return:
       '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    if request.method == "POST":
        id = res_dir.get("id")
        if id:
            model = Configs.query.get(id)
            if model:
                dict_data = model_to_dict(model)
                return SUCCESS(dict_data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = res_dir.get("id")
        config_name = res_dir.get("config_name")
        config_key = res_dir.get("config_key")
        config_value = res_dir.get("config_value")
        config_type = res_dir.get("config_type")
        remark = res_dir.get("remark")
        if id and config_name and config_key and config_value:
            model = Configs.query.get(id)
            if model:
                token = request.headers["Authorization"]
                user = verify_token(token)
                model.config_name = config_name
                model.config_key = config_key
                model.config_value = config_value.strip()
                model.config_type = config_type
                model.remark = remark
                model.update_by = user['name']
                try:
                    model.update()
                    return SUCCESS()
                except Exception as e:
                    app.logger.error(f"更新参数失败:{e}")
                    return UPDATE_ERROR()
            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()


@configs.route('/create', methods=["PUT"])
def create():
    '''
    创建参数信息
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    config_name = res_dir.get("config_name")
    config_key = res_dir.get("config_key")
    config_value = res_dir.get("config_value")
    config_type = res_dir.get("config_type")
    remark = res_dir.get("remark")
    if config_name and config_key and config_value:
        try:
            is_exist = Configs.query.filter(Configs.config_key == config_key).first()
            if is_exist:
                return CREATE_ERROR(msg="键名重复")
            token = request.headers["Authorization"]
            user = verify_token(token)
            model = Configs()
            model.config_name = config_name
            model.config_key = config_key
            model.config_value = config_value.strip()
            model.remark = remark
            model.config_type = config_type
            model.create_by = user['name']
            model.save()
            return SUCCESS()
        except Exception as e:
            app.logger.error(f"新建字典失败:{e}")
            return CREATE_ERROR()
    else:
        return NO_PARAMETER()


@configs.route('/delete', methods=["DELETE"])
def delete():
    '''
    参数删除
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    id = res_dir.get("id")
    if id:
        try:
            model = Configs.query.get(id)
            if model:
                model.delete()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除参数失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()
