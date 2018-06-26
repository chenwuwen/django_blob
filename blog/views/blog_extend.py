from django.db.models import F
from django.views import View

from blog.models import Blog


# 博客阅读量加1
class add_read_count(View):
    def get(self, request, blog_id):
        Blog.objects.get(pk=blog_id).update(readTotal=F('readTotal') + 1)


# 点赞量数量加1
class add_favor_count(View):
    def get(self, request, blog_id):
        Blog.objects.get(pk=blog_id).update(favorTotal=F('favorTotal') + 1)
