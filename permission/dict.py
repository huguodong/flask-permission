# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  dict_route.py.py
@Description    :  
@CreateTime     :  2020/3/16 21:45
------------------------------------
@ModifyTime     :  
"""
from permission import *

dict = Blueprint('dict', __name__)


@dict.route('/index', methods=["POST"])
def index():
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    model = Dict_Type.query
    dict_name = res_dir.get("dict_name")
    dict_type = res_dir.get("dict_type")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    status = res_dir.get("status")
    order_column_name = res_dir.get("order_column_name")
    order_type = res_dir.get("order_type")
    try:
        if dict_name:
            model = model.filter(Dict_Type.dict_name.like("%" + dict_name + "%"))
        if dict_type:
            model = model.filter(Dict_Type.dict_type.like("%" + dict_type + "%"))
        if status is not None:
            model = model.filter(Dict_Type.status.in_((1, 2))) if status == 0 else model.filter(
                Dict_Type.status == status)
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
        app.logger.error(f"获取字典失败：{e}")
        return REQUEST_ERROR()


@dict.route('/update', methods=["POST", "PUT"])
def update():
    '''
    更新字典
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
            model = Dict_Type.query.get(id)
            if model:
                data = model_to_dict(model)
                return SUCCESS(data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = res_dir.get("id")
        dict_value_type = res_dir.get("dict_value_type")
        dict_name = res_dir.get("dict_name")
        dict_type = res_dir.get("dict_type")
        status = res_dir.get("status")
        dict_id = res_dir.get("dict_id")
        if id and dict_type and dict_name and dict_value_type:
            model = Dict_Type.query.get(id)
            if model:
                token = request.headers["Authorization"]
                user = verify_token(token)
                model.dict_name = dict_name
                model.dict_type = dict_type
                model.dict_value_type = dict_value_type
                model.status = status
                model.dict_id = dict_id
                model.update_by = user['name']
                try:
                    model.update()
                    return SUCCESS()
                except Exception as e:
                    app.logger.error(f"更新字典失败:{e}")
                    return UPDATE_ERROR()
            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()


@dict.route('/create', methods=["PUT"])
def create():
    '''
    创建字典
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    dict_name = res_dir.get("dict_name")
    dict_type = res_dir.get("dict_type")
    dict_value_type = res_dir.get("dict_value_type")
    remark = res_dir.get("remark")
    status = res_dir.get("status")
    if dict_name and dict_type and dict_value_type:
        try:
            is_exist = Dict_Type.query.filter(Dict_Type.dict_type == dict_type).first()
            if is_exist:
                return CREATE_ERROR(msg="字典类型已存在")
            token = request.headers["Authorization"]
            user = verify_token(token)
            model = Dict_Type()
            model.dict_name = dict_name
            model.dict_type = dict_type
            model.dict_value_type = dict_value_type
            model.remark = remark
            model.status = status
            model.create_by = user['name']
            model.save()
            return SUCCESS()
        except Exception as e:
            app.logger.error(f"新建字典失败:{e}")
            return CREATE_ERROR()
    else:
        return NO_PARAMETER()


@dict.route('/delete', methods=["DELETE"])
def delete():
    '''
    根据ID删除字典
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    dict_id = res_dir.get("id")
    if dict_id:
        try:
            is_exist = Dict_Data.query.filter(Dict_Data.dict_id == dict_id).first()
            if is_exist:
                return DELETE_ERROR(msg="该字典存在数据，无法删除！")
            model = Dict_Type.query.get(dict_id)
            if model:
                model.delete()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除字典失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()
