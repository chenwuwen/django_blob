'''装饰器'''
"""
通常情况，使用 函数定义的view,可以使用如下定义的装饰器(即:在方法名上添加 @装饰器)
但是如果使用类定义的view，是不能够直接使用如下定义的装饰器进行装饰的(而是需要在被装饰的类的方法上添加 @method_decorator(装饰器名称))

"""
import json

from django.shortcuts import render, redirect
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler

# 验证Session是否存在的装饰器
from common.utils.response import BaseResponse
from django_blog.settings import BASE_DIR, LOGIN_URL


# 重定向装饰器
def auth(func):
    def inner(request, *args, **kwargs):  # 对于装饰的方法或者类的参数数量问题，*args, **kwargs即可满足所有参数类型
        try:
            user = request.session['user']
            if not user:
                return redirect(LOGIN_URL)
        except Exception as e:
            print(e)
            return redirect(LOGIN_URL)
        return func(request, *args, **kwargs)

    return inner


# json权限验证装饰器
def auth_json(func):
    def inner(self, *args, **kwargs):
        if not self.session['user']:
            rep = BaseResponse()
            rep.summary = "未登录"
            self.write(json.dumps(rep.__dict__))
            return
        func(self, *args, **kwargs)

    return inner


# 带参数的装饰器需要2层装饰器实现,第一层传参数，第二层传函数，每层函数在上一层返回
def logger():
    def outter(func):
        def inner(*args, **kwargs):
            logFilePath = BASE_DIR.join("logger/blog.log")
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            # 日志按日期滚动，保留5天
            handler = TimedRotatingFileHandler(logFilePath, when="d", interval=1, backupCount=5)
            formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            try:
                result = func(*args, **kwargs)
                logger.info(result)
            except Exception as e:
                print(e)
                logger.error(traceback.format_exc())

        return inner

    return outter
