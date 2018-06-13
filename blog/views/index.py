# -*-coding:utf-8-*-
from django.shortcuts import render
from django.views import View

from blog.models import Blog


class Index(View):
    def get(self, request):
        user = request.session['user']
        blog_list = Blog.objects.all()
        return render(request, "index.html", {'user': user,'blog_list':blog_list})


