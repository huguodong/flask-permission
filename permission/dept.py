# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  dept.py
@Description    :  岗位信息
@CreateTime     :  2020/3/18 22:11
------------------------------------
@ModifyTime     :  
"""
from permission import *

dept = Blueprint('dept', __name__)


@dept.route('/findall', methods=["POST"])
def find_all():
    '''
    获取部门信息
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    dept_name = res_dir.get("dept_name")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    status = res_dir.get("status")
    if dept_name:
        # 部门名不为空，直接根据条件查询数据
        try:
            model = Dept.query.filter(Dept.dept_name.like("%" + dept_name + "%"))
            if status is not None:
                model = model.filter(Dept.status.in_((1, 2))) if status == 0 else model.filter(Dept.status == status)
            if not page or page <= 0:
                page = 1
            if not page_size or page_size <= 0:
                page_size = 10
            result = model.order_by("order_num").paginate(page, page_size, error_out=False)
            data = construct_page_data(result)
            return SUCCESS(data=data)
        except Exception as e:
            app.logger.error(f"获取岗位信息失败：{e}")
            return REQUEST_ERROR()
    else:
        # 部门为空，获取全部部门
        data = constructDeptTrees()  # 获取菜单树
        return jsonify(code=Code.SUCCESS.value, msg="ok", data=data)


@dept.route('/update', methods=["POST", "PUT"])
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
            model = Dept.query.get(id)
            if model:
                data = model_to_dict(model)
                return SUCCESS(data=data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = res_dir.get("id")
        dept_name = res_dir.get("dept_name")
        email = res_dir.get("email")
        leader = res_dir.get("leader")
        order_num = res_dir.get("order_num")
        parent_id = res_dir.get("parent_id")
        phone = res_dir.get("phone")
        remark = res_dir.get("remark")
        status = res_dir.get("status")

        if id and dept_name:
            model = Dept.query.get(id)
            if model:
                try:
                    token = request.headers["Authorization"]
                    user = verify_token(token)
                    model.dept_name = dept_name
                    model.parent_id = parent_id
                    model.leader = leader
                    model.email = email
                    model.order_num = order_num
                    model.phone = phone
                    model.status = status
                    model.remark = remark
                    model.update_by = user['name']
                    model.update()
                    return SUCCESS()
                except Exception as e:
                    app.logger.error(f"更新部门失败:{e}")
                    return UPDATE_ERROR()
            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()


@dept.route('/create', methods=["PUT"])
def create():
    '''
    创建部门
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    dept_name = res_dir.get("dept_name")
    email = res_dir.get("email")
    leader = res_dir.get("leader")
    order_num = res_dir.get("order_num")
    parent_id = res_dir.get("parent_id")
    phone = res_dir.get("phone")
    remark = res_dir.get("remark")
    status = res_dir.get("status")
    token = request.headers["Authorization"]
    user = verify_token(token)
    if dept_name:
        try:
            is_exist = Dept.query.filter(Dept.dept_name == dept_name, Dept.parent_id == parent_id).first()
            if is_exist:
                return CREATE_ERROR(msg="同级别该部门名称已存在")
            model = Dept()
            model.dept_name = dept_name
            model.parent_id = parent_id
            model.leader = leader
            model.email = email
            model.order_num = order_num
            model.phone = phone
            model.remark = remark
            model.status = status
            model.create_by = user['name']
            model.save()
            return SUCCESS()
        except Exception as e:
            app.logger.error(f"新建部门失败:{e}")
            return CREATE_ERROR()
    else:
        return NO_PARAMETER()


@dept.route('/delete', methods=["DELETE"])
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
            parent = Dept.query.filter_by(parent_id=id).all()
            if parent:
                return DELETE_ERROR(msg="该部门下存在子部门，无法删除！")
            role = Role_Dept.query.filter_by(dept_id=id).all()
            if role:
                return DELETE_ERROR(msg="该部门已与角色关联，无法删除！")
            model = Dept.query.get(id)
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


def constructDeptTrees(parentId=0):
    '''
    通过递归实现根据父ID查找子部门
    1.根据父ID获取该部门下的子部门
    2.遍历子部门，继续向下获取，直到最小部门
    3.如果没有遍历到，返回空的数组，有返回权限列表
    :param parentId:
    :return:dict
    '''
    dept_data = Dept.query.filter(Dept.parent_id == parentId).order_by('order_num').all()
    dept_dict = model_to_dict(dept_data)
    if len(dept_dict) > 0:
        data = []
        for dept in dept_dict:
            dept['children_list'] = constructDeptTrees(dept['id'])
            data.append(dept)
        return data
    return []
