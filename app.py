from flask import Flask, jsonify
from flask_cors import CORS

from db import db
from conf import config
from permission import dict_data, menu, user, dict, post, dept, role, configs
from basic import upload
from utils.code_enum import Code
from utils.conf_log import handler


def create_app():
    app = Flask(__name__)

    # 设置返回jsonify方法返回dict不排序
    app.config['JSON_SORT_KEYS'] = False
    # 设置返回jsonify方法返回中文不转为Unicode格式
    app.config['JSON_AS_ASCII'] = False

    # 配置跨域
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 注册蓝图
    register_blueprints(app)

    # 加载数据库
    init_db(app)

    # 加载redis配置
    init_redis(app)

    # 加载日志
    app.logger.addHandler(handler)
    return app


def register_blueprints(app):
    '''
    创建蓝图
    :param app:
    :return:
    '''
    app.register_blueprint(user.user, url_prefix='/api/user')
    app.register_blueprint(menu.menu, url_prefix='/api/menu')
    app.register_blueprint(dict.dict, url_prefix='/api/dict')
    app.register_blueprint(dict_data.dictData, url_prefix='/api/dictData')
    app.register_blueprint(post.post, url_prefix='/api/post')
    app.register_blueprint(dept.dept, url_prefix='/api/dept')
    app.register_blueprint(role.role, url_prefix='/api/role')
    app.register_blueprint(configs.configs, url_prefix='/api/configs')
    app.register_blueprint(upload.upload, url_prefix='/api/upload')


def init_db(app):
    '''
    加载数据库
    :param app:
    :return:
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(config.MYSQL['USER'],
                                                                            config.MYSQL['PASSWD'],
                                                                            config.MYSQL['HOST'],
                                                                            config.MYSQL['PORT'], config.MYSQL['DB'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 跟踪对象的修改，在本例中用不到调高运行效率，所以设置为False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)


def init_redis(app):
    '''
    加载redis
    :param app:
    :return:
    '''
    app.config['REDIS_HOST'] = config.REDIS['HOST']
    app.config['REDIS_PORT'] = config.REDIS['PORT']
    app.config['REDIS_DB'] = config.REDIS['DB']
    app.config['REDIS_PWD'] = config.REDIS['PASSWD']
    app.config['REDIS_EXPIRE'] = config.REDIS['EXPIRE']


app = create_app()


@app.errorhandler(Exception)
def handle_error(err):
    """自定义处理错误方法"""
    # 这个函数的返回值会是前端用户看到的最终结果
    try:
        if err.code == 404:
            app.logger.error(err)
            return jsonify(code=Code.NOT_FOUND.value, msg="服务器异常,404")
        elif err.code == 400:
            app.logger.error(err)
            return jsonify(code=Code.REQUEST_ERROR.value, msg="服务器异常,400")
        elif err.code == 500:
            app.logger.error(err)
            return jsonify(code=Code.INTERNAL_ERROR.value, msg="服务器异常,500")
        else:
            return jsonify(code=err.code, msg=f"服务器异常,{err.code}")
    except:
        return jsonify(code=Code.INTERNAL_ERROR.value, msg=f"服务器异常,{err}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
