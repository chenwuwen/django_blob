import json

import time

from django.db.models import F
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
            if not result.cleaned_data['reply']:
                # 此处不能使用update,这也说明了为什么在使用update的时候,前面必须使用filter而不能使用get了,总结说从使用情境上看，update更加适用于批量数据更新，而save则更适合当然也只适合做单条记录的数据更新操作了,当然从SQL的执行情况来看,使用upate是要优于save方式的
                # blog.update(commentTotal=F('commentTotal') + 1)
                blog.commentTotal = blog.commentTotal + 1
                blog.save()
            response.status = True
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')
        else:
            response.message(result.errors.as_data())
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type='application/json')


# 获取评论,返回json格式评论
class getComment(View):
    def get(self, request, blog_id):
        response = BaseResponse()
        try:
            blog = Blog.objects.get(pk=blog_id)
            comment_query_set = BlogComment.objects.filter(commentBlog=blog)
            comment_query_list = transform_comment(comment_query_set)
            comment_tree = build_tree(comment_query_list)
            response.status = True
            response.data = comment_tree
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps(response.__dict__, ensure_ascii=False), content_type='application/json')


# 拼装 comment 数据
def build_tree(comment_query_list):
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
    return comment_tree


# 转换评论由query_set转换为 list 包含 字典
def transform_comment(comment_query_set):
    comment_query_list = []
    now = lambda: round(
        time.time())  # 默认是秒级的时间戳,获得毫秒级的时间戳 round(time.time() * 1000) 或者使用lambda表达式lambda: time.time()*1000 如果使用lambda表达式,那么使用now这个变量是需要加括号，也就是用 now() , round() 方法返回浮点数x的四舍五入值
    for comment_obj in comment_query_set:
        comment_dic = {}
        comment_dic['id'] = comment_obj.id
        comment_dic['commentContent'] = comment_obj.commentContent
        comment_dic['commentBlog'] = comment_obj.commentBlog.id
        comment_dic['commentUser'] = comment_obj.commentUser.username
        if (now() - round(time.mktime(comment_obj.commentDate.timetuple()))) < (
                        2 * 60 * 60):  # 判断回复时间与当前时间是否大于两个小时,mktime() 默认返回秒级的浮点数
            comment_dic['commentDate'] = '刚刚'
        else:
            comment_dic['commentDate'] = comment_obj.commentDate.strftime("%Y-%m-%d %H:%M")  # 日期转化为字符串
        if comment_obj.reply:  # 如果回复不为None
            comment_dic['reply_src_content'] = comment_obj.reply.commentContent
            comment_dic['reply_src_user'] = comment_obj.reply.commentUser.username
            comment_dic['reply'] = comment_obj.reply.id
        else:
            comment_dic['reply'] = comment_obj.reply
        comment_query_list.append(comment_dic)
    return comment_query_list
