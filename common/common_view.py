# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2018-04-14 17:36:03
# @Last Modified by:   Marte
# @Last Modified time: 2018-04-14 18:39:21

import io
import time
from datetime import date

from django.shortcuts import HttpResponse
import json
from common.utils import check_code as CheckCode

'''
获取验证码
'''


def getCheckCode(request):
    stream = io.BytesIO()
    # 创建随机字符 code
    # 创建一张图片格式的字符串，将随机字符串写到图片上
    img, code = CheckCode.create_validate_code()
    img.save(stream, 'png')
    # 创建随机字符 code
    # 创建一张图片格式的字符串，将随机字符串写到图片上
    request.session['CheckCode'] = code.lower()
    print('验证码是：', request.session['CheckCode'])
    return HttpResponse(stream.getvalue())


'''
consul健康检查,实际上直接返回UP的做法是不正确的,这个方法应该检测当前项目运行的情况(包括各个API是否正常(如timeout),
是否存在错误信息等等)而不是简单的只是检查这个API是否可以正常返回
'''


def health(request):
    now = int(time.time())
    print(f'时间：{now},consul检查本服务的健康状态')
    ret = 'UP'
    return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json,charset=utf-8")
