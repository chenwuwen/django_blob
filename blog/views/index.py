# -*-coding:utf-8-*-
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from blog.models import Blog
from common.decorators import auth


class Index(View):
    @method_decorator(auth)
    def get(self, request):
        user = request.session['user']
        blog_list = Blog.objects.all()
        return render(request, "index.html", {'user': user, 'blog_list': blog_list})
