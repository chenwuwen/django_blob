import json
from django.db.models import F
from django.http import HttpResponse
from django.views import View

from blog.models import Blog

# 博客阅读量加1
from common.utils.response import BaseResponse


class addReadCount(View):
    def get(self, request, blog_id):
        response = BaseResponse()
        try:
            # update更新时不能使用get方法会报错（'Blog' object has no attribute 'update'）使用filter方法
            Blog.objects.filter(pk=blog_id).update(readTotal=F('readTotal') + 1)
            response.status = True
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps(response.__dict__), content_type="application/json")


# 点赞量数量加1
class addFavorCount(View):
    def get(self, request, blog_id):
        response = BaseResponse()
        try:
            Blog.objects.filter(pk=blog_id).update(favorTotal=F('favorTotal') + 1)
            response.status = True
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps(response.__dict__), content_type="application/json")
