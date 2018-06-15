# -*-coding:utf-8-*-
import json

import collections
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from blog.models import Blog, BlogClassification, SelfSort
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
        user = None
        try:
            user = request.session['user']
        except Exception as e:
            print("未登录")
            print(e)
        finally:
            pass
        comment_query_set = blog.blogcomment_set.all()
        # QuerySet转换为List有两种方法 1：values返回是字典列表[{},{}],2:values_list返回的是元组列表 [(),()] values_list加上 flat=True 之后返回值列表
        comment_query_list = blog.blogcomment_set.all().values()
        print(len(comment_query_set))
        comment_tree = []
        comment_list_dict = {}
        for row in comment_query_list:
            row.update({'children': []})
            comment_list_dict[row['id']] = row
        for item in comment_query_list:
            parent_row = comment_list_dict.get(item['reply'])
            if not parent_row:
                comment_tree.append(item)
            else:
                parent_row['children'].append(item)
        comment_dic, comment_count = build_tree(comment_query_set)
        return render(request, "blog/view.html",
                      {'blog': blog, 'comment_count': comment_count, 'comment_dic': comment_dic, 'user': user})


# 写博客
class WriteBlog(View):
    def get(self, request):
        blog_classification_list = BlogClassification.objects.all()
        # 反向查询（需要先获取主表的对象,在进行反向查找）下面操作如下：
        # user = request.session['user']  #主表的对象可以从session获取(需要设置session的时候保存的是对象),也可以为数据库查询(但是必须是get()获取的单一查询 ,使用filter（），excute（）等获取的是查询集集合不能用此方法)
        # 注意：blogtag_set为小写（首字母和中间的都要小写
        # blog_tag_list = user.blogtag_set.all()
        self_sort_list = request.session['user'].selfsort_set.all()
        return render(request, "blog/write_blog.html",
                      {'blog_classification_list': blog_classification_list, 'self_sort_list': self_sort_list}
                      )

    def post(self, request):
        result = BlogForm(request.POST)
        ret = result.is_valid()
        response = BaseResponse()
        if ret:
            classification_id = result.cleaned_data['classification']
            classification = BlogClassification.objects.get(pk=classification_id)
            result.cleaned_data['classification'] = classification
            result.cleaned_data['createUser'] = request.session['user']
            Blog.objects.create(**result.cleaned_data)
            response.status = True
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')
        else:
            response.message(result.errors.as_json())
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')

"""
博客评论中,有评论和回复,可以使用递归来处理,先把数据通过有序字典(即：collections.OrderedDict()),key为对象,value为有序字典,依次类推!

"""

def tree_search(comment_dic, comment_obj):
    # 在comment_dic中一个一个的寻找其回复的评论
    # 检查当前评论的 reply_id 和 comment_dic中已有评论的nid是否相同，
    # 如果相同，表示就是回复的此信息
    # 如果不同，则需要去 comment_dic 的所有子元素中寻找，一直找，如果一系列中未找，则继续向下找
    for k, v in comment_dic.items():
        # 找回复的评论，将自己添加到其对应的字典中，例如： {评论一： {回复一：{},回复二：{}}} 这里没有使用comment_obj.reply是因为comment_obj.reply也是一个BlogComment对象实例
        if k.id == comment_obj.reply.id:
            comment_dic[k][comment_obj] = collections.OrderedDict()
            print(comment_dic)
            return
        else:
            # 在当前第一个根元素中递归的去寻找父亲
            tree_search(comment_dic[k], comment_obj)


def build_tree(comment_query_set):
    # 字典是无序的,但是collections的OrderedDict类为我们提供了一个有序的字典结构(它记录了每个键值对添加的顺序,但是如果初始化的时候同时传入多个参数，它们的顺序是随机的，不会按照位置顺序存储）
    comment_dic = collections.OrderedDict()
    comment_count = 0
    for comment_obj in comment_query_set:
        if comment_obj.reply is None:
            comment_count += 1
            # 如果是根评论，添加到comment_dic[评论对象] ＝ {}
            comment_dic[comment_obj] = collections.OrderedDict()
            print(comment_dic)
        else:
            # 如果是回复的评论，则需要在 comment_dic 中找到其回复的评论
            tree_search(comment_dic, comment_obj)
    return comment_dic, comment_count,
