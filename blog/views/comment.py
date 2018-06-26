import json

from django.http import HttpResponse
from django.views import View

from blog.models import Blog, BlogComment
from blog.validform import CommentForm
from common.utils.json_util import JsonCustomEncoder
from common.utils.response import BaseResponse


# 评论博客（提交）
class commitComment(View):
    def get(self):
        pass

    def post(self, request):
        result = CommentForm(request.POST)
        ret = result.is_valid()
        response = BaseResponse()
        if ret:
            blog_id = result.cleaned_data['commentBlog']
            blog = Blog.objects.get(pk=blog_id)
            user = request.session['user']
            result.cleaned_data['commentBlog'] = blog
            result.cleaned_data['commentUser'] = user
            BlogComment.objects.create(**result.cleaned_data)
            response.status = True
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')
        else:
            response.message(result.errors.as_data())
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')
