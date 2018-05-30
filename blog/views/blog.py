# -*-coding:utf-8-*-
from django.shortcuts import render
from django.views import View

from user.views.login import auth


class ReadBlog(View):
    def get(self, request):
        return render(request, "blog/view.html")


class WriteBlog(View):
    def get(self, request):
        return render(request, "blog/write_blog.html")

    def post(self, request):
        pass
