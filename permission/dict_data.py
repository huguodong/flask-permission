# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  dict_route.py
@Description    :  字典数据
@CreateTime     :  2020/3/14 16:10
------------------------------------
@ModifyTime     :  
"""
from permission import *

dictData = Blueprint('dictData', __name__)


@dictData.route('/index', methods=["POST"])
def index():
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    dict_type = res_dir.get("dict_type")
    dict_id = res_dir.get("dict_id")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    dict_label = res_dir.get("dict_label")
    dict_number = res_dir.get("dict_number")
    status = res_dir.get("status")
    order_column_name = res_dir.get("order_column_name")
    order_type = res_dir.get("order_type")
    if not page or page <= 0:
        page = 1
    if not page_size or page_size <= 0:
        page_size = 10

    if dict_type and dict_id is None:
        dict_data = Dict_Data.query.filter(Dict_Data.dict_type == dict_type).order_by('dict_sort').paginate(page,
                                                                                                            page_size,
                                                                                                            error_out=False)
        data = construct_page_data(dict_data)  # 格式化返回数据
        return jsonify(code=Code.SUCCESS.value, msg="ok", data=data)
    elif dict_id is not None:
        dict_data = Dict_Data.query
        if dict_id != 0:
            dict_data = dict_data.filter(Dict_Data.dict_id == dict_id)
        if dict_label:
            dict_data = dict_data.filter(Dict_Data.dict_label.like("%" + dict_label + "%"))
        if dict_number:
            dict_data = dict_data.filter(Dict_Data.dict_number == int(dict_number))
        if dict_type:
            dict_data = dict_data.filter(Dict_Data.dict_type.like("%" + dict_type + "%"))
        if status is not None:
            dict_data = dict_data.filter(Dict_Data.status.in_((1, 2))) if status == 0 else dict_data.filter(
                Dict_Data.status == status)
        if order_column_name and order_type and order_type.lower() in ['asc', 'desc']:
            dict_data = dict_data.order_by(text(f"{order_column_name} {order_type}"))

        result = dict_data.paginate(page, page_size, error_out=False)
        data = construct_page_data(result)  # 格式化返回数据
        return SUCCESS(data=data)
    else:
        return PARAMETER_ERR()


@dictData.route('/create', methods=["PUT"])
def create():
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    dict_id = res_dir.get("dict_id")
    dict_label = res_dir.get("dict_label")
    dict_number = res_dir.get("dict_number")
    css_class = res_dir.get("css_class")
    list_class = res_dir.get("list_class")
    is_default = res_dir.get("is_default")
    dict_sort = res_dir.get("dict_sort")
    dict_value = res_dir.get("dict_value")
    status = res_dir.get("status")
    remark = res_dir.get("remark")
    if dict_id and dict_label if dict_label is not None else dict_value:
        try:
            token = request.headers["Authorization"]
            user = verify_token(token)
            dict_type = Dict_Type.query.get(dict_id).dict_type
            model = Dict_Data()
            model.dict_id = dict_id
            model.dict_type = dict_type
            model.dict_label = dict_label
            model.dict_number = dict_number
            model.css_class = css_class
            model.list_class = list_class
            model.is_default = is_default
            model.dict_sort = dict_sort
            model.dict_value = dict_value
            model.remark = remark
            model.status = status
            model.create_by = user['name']
            model.save()
            return SUCCESS()
        except Exception as e:
            app.logger.error(f"创建字典数据失败:{e}")
            return CREATE_ERROR()
    else:
        return NO_PARAMETER()


@dictData.route('/update', methods=["POST", "PUT"])
def update():
    '''
    更新字典数据
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
            model = Dict_Data.query.get(id)
            if model:
                dict_data = model_to_dict(model)
                return SUCCESS(dict_data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = res_dir.get("id")
        dict_id = res_dir.get("dict_id")
        dict_label = res_dir.get("dict_label")
        dict_number = res_dir.get("dict_number")
        css_class = res_dir.get("css_class")
        list_class = res_dir.get("list_class")
        is_default = res_dir.get("is_default")
        dict_sort = res_dir.get("dict_sort")
        status = res_dir.get("status")
        remark = res_dir.get("remark")
        if id and dict_id and dict_label and dict_number:
            model = Dict_Data.query.get(id)
            if model:
                token = request.headers["Authorization"]
                user = verify_token(token)
                model.dict_id = dict_id
                model.dict_label = dict_label
                model.dict_number = dict_number
                model.css_class = css_class
                model.list_class = list_class
                model.is_default = is_default
                model.dict_sort = dict_sort
                model.remark = remark
                model.status = status
                model.update_by = user['name']
                try:
                    model.update()
                    return SUCCESS()
                except Exception as e:
                    app.logger.error(f"更新字典数据失败:{e}")
                    return UPDATE_ERROR()
            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()


@dictData.route('/delete', methods=["DELETE"])
def delete():
    '''
    根据id删除字典数据
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    dict_id = res_dir.get("id")
    if dict_id:
        try:
            model = Dict_Data.query.get(dict_id)
            if model:
                model.delete()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()
