# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  post_route.py
@Description    :  岗位路由
@CreateTime     :  2020/3/18 20:58
------------------------------------
@ModifyTime     :  
"""
from permission import *


post = Blueprint('post', __name__)


@post.route('/index', methods=["POST"])
def index():
    '''
    获取岗位
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    post_name = res_dir.get("post_name")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    status = res_dir.get("status")
    order_column_name = res_dir.get("order_column_name")
    order_type = res_dir.get("order_type")
    try:
        model = Post.query
        if post_name:
            model = model.filter(Post.post_name.like("%" + post_name + "%"))
        if status is not None:
            model = model.filter(Post.status.in_((1, 2))) if status == 0 else model.filter(Post.status == status)
        if order_column_name and order_type and order_type.lower() in ['asc', 'desc']:
            model = model.order_by(text(f"{order_column_name} {order_type}"))
        if not page or page <= 0:
            page = 1
        if not page_size or page_size <= 0:
            page_size = 10
        result = model.order_by("post_sort").paginate(page, page_size, error_out=False)
        data = construct_page_data(result)
        return SUCCESS(data=data)
    except Exception as e:
        app.logger.error(f"获取岗位信息失败：{e}")
        return REQUEST_ERROR()


@post.route('/update', methods=["POST", "PUT"])
def update():
    '''
        更新岗位
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
            model = Post.query.get(id)
            if model:
                dict_data = model_to_dict(model)
                return SUCCESS(dict_data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = res_dir.get("id")
        post_name = res_dir.get("post_name")
        post_code = res_dir.get("post_code")
        post_sort = res_dir.get("post_sort")
        status = res_dir.get("status")
        remark = res_dir.get("remark")

        if id and post_name and post_code:
            model = Post.query.get(id)
            if model:
                token = request.headers["Authorization"]
                user = verify_token(token)
                model.post_name = post_name
                model.post_code = post_code
                model.post_sort = post_sort
                model.status = status
                model.remark = remark
                model.update_by = user['name']
                try:
                    model.update()
                    return SUCCESS()
                except Exception as e:
                    app.logger.error(f"更新岗位失败:{e}")
                    return UPDATE_ERROR()
            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()


@post.route('/create', methods=["PUT"])
def create():
    '''
    创建岗位
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    post_name = res_dir.get("post_name")
    post_code = res_dir.get("post_code")
    post_sort = res_dir.get("post_sort")
    remark = res_dir.get("remark")
    status = res_dir.get("status")
    token = request.headers["Authorization"]
    user = verify_token(token)
    if post_name and post_code:
        try:
            is_exist = Post.query.filter(Post.post_name == post_name).first()
            if is_exist:
                return CREATE_ERROR(msg="岗位名称已存在")
            model = Post()
            model.post_name = post_name
            model.post_code = post_code
            model.post_sort = post_sort
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


@post.route('/delete', methods=["DELETE"])
def delete():
    '''
        根据ID删除岗位
        :return:
        '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    id = res_dir.get("id")
    if id:
        try:
            model = Post.query.get(id)
            if model:
                model.delete()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除岗位失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()
