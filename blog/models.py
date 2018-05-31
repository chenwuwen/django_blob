# -*-coding:utf-8-*-
from django.db import models

from user.models import User


class BlogInfo(models.Model):
    class Meta:
        db_table = "blog_info"
        verbose_name_plural = "博客信息表"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, verbose_name="博客标题")  # 博客标题
    content = models.TextField(verbose_name="博客正文")  # 博客正文
    createUser = models.ForeignKey(User)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


class BlogComment(models.Model):
    class Meta:
        db_table = "blog_info"
        verbose_name_plural = "博客评论表"

    id = models.AutoField(primary_key=True)
    commentBlog = models.ManyToManyField(max_length=150, verbose_name="被评论博客")
    commentUser = models.ManyToManyField(verbose_name="评论人")  # 博客正文
    createUser = models.ForeignKey(User)
    commentDate = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
