# -*-coding:utf-8-*-
from django.shortcuts import render
from django.views import View

from user.views.login import auth


@auth
class ReadBlog(View):
    def get(self, request):
        return render(request, "blog/view.html")


@auth
class WriteBlog(View):
    def get(self, request):
        return render(request, "blog/view.html")

    def post(self, request):
        pass
