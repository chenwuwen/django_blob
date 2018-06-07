# -*-coding:utf-8-*-
from django.shortcuts import render
from django.views import View

from blog.models import Blog, BlogClassification, BlogTag
from blog.validform import BlogForm
from user.models import User


class ReadBlog(View):
    def get(self, request):
        return render(request, "blog/view.html")


class WriteBlog(View):
    def get(self, request):
        blog_classification_list = BlogClassification.objects.all()
        # 反向查询（需要先获取主表的对象,在进行反向查找）下面操作如下：
        # user = request.session['user']  #主表的对象可以从session获取(需要设置session的时候保存的是对象),也可以为数据库查询(但是必须是get()获取的单一查询 ,使用filter（），excute（）等获取的是查询集集合不能用此方法)
        # 注意：blogtag_set为小写（首字母和中间的都要小写
        # blog_tag_list = user.blogtag_set.all()
        blog_tag_list = request.session['user'].blogtag_set.all()
        return render(request, "blog/write_blog.html",
                      {'blog_classification_list': blog_classification_list, 'blog_tag_list': blog_tag_list}
                      )

    def post(self, request):
        result = BlogForm(request.POST)
        ret = result.is_valid()
        if ret:
            blog = result.cleaned_data
            Blog.objects.create(blog)
