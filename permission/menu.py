# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  menu_route.py
@Description    :  菜单方面的请求
@CreateTime     :  2020/3/8 15:55
------------------------------------
@ModifyTime     :  
"""
from permission import *

menu = Blueprint('menu', __name__)


@menu.route('/find_all_menu', methods=["POST"])
# @login_required
def find_all_menu():
    '''
    根据用户id获取菜单
    :return:
    '''
    res_dir = request.get_json()
    user_id = res_dir.get("uuid")
    data = constructMenuTrees(user_id=user_id)  # 获取菜单树
    return jsonify(code=Code.SUCCESS.value, msg="ok", data=data)


@menu.route('/menus', methods=["POST"])
def menus():
    '''
    获取菜单信息
    :param:{"menu_name":"菜单","visible":0,"page":1,"page_size":10,"order_column_name":"","order_type":""}
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    visible = res_dir.get("visible")
    menu_name = res_dir.get("menu_name")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    # 如果没有查询条件，则返回全部数据
    if not visible and not menu_name:
        data = constructMenuTrees()  # 获取菜单树
        return jsonify(code=Code.SUCCESS.value, msg="ok", data=data)
    else:
        if not page or page <= 0:
            page = 1
        if not page_size or page_size <= 0:
            page_size = 10
        if visible == 0:
            visible = (1, 2)
        else:
            visible = (visible,)
        # 根据条件查询，并分页
        menu_data = Menu.query.filter(
            Menu.menu_name.like("%" + menu_name + "%") if menu_name is not None else "",
            Menu.visible.in_(visible),
        ).order_by('menu_name').paginate(page, page_size, error_out=False)
        data = construct_menu_data(menu_data)  # 格式化返回数据
        return jsonify(code=Code.SUCCESS.value, msg="ok", data=data)


@menu.route('/create', methods=["PUT"])
def create():
    '''
    新建菜单或权限
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    # 根据token获取用户id
    try:
        token = request.headers["Authorization"]
        user = verify_token(token)
        menu = Menu()
        menu.parent_id = res_dir.get("parent_id"),
        menu.menu_name = res_dir.get("menu_name"),
        menu.menu_type = res_dir.get("menu_type"),
        menu.icon = res_dir.get("icon"),
        menu.is_frame = res_dir.get("is_frame"),
        menu.url = res_dir.get("url"),
        menu.route_name = res_dir.get("route_name"),
        menu.route_path = res_dir.get("route_path"),
        menu.route_component = res_dir.get("route_component"),
        menu.route_cache = res_dir.get("route_cache"),
        menu.perms = res_dir.get("perms"),
        menu.visible = res_dir.get("visible"),
        menu.order_num = res_dir.get("order_num"),
        menu.remark = res_dir.get("remark"),
        menu.create_by = user['name'],
        menu.save()
        return SUCCESS()
    except Exception as e:
        app.logger.error(f"新建菜单失败:{e}")
        return CREATE_ERROR()


@menu.route('/delete', methods=["DELETE"])
def delete():
    '''
    根据id删除菜单或权限
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    menu_id = res_dir.get("id")
    if menu_id:
        try:
            parent = Menu.query.filter_by(parent_id=menu_id).all()
            if parent:
                return DELETE_ERROR(msg="该菜单下存在子菜单，无法删除！")
            role = Role_Menu.query.filter_by(menu_id=menu_id).all()
            if role:
                return DELETE_ERROR(msg="该菜单已与角色关联，无法删除！")
            menu = Menu.query.get(menu_id)
            if menu:
                menu.delete()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除菜单失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()


@menu.route('/update', methods=["POST", "PUT"])
def update():
    '''
    更新菜单或权限
    POST方法根据id返回数据
    PUT方法更新菜单或权限
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    if request.method == "POST":
        menu_id = res_dir.get("id")
        if id:
            menu = Menu.query.get(menu_id)
            if menu:
                menu_data = model_to_dict(menu)
                return SUCCESS(menu_data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        menu_id = res_dir.get("id")
        menu_name = res_dir.get("menu_name")
        if id and menu_name:
            model = Menu.query.get(menu_id)
            if model:
                token = request.headers["Authorization"]
                user = verify_token(token)
                model.parent_id = res_dir.get("parent_id")
                model.menu_name = res_dir.get("menu_name")
                model.menu_type = res_dir.get("menu_type")
                model.icon = res_dir.get("icon")
                model.is_frame = res_dir.get("is_frame")
                model.url = res_dir.get("url")
                model.route_name = res_dir.get("route_name")
                model.route_path = res_dir.get("route_path")
                model.route_component = res_dir.get("route_component")
                model.route_cache = res_dir.get("route_cache")
                model.perms = res_dir.get("perms")
                model.visible = res_dir.get("visible")
                model.order_num = res_dir.get("order_num")
                model.remark = res_dir.get("remark")
                model.update_by = user['name']
                try:
                    model.update()
                    return SUCCESS()
                except Exception as e:
                    app.logger.error(f"更新菜单失败:{e}")
                    return UPDATE_ERROR()
            else:
                return ID_NOT_FOUND()
        else:
            return PARAMETER_ERR()


def constructMenuTrees(parentId=0, user_id=None):
    '''
    通过递归实现根据父ID查找子菜单,如果传入用户id则只查询该用户的权限否则查询所有权限,一级菜单父id默认是0
    1.根据父ID获取该菜单下的子菜单或权限
    2.遍历子菜单或权限，继续向下获取，直到最小级菜单或权限
    3.如果没有遍历到，返回空的数组，有返回权限列表
    :param user_id:
    :param parentId:
    :return:dict
    '''
    if user_id:
        menu_data = Menu.query.join(Role_Menu, Menu.id == Role_Menu.menu_id).join(User_Role,
                                                                                  User_Role.role_id == Role_Menu.role_id).filter(
            User_Role.user_id == user_id).filter(Menu.parent_id == parentId).order_by('order_num').all()
    else:
        menu_data = Menu.query.filter(Menu.parent_id == parentId).order_by('order_num').all()
    menu_dict = menu_to_dict(menu_data)
    if len(menu_dict) > 0:
        data = []
        for menu in menu_dict:
            menu['children_list'] = constructMenuTrees(menu['id'], user_id)
            data.append(menu)
        return data
    return []


def menu_to_dict(result):
    '''
    格式化菜单字段显示顺序
    :param result:
    :return:
    '''
    data = []
    for menu in result:
        child = {
            "id": menu.id,
            "menu_name": menu.menu_name,
            "parent_id": menu.parent_id,
            "order_num": menu.order_num,
            "url": menu.url,
            "menu_type": menu.menu_type,
            "visible": menu.visible,
            "perms": menu.perms,
            "icon": menu.icon,
            "is_frame": menu.is_frame,
            "create_by": menu.create_by,
            "created_at": menu.created_at,
            "update_by": menu.update_by,
            "updated_at": menu.updated_at,
            "remark": menu.remark,
            "route_name": menu.route_name,
            "route_path": menu.route_path,
            "route_cache": menu.route_cache,
            "route_component": menu.route_component,
        }
        data.append(child)
    return data
