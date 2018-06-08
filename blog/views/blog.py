# -*-coding:utf-8-*-
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from blog.models import Blog, BlogClassification, BlogTag
from blog.validform import BlogForm
from common.utils.json_util import JsonCustomEncoder
from common.utils.response import BaseResponse
from user.models import User

"""
关于Django通过主键进行查询：
每一个Django模型类都有一个主键字段(ID)，它用来维护模型对象的唯一性。Django提供了一个pk字段来代表它，我们可以通过它来完成相应的查询。比如下面的例子：
>>> Blog.objects.get(id__exact=14) # 通过明确声明ID字段的方式获得一个Blog对象
>>> Blog.objects.get(id=14) # 通过ID字段获得Blog对象，但是使用确实的__exact
>>> Blog.objects.get(pk=14) # 这里的pk就相当于id__exact
pk也支持其它除了__exact的操作，比如：
# 获得ID值为1,3,9的Blog对象集合  
>>> Blog.objects.filter(pk__in=[1,3,9])  
# 获得所有ID值大于18的Blog对象集合  
>>> Blog.objects.filter(pk__gt=18)  
pk字段同样也支持跨模型的查询，比如下面的三种写法，效果是一样的，都是表示查找所有Blog的ID为1的Entry集合：
>>> Entry.objects.filter(blog__id__exact=1) # 显示的使用__exact  
>>> Entry.objects.filter(blog__id=1) # 隐含的使用__exact  
>>> Entry.objects.filter(blog__pk=1) # __pk 相当于 __id__exact
"""


# 阅读博客
class ReadBlog(View):
    def get(self, request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        comment_list = blog.blogcomment_set.add()
        return render(request, "blog/view.html", {'blog': blog, 'comment_list': comment_list})


# 写博客
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
        response = BaseResponse()
        if ret:
            blog = result.cleaned_data
            Blog.objects.create(blog)
            response.status = True
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')
        else:
            response.message(result.errors.as_json())
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')
