# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  role.py
@Description    :  角色管理
@CreateTime     :  2020/3/19 21:14
------------------------------------
@ModifyTime     :  
"""
from permission import *


role = Blueprint('role', __name__)


@role.route('/index', methods=["POST"])
def index():
    '''
    获取角色
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    role_name = res_dir.get("role_name")
    role_key = res_dir.get("role_key")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    status = res_dir.get("status")
    order_column_name = res_dir.get("order_column_name")
    order_type = res_dir.get("order_type")
    try:
        model = Role.query
        if role_name:
            model = model.filter(Role.role_name.like("%" + role_name + "%"))
        if role_key:
            model = model.filter(Role.role_key.like("%" + role_key + "%"))
        if status is not None:
            model = model.filter(Role.status.in_((1, 2))) if status == 0 else model.filter(Role.status == status)
        if order_column_name and order_type and order_type.lower() in ['asc', 'desc']:
            model = model.order_by(text(f"{order_column_name} {order_type}"))
        if not page or page <= 0:
            page = 1
        if not page_size or page_size <= 0:
            page_size = 10
        result = model.order_by("created_at").paginate(page, page_size, error_out=False)
        data = construct_page_data(result)
        return SUCCESS(data=data)
    except Exception as e:
        app.logger.error(f"获取角色信息失败：{e}")
        return REQUEST_ERROR()


@role.route('/update', methods=["POST", "PUT"])
def update():
    '''
    更新角色
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
            model = Role.query.get(id)
            if model:
                dict_data = model_to_dict(model)
                #获取菜单列表和部门列表
                role_menu = Role_Menu.query.with_entities(Role_Menu.menu_id).filter(Role_Menu.role_id == id).order_by(
                    "menu_id").all()
                role_dept = Role_Dept.query.with_entities(Role_Dept.dept_id).filter(Role_Dept.role_id == id).order_by(
                    "dept_id").all()
                menu_list = [str(i[0]) for i in role_menu]
                dept_list = [str(i[0]) for i in role_dept]
                dict_data['role_menu'] = ','.join(menu_list)
                dict_data['role_dept'] = ','.join(dept_list)
                return SUCCESS(dict_data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = res_dir.get("id")
        role_name = res_dir.get("role_name")
        role_key = res_dir.get("role_key")
        role_sort = res_dir.get("role_sort")
        remark = res_dir.get("remark")
        status = res_dir.get("status")
        role_menu = res_dir.get("role_menu")
        data_scope = res_dir.get("data_scope")
        role_dept = res_dir.get("role_dept")
        if id and role_name and role_key:
            model = Role.query.get(id)
            if model:
                try:
                    token = request.headers["Authorization"]
                    user = verify_token(token)
                    model.role_name = role_name
                    model.role_key = role_key
                    model.role_sort = role_sort
                    model.data_scope = data_scope
                    model.status = status
                    model.remark = remark
                    model.update_by = user['name']
                    model.update()
                    try:
                        #更新菜单列表
                        update_menu(id, role_menu)
                        #更新部门
                        update_dept(id, role_dept)
                        return SUCCESS()
                    except Exception as e:
                        app.logger.error(f"更新菜单或部门失败:{e}")
                        return UPDATE_ERROR(msg="更新菜单或部门失败")
                except Exception as e:
                    app.logger.error(f"更新角色失败:{e}")
                    return UPDATE_ERROR()

            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()


@role.route('/create', methods=["PUT"])
def create():
    '''
    创建角色
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    role_name = res_dir.get("role_name")
    role_key = res_dir.get("role_key")
    role_sort = res_dir.get("role_sort")
    remark = res_dir.get("remark")
    status = res_dir.get("status")
    role_menu = res_dir.get("role_menu")
    token = request.headers["Authorization"]
    user = verify_token(token)
    if role_name and role_key:
        try:
            is_exist = Role.query.filter(Role.role_name == role_name).first()
            if is_exist:
                return CREATE_ERROR(msg="角色名称已存在")
            model = Role()
            model.role_name = role_name
            model.role_key = role_key
            model.role_sort = role_sort
            model.remark = remark
            model.status = status
            model.create_by = user['name']
            model.save()
            if role_menu:
                try:
                    # 向角色菜单表插入数据
                    role_id = model.id
                    menu_list = role_menu.split(',')
                    insert_list = []
                    for menu_id in menu_list:
                        insert_list.append({"role_id": role_id, "menu_id": menu_id})
                    if len(insert_list) > 0:
                        role_menu_model = Role_Menu()
                        role_menu_model.save_all(insert_list)
                    return SUCCESS()
                except Exception as e:
                    model.delete()
                    app.logger.error(f"新建角色失败:{e}")
                    return CREATE_ERROR()
            else:
                return SUCCESS()
        except Exception as e:
            app.logger.error(f"新建角色失败:{e}")
            return CREATE_ERROR()
    else:
        return NO_PARAMETER()


@role.route('/delete', methods=["DELETE"])
def delete():
    '''
    根据ID删除角色
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    role_id = res_dir.get("id")
    if role_id:
        try:
            role = Role.query.get(role_id)
            if role_id:
                # user_role = User_Role.query.filter_by(role_id=role_id).all()
                # if user_role:
                #     return DELETE_ERROR(msg="该角色已关联用户，无法删除！")
                role_dept = Role_Dept.query.filter_by(role_id=role_id).all()
                if role_dept:
                    for role in role_dept:
                        role.delete()
                role_menu = Role_Menu.query.filter_by(role_id=role_id).all()
                if role_menu:
                    for menu in role_menu:
                        menu.delete()
                role.delete()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除角色失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()


def update_menu(id, role_menu):
    menu_db = Role_Menu.query.filter(
        Role_Menu.role_id == id).all()
    if role_menu:  # 如果有菜单
        # 获取数据库菜单列表
        db_list = [str(i.menu_id) for i in menu_db]
        # 获取传过来的参数
        par_list = role_menu.split(',')
        # 获取需要删除和增加的数据
        add_list, less_list = get_diff(db_list, par_list)
        if len(less_list) > 0:
            # 删除没有权限的菜单
            for menu in menu_db:
                if str(menu.menu_id) in less_list:
                    menu.delete()
        if len(add_list) > 0:
            insert_list = []
            for menu_id in add_list:
                insert_list.append({"role_id": id, "menu_id": menu_id})
            role_menu_model = Role_Menu()
            role_menu_model.save_all(insert_list)
    else:  # 如果没菜单
        # 获取数据库菜单列表
        for menu in menu_db:
            menu.delete()


def update_dept(id, role_dept):
    dept_db = Role_Dept.query.filter(Role_Dept.role_id == id).all()
    if role_dept:
        # 获取数据库列表
        db_list = [str(i.dept_id) for i in dept_db]
        # 获取传过来的参数
        par_list = role_dept.split(',')
        # 获取需要删除和增加的数据
        add_list, less_list = get_diff(db_list, par_list)
        if len(less_list) > 0:
            # 删除没有权限的菜单
            for dept in dept_db:
                if str(dept.dept_id) in less_list:
                    dept.delete()
        if len(add_list) > 0:
            insert_list = []
            for dept_id in add_list:
                insert_list.append({"role_id": id, "dept_id": dept_id})
            role_menu_model = Role_Dept()
            role_menu_model.save_all(insert_list)
    else:
        for dept in dept_db:
            dept.delete()
