# -*-coding:utf-8-*-

"""
根据Model生成数据库表命令，首先在setting.py中的INSTALLED_APPS 加入你的 app
使用命令  python manage.py makemigrations + "app名称"  （有几个app，就使用几次命令）
上述执行完成之后 使用命令 python manage.py migrate 就可以生成表了，生成的表 是上面命令加入的app中的表

"""
"""
有时在django的Model定义中，会出现引用一个未定义Model的情况,例如：
classification = models.ForeignKey(BlogClassification, verbose_name="博客类型")  NameError: name 'BlogClassification' is not defined
解决方法：将ForeignKey引用的Model改为字符串即可

在Django2.0之后定义Model外键关联可能会报错： __init__() missing 1 required positional argument: 'on_delete'
原因：在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错
"""

"""
ForeignKey()中的参数：
- to="表名"
- to_field="列名" #建立外键关系的列名，默认是id列
- related_query_name="自定义名" #定义一个反向操作的名称,保留了反向连表操作中_set的属性
- related_name="自定义名" #定义一个反向操作的名称，直接通过自定义名即可反向操作
related_query_name和related_name都是定义的反向操作的属性，一般常用于related_name.
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
    classification = models.OneToOneField(to='BlogClassification', to_field='id', max_length=20, verbose_name="博客类型",
                                          on_delete="CASCADE")
    createUser = models.ForeignKey(to='user.User', to_field='id', verbose_name="创建人", on_delete="CASCADE",
                                   max_length=20)
    open = models.IntegerField(verbose_name="是否私有文章,1:否，0:是")
    valid = models.IntegerField(verbose_name="文章是否有效,0:审核中,1:审核通过,2:审核不通过,3:文章被删除,4:当前文章是草稿")
    createDate = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    class Meta:
        db_table = "blog_comment"
        verbose_name_plural = "博客评论表"

    id = models.AutoField(primary_key=True)
    commentContent = models.CharField(max_length=255, verbose_name="评论内容")
    commentBlog = models.ManyToManyField(to='Blog', verbose_name="被评论博客", max_length=20)
    commentUser = models.ManyToManyField(to='user.User', verbose_name="评论人", max_length=20)
    commentDate = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    reply = models.ForeignKey(to='self', to_field='id', verbose_name="回复ID", on_delete="CASCADE", null=True)


class BlogCollect(models.Model):
    class Meta:
        db_table = "blog_collect"
        verbose_name_plural = "博客收藏表"

    id = models.AutoField(primary_key=True)
    collectBlog = models.ManyToManyField(to='Blog', verbose_name="被收藏博客", max_length=20)
    collectUser = models.ManyToManyField(to='user.User', verbose_name="收藏人", max_length=20)
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
    name = models.IntegerField(choices=type_list, blank=True, null=True, verbose_name="类型分类名称")


class BlogClassification(models.Model):
    class Meta:
        db_table = "blog_classification"
        verbose_name_plural = "博客分类"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="博客分类名称", max_length=20)
    createDate = models.DateField(auto_now_add=True, verbose_name="创建时间")


class BlogTag(models.Model):
    class Meta:
        db_table = "blog_tag"
        verbose_name_plural = "博客标签"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="标签名", max_length=20)
    createUser = models.ForeignKey(to='user.User', to_field='id', verbose_name="创建人", on_delete="CASCADE")
    createDate = models.DateField(auto_now_add=True, verbose_name="创建时间")
