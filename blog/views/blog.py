# -*-coding:utf-8-*-
from django.shortcuts import render
from django.views import View

from blog.models import Blog
from blog.validform import BlogForm


class ReadBlog(View):
    def get(self, request):
        return render(request, "blog/view.html")


class WriteBlog(View):
    def get(self, request):
        return render(request, "blog/write_blog.html")

    def post(self, request):
        result = BlogForm(request.POST)
        ret = result.is_valid()
        if ret:
            blog = self.cleaned_data
            Blog.objects.create(blog)
