# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  route.py
@Description    :  用户相关的请求
@CreateTime     :  2020/2/24 21:55
------------------------------------
@ModifyTime     :  
"""
from permission import *

user = Blueprint('user', __name__)


@user.route('/login', methods=["POST"])
def login():
    '''
    用户登录
    :return:token
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    # 获取前端传过来的参数
    username = res_dir.get("username")
    password = res_dir.get("password")
    # 校验参数
    if not all([username, password]):
        return jsonify(code=Code.NOT_NULL.value, msg="用户名和密码不能为空")
    try:
        user = User.query.filter_by(user_name=username).first()
    except Exception as e:
        app.logger.error("login error：{}".format(e))
        return jsonify(code=Code.REQUEST_ERROR.value, msg="获取信息失败")
    if user is None or not user.check_password(password) or user.del_flag == 2 or user.status == 2:
        return jsonify(code=Code.ERR_PWD.value, msg="用户名或密码错误")

    # 获取用户信息，传入生成token的方法，并接收返回的token
    # 获取用户角色
    user_role = Role.query.join(User_Role, Role.id == User_Role.role_id).join(User,
                                                                              User_Role.user_id == user.id).filter(
        User.id == user.id).all()
    role_list = [i.role_key for i in user_role]
    token = create_token(user.id, user.user_name, role_list)
    data = {'token': token, 'userId': user.id, 'userName': user.user_name, 'nickname': user.nickname}
    # 记录登录ip将token存入rerdis
    try:
        user.login_ip = request.remote_addr
        user.update()
        Redis.write(f"token_{user.user_name}", token)

    except Exception as e:
        return jsonify(code=Code.UPDATE_DB_ERROR.value, msg="登录失败")
    if token:
        # 把token返回给前端
        return jsonify(code=Code.SUCCESS.value, msg="登录成功", data=data)
    else:
        return jsonify(code=Code.REQUEST_ERROR.value, msg="请求失败", data=token)


@user.route('/logout', methods=["POST"])
@login_required()
def logout():
    '''
    注销方法：redis删除token
    :return:
    '''
    try:
        token = request.headers["Authorization"]
        user = verify_token(token)
        if user:
            key = f"token_{user.get('name')}"
            redis_token = Redis.read(key)
            if redis_token:
                Redis.delete(key)
            return SUCCESS()
        else:
            return AUTH_ERR()
    except Exception as e:
        app.logger.error(f"注销失败")
        return REQUEST_ERROR()


@user.route('/check_token', methods=["POST"])
def check_token():
    # 在请求头上拿到token
    token = request.headers["Authorization"]
    user = verify_token(token)
    if user:
        key = f"token_{user.get('name')}"
        redis_token = Redis.read(key)
        if redis_token == token:
            return SUCCESS(data=user.get('id'))
        else:
            return OTHER_LOGIN()
    else:
        return AUTH_ERR()


@user.route('/index', methods=["POST"])
def index():
    '''
    获取用户
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    user_name = res_dir.get("user_name")
    phone = res_dir.get("phone")
    dept_id = res_dir.get("dept_id")
    order_column_name = res_dir.get("order_column_name")
    order_type = res_dir.get("order_type")
    page = res_dir.get("page")
    page_size = res_dir.get("page_size")
    status = res_dir.get("status")
    try:
        model = User.query.filter(User.del_flag == 1)
        if user_name:
            model = model.filter(User.user_name.like("%" + user_name + "%"))
        if phone:
            model = model.filter(User.phone.like("%" + phone + "%"))
        if dept_id:
            # 根据部门id查找该部门下的用户，包括子部门
            dept = Dept.query.filter_by(id=dept_id).first()
            dept_ids = find_childern(dept)
            model = model.filter(User.dept_id.in_(dept_ids))
        if status is not None:
            model = model.filter(User.status.in_((1, 2))) if status == 0 else model.filter(User.status == status)
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
        app.logger.error(f"获取用户信息失败：{e}")
        return REQUEST_ERROR()


@user.route('/update', methods=["POST", "PUT"])
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
            model = User.query.get(id)
            if model:
                dict_data = model_to_dict(model)
                del dict_data["password"]  # 删除密码，不返回前端
                # 获取角色和岗位
                user_post = User_Post.query.with_entities(User_Post.post_id).filter(User_Post.user_id == id).order_by(
                    "post_id").all()
                user_role = User_Role.query.with_entities(User_Role.role_id).filter(User_Role.user_id == id).order_by(
                    "role_id").all()
                post_list = [str(i[0]) for i in user_post]
                role_list = [str(i[0]) for i in user_role]
                dict_data['user_post'] = ','.join(post_list)
                dict_data['user_role'] = ','.join(role_list)
                return SUCCESS(dict_data)
            else:
                return ID_NOT_FOUND()
        else:
            PARAMETER_ERR()
    if request.method == "PUT":
        id = res_dir.get("id")
        user_name = res_dir.get("user_name")
        phone = res_dir.get("phone")
        dept_id = res_dir.get("dept_id")
        avatar = res_dir.get("avatar")
        email = res_dir.get("email")
        nickname = res_dir.get("nickname")
        status = res_dir.get("status")
        user_role = res_dir.get("user_role")
        user_post = res_dir.get("user_post")
        sex = res_dir.get("sex")
        remark = res_dir.get("remark")
        if id and user_name and dept_id:
            model = User.query.get(id)
            if model:
                try:
                    token = request.headers["Authorization"]
                    user = verify_token(token)
                    model.user_name = user_name
                    model.phone = phone
                    model.dept_id = dept_id
                    model.avatar = avatar
                    model.email = email
                    model.nickname = nickname
                    model.sex = sex
                    model.remark = remark
                    model.status = status
                    model.update_by = user['name']
                    model.update()
                    try:
                        update_post(id, user_post)
                        update_role(id, user_role)
                        return SUCCESS()
                    except Exception as e:
                        app.logger.error(f"更新角色或岗位失败:{e}")
                        return UPDATE_ERROR(msg="更新角色或岗位失败")
                except Exception as e:
                    app.logger.error(f"更新用户失败:{e}")
                    return UPDATE_ERROR()
            else:
                return ID_NOT_FOUND()
        else:
            return NO_PARAMETER()
    return SUCCESS()


@user.route('/create', methods=["PUT"])
def create():
    '''
    创建用户
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    user_name = res_dir.get("user_name")
    phone = res_dir.get("phone")
    dept_id = res_dir.get("dept_id")
    avatar = res_dir.get("avatar")
    email = res_dir.get("email")
    nickname = res_dir.get("nickname")
    password = res_dir.get("password")
    status = res_dir.get("status")
    user_role = res_dir.get("user_role")
    user_post = res_dir.get("user_post")
    sex = res_dir.get("sex")
    remark = res_dir.get("remark")
    token = request.headers["Authorization"]
    user = verify_token(token)
    if user_name and dept_id and password and nickname:
        try:
            is_exist = User.query.filter(User.user_name == user_name).first()
            if is_exist:
                return CREATE_ERROR(msg="角色名已存在")
            # 添加用户
            model = User()
            model.user_name = user_name
            model.phone = phone
            model.dept_id = dept_id
            model.avatar = avatar
            model.email = email
            model.nickname = nickname
            model.password = create_passwd(password)
            model.sex = sex
            model.remark = remark
            model.status = status
            model.create_by = user['name']
            model.save()
            # 添加角色和岗位
            try:
                # 添加角色
                if user_role:
                    role_list = user_role.split(',')
                    insert_list = []
                    for role_id in role_list:
                        insert_list.append({"role_id": role_id, "user_id": model.id})
                    if len(insert_list) > 0:
                        user_role_model = User_Role()
                        user_role_model.save_all(insert_list)
                # 添加岗位
                if user_post:
                    post_list = user_post.split(',')
                    insert_list = []
                    for post_id in post_list:
                        insert_list.append({"post_id": post_id, "user_id": model.id})
                    if len(insert_list) > 0:
                        user_post_model = User_Post()
                        user_post_model.save_all(insert_list)
                return SUCCESS()
            except Exception as e:
                app.logger.error(f"添加角色或岗位失败:{e}")
                return CREATE_ERROR(msg="添加角色或岗位失败")
        except Exception as e:
            return CREATE_ERROR()
    else:
        return NO_PARAMETER()


@user.route('/delete', methods=["DELETE"])
def delete():
    '''
    根据id删除用户
    :return:
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    userid = res_dir.get("id")
    if userid:
        try:
            model = User.query.get(userid)
            if model:
                model.del_flag = 2
                model.update()
                return SUCCESS()
            else:
                return ID_NOT_FOUND()
        except Exception as e:
            app.logger.error(f"删除失败:{e}")
            return DELETE_ERROR()
    else:
        return PARAMETER_ERR()


def find_childern(dept):
    '''
     获取部门下的子部门ID元祖
     :param dept:
    :return: tuple
     '''
    dept_ids = [dept.id]
    dept_id = get_dept_by_parentId(dept.id)
    dept_ids += dept_id
    return tuple(dept_ids)


def get_dept_by_parentId(parentId):
    '''
    递归查找部门和子部门id
    :param parentId:
    :return:
    '''
    dept_data = Dept.query.filter(Dept.parent_id == parentId).all()
    if len(dept_data) > 0:
        data = []
        for dept in dept_data:
            ids = get_dept_by_parentId(dept.id)
            data += ids
            data += (str(dept.id))
        return data
    return []


def update_post(userid, user_post):
    post_db = User_Post.query.filter(
        User_Post.user_id == userid).all()
    if user_post:  # 如果有菜单
        # 获取数据库菜单列表
        db_list = [str(i.post_id) for i in post_db]
        # 获取传过来的参数
        par_list = user_post.split(',')
        # 获取需要删除和增加的数据
        add_list, less_list = get_diff(db_list, par_list)
        if len(less_list) > 0:
            # 删除没有权限的菜单
            for post in post_db:
                if str(post.post_id) in less_list:
                    post.delete()
        if len(add_list) > 0:
            insert_list = []
            for post_id in add_list:
                insert_list.append({"user_id": userid, "post_id": post_id})
            role_menu_model = User_Post()
            role_menu_model.save_all(insert_list)
    else:
        for post in post_db:
            post.delete()


def update_role(userid, user_role):
    role_db = User_Role.query.filter(
        User_Role.user_id == userid).all()
    if user_role:  # 如果有菜单
        # 获取数据库菜单列表
        db_list = [str(i.role_id) for i in role_db]
        # 获取传过来的参数
        par_list = user_role.split(',')
        # 获取需要删除和增加的数据
        add_list, less_list = get_diff(db_list, par_list)
        if len(less_list) > 0:
            # 删除没有权限的菜单
            for role in role_db:
                if str(role.role_id) in less_list:
                    role.delete()
        if len(add_list) > 0:
            insert_list = []
            for role_id in add_list:
                insert_list.append({"user_id": userid, "role_id": role_id})
            role_menu_model = User_Role()
            role_menu_model.save_all(insert_list)
    else:
        for role in role_db:
            role.delete()
