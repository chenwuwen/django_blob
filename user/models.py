from django.db import models


# Create your models here.
class User(models.Model):
    class Meta:
        db_table = 'user'  # 指定数据表的名称
        verbose_name_plural = "用户表"  # 在admin管理页面显示表的名称,也可以使用verbose_name

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    age = models.IntegerField(verbose_name="年龄")
    sex = models.CharField(max_length=2, verbose_name="性别")
    createDate = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    email = models.EmailField(verbose_name="邮箱地址")

    # def __str__(self):
    #     return self.username
