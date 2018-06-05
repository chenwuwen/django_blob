from django.db import models

'''
http://www.cnblogs.com/wupeiqi/articles/6216618.html
'''
'''
Field 选项
null ：缺省设置为false.通常不将其用于字符型字段上，比如CharField,TextField上.字符型字段如果没有值会返回空字符串。
blank：该字段是否可以为空。如果为假，则必须有值
choices：一个用来选择值的2维元组。第一个值是实际存储的值，第二个用来方便进行选择。如SEX_CHOICES= ((‘F’,'Female’),(‘M’,'Male’),)
core：db_column，db_index 如果为真将为此字段创建索引
default：设定缺省值
editable：如果为假，admin模式下将不能改写。缺省为真
help_text：admin模式下帮助文档
primary_key：设置主键，如果没有设置django创建表时会自动加上：
'''


# Create your models here.
class User(models.Model):
    class Meta:
        db_table = 'user'  # 指定数据表的名称(默认是app名_表名)
        verbose_name_plural = "用户表"  # 在admin管理页面显示表的名称,也可以使用verbose_name

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField(verbose_name="年龄", blank=True, null=True, default=0)
    sex_list = (
        (1, "男"),
        (0, "女"),
    )
    sex = models.IntegerField(choices=sex_list, verbose_name="性别", blank=True, null=True)  # 以下拉框的形式在页面展示
    createDate = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    email = models.EmailField(verbose_name="邮箱地址")

    def __str__(self):
        return self.username
