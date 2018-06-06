# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2018-04-14 17:36:03
# @Last Modified by:   Marte
# @Last Modified time: 2018-04-14 18:39:21

import io

from django.shortcuts import HttpResponse

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
