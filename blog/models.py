# -*-coding:utf-8-*-
from django.db import models

from user.models import User


class Blog(models.Model):
    class Meta:
        db_table = "blog_info"
        verbose_name_plural = "博客信息表"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, verbose_name="博客标题")  # 博客标题
    content = models.TextField(verbose_name="博客正文")  # 博客正文
    type = models.CharField(verbose_name="博客分类")
    classification = models.ForeignKey(BlogClassification, verbose_name="博客类型")
    createUser = models.ForeignKey(User)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    class Meta:
        db_table = "blog_info"
        verbose_name_plural = "博客评论表"

    id = models.AutoField(primary_key=True)
    commentContent = models.CharField(max_length=255, verbose_name="评论内容")
    commentBlog = models.ManyToManyField(Blog, verbose_name="被评论博客")
    commentUser = models.ManyToManyField(User, verbose_name="评论人")
    commentDate = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")


class BlogCollect(models.Model):
    class Meta:
        db_table = "blog_collect"
        verbose_name_plural = "博客收藏表"

    id = models.AutoField(primary_key=True)
    collectBlog = models.ManyToManyField(Blog, verbose_name="被收藏博客")
    collectUser = models.ManyToManyField(User, verbose_name="收藏人")
    collectBlogDate = models.DateField(auto_now_add=True, verbose_name="收藏时间")


class BlogType(models.Model):
    class Meta:
        db_table = "blog_type"
        verbose_name_plural = "博客类型"

    id = models.AutoField(primary_key=True)
    type_list = (
        (0, '原创')
        (1, '转载')
        (2, '翻译')
    )
    name = models.CharField(choices=type_list, blank=True, null=True, verbose_name="类型分类名称")


class BlogClassification(models.Model):
    class Meta:
        db_table = "blog_classification"
        verbose_name_plural = "博客分类"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="博客分类名称")
    createDate = models.DateField(auto_now_add=True, verbose_name="创建时间")
