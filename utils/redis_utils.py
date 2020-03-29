# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Huguodong
@Version        :  
------------------------------------
@File           :  redis_utils.py
@Description    :  封装redis类
@CreateTime     :  2020/3/23 22:04
------------------------------------
@ModifyTime     :  
"""
import pickle

import redis
from flask import current_app as app


class Redis(object):
    """
    redis数据库操作
    """

    @staticmethod
    def _get_r():
        host = app.config['REDIS_HOST']
        port = app.config['REDIS_PORT']
        db = app.config['REDIS_DB']
        passwd = app.config['REDIS_PWD']
        r = redis.StrictRedis(host=host, port=port, db=db, password=passwd)
        return r

    @classmethod
    def write(self, key, value, expire=None):
        """
        写入键值对
        """
        # 判断是否有过期时间，没有就设置默认值
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = app.config['REDIS_EXPIRE']
        r = self._get_r()
        r.set(key, value, ex=expire_in_seconds)

    @classmethod
    def write_dict(self, key, value, expire=None):
        '''
        将内存数据二进制通过序列号转为文本流，再存入redis
        '''
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = app.config['REDIS_EXPIRE']
        r = self._get_r()
        r.set(pickle.dumps(key), pickle.dumps(value), ex=expire_in_seconds)

    @classmethod
    def read_dict(self, key):
        '''
        将文本流从redis中读取并反序列化，返回
        '''
        r = self._get_r()
        data = r.get(pickle.dumps(key))
        if data is None:
            return None
        return pickle.loads(data)

    @classmethod
    def read(self, key):
        """
        读取键值对内容
        """
        r = self._get_r()
        value = r.get(key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hset(self, name, key, value):
        """
        写入hash表
        """
        r = self._get_r()
        r.hset(name, key, value)

    @classmethod
    def hmset(self, key, *value):
        """
        读取指定hash表的所有给定字段的值
        """
        r = self._get_r()
        value = r.hmset(key, *value)
        return value

    @classmethod
    def hget(self, name, key):
        """
        读取指定hash表的键值
        """
        r = self._get_r()
        value = r.hget(name, key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hgetall(self, name):
        """
        获取指定hash表所有的值
        """
        r = self._get_r()
        return r.hgetall(name)

    @classmethod
    def delete(self, *names):
        """
        删除一个或者多个
        """
        r = self._get_r()
        r.delete(*names)

    @classmethod
    def hdel(self, name, key):
        """
		删除指定hash表的键值
        """
        r = self._get_r()
        r.hdel(name, key)

    @classmethod
    def expire(self, name, expire=None):
        """
        设置过期时间
        """
        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = app.config['REDIS_EXPIRE']
        r = self._get_r()
        r.expire(name, expire_in_seconds)
