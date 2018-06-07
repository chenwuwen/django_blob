'''装饰器'''

from django.shortcuts import render, redirect
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler

# 验证Session是否存在的装饰器
from django_blog.settings import BASE_DIR


def auth(func):
    def inner(request, *args, **kwargs):
        user = request.session['user']
        if not user:
            return redirect('/user/login')
        return func(request, *args, **kwargs)

    return inner



#带参数的装饰器需要2层装饰器实现,第一层传参数，第二层传函数，每层函数在上一层返回
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
