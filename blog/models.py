# -*-coding:utf-8-*-
"""
有时在django的Model定义中，会出现引用一个未定义Model的情况,例如：
classification = models.ForeignKey(BlogClassification, verbose_name="博客类型")  NameError: name 'BlogClassification' is not defined
解决方法：将ForeignKey引用的Model改为字符串即可

在Django2.0之后定义Model外键关联可能会报错： __init__() missing 1 required positional argument: 'on_delete'
原因：在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错
"""
from django.db import models

from user.models import User


class Blog(models.Model):
    class Meta:
        db_table = "blog"
        verbose_name_plural = "博客表"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, verbose_name="博客标题")  # 博客标题
    content = models.TextField(verbose_name="博客正文")  # 博客正文
    type = models.CharField(verbose_name="博客分类", max_length=20)
    classification = models.OneToOneField('BlogClassification', max_length=20, verbose_name="博客类型", on_delete="CASCADE")
    createUser = models.ForeignKey('user.User', verbose_name="创建人", on_delete="CASCADE", max_length=20)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    class Meta:
        db_table = "blog_info"
        verbose_name_plural = "博客评论表"

    id = models.AutoField(primary_key=True)
    commentContent = models.CharField(max_length=255, verbose_name="评论内容")
    commentBlog = models.ManyToManyField('Blog', verbose_name="被评论博客")
    commentUser = models.ManyToManyField('user.User', verbose_name="评论人", max_length=20)
    commentDate = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")


class BlogCollect(models.Model):
    class Meta:
        db_table = "blog_collect"
        verbose_name_plural = "博客收藏表"

    id = models.AutoField(primary_key=True)
    collectBlog = models.ManyToManyField('Blog', verbose_name="被收藏博客")
    collectUser = models.ManyToManyField('user.User', verbose_name="收藏人", max_length=20)
    collectBlogDate = models.DateField(auto_now_add=True, verbose_name="收藏时间")


class BlogType(models.Model):
    class Meta:
        db_table = "blog_type"
        verbose_name_plural = "博客类型"

    id = models.AutoField(primary_key=True)
    type_list = (
        (0, '原创'),
        (1, '转载'),
        (2, '翻译'),
    )
    name = models.CharField(choices=type_list, max_length=20, blank=True, null=True, verbose_name="类型分类名称")


class BlogClassification(models.Model):
    class Meta:
        db_table = "blog_classification"
        verbose_name_plural = "博客分类"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="博客分类名称", max_length=20)
    createDate = models.DateField(auto_now_add=True, verbose_name="创建时间")
