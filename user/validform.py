# -*-coding:utf-8-*-
'''
http://www.cnblogs.com/wupeiqi/articles/6229414.html
http://www.cnblogs.com/wupeiqi/articles/6144178.html
'''
# Django2.0.2增删改都不需要再用models去调用了
import datetime

from django.core.exceptions import ValidationError
from django.forms import forms, fields
from user.models import *


# from django.db.modelsimports Q



# form类的运行顺序是init，clean，validte，save


# 登录验证form


class LoginForm(forms.Form):
    username = fields.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = fields.CharField(required=True, error_messages={'required': '密码不能为空'})
    vcode = fields.CharField(required=True, error_messages={'required': '验证码不能为空'})

    # 自定义方法（局部钩子(该from里有几个字段,就有几个局部钩子,当然自己也可以进行选择定义,方法名为 clean_(字段名))：当局部钩子抛出异常,如果自己不去捕获处理异常,则将异常抛出到页面）
    # def clean_username(self):
    #     value = self.cleaned_data['username']
    #     if value == 'root':
    #         return value
    #     else:
    #         raise ValidationError('这是自定义表单验证的一种方式(即:验证字段)...')

    # 自定义方法（全局钩子, 检验两个字段）
    def clean(self):
        # v0 = self.cleaned_data['vcode'].lower()
        # if v0 == self.request.session['CheckCode']:
        # print(type(self.cleaned_data))
        if 1:
            v1 = self.cleaned_data['username']
            v2 = self.cleaned_data['password']
            # 删除字典中vcode键,用以用户名密码在数据库查询
            self.cleaned_data.pop('vcode')
            print(self.cleaned_data)
            '''
            # 这里用了get,而不是filter,是因为filter查询出来的是一个QuerySet对象,而get是只取一个匹配的结果如果记录不存在的话，它会报错,如果Model类重写了_str_方法，则返回str方法里的返回值
            # user = User.objects.get(username=v1, password=v2)
            user = User.objects.get(**self.cleaned_data)
            if user:
                print("登陆from表单查询到数据-》", user)
                print("登陆from表单查询到数据-》", type(user))
                # 登陆成功，把查询到的对象放到cleaned_data中,view函数,将结果放到session中保存,由于get返回的是一个对象，可以通过__dict__来返回一个字典对象
                # 此处不设置,则返回的是用户输入的信息
                self.cleaned_data = user.__dict__
            else:
                # 抛出异常：就不走return self.cleaned_data 了，view函数就需要获取错误信息
                print(user)
                print("当前登陆用户：用户名密码不匹配")
                raise ValidationError('用户名或密码错误!!!')
            '''

            # 由于使用了get方法获取用户信息,由于get方法在获取不到记录时会抛出异常，所以不能使用 if判断而需要使用try/except/finally来捕获异常
            try:
                user = User.objects.get(**self.cleaned_data)
                print("登陆from表单查询到数据-》", user)
                print("登陆from表单查询到数据-》", type(user))
                # 登陆成功，把查询到的对象放到cleaned_data中,view函数,将结果放到session中保存,由于get返回的是一个对象，可以通过__dict__来返回一个字典对象
                # 此处不设置,则返回的是用户输入的信息
                # 当我试图将user的字典对象(即：user.__dict__)放进session的时候(此session是数据库保存的session),发现报错："Object of type 'ModelState' is not JSON serializable"
                # 而后我将session的保存位置放在内存中,没有报错,暂时没有想到为什么
                # self.cleaned_data = user
                self.cleaned_data = user.__dict__
            except Exception as e:
                # 抛出异常：就不走return self.cleaned_data 了，view函数就需要获取错误信息
                print(e)
                print("当前登陆用户：用户名密码不匹配")
                raise ValidationError('用户名或密码错误!!!')
            finally:
                print("时间：%s , 用户名：%s ,登陆系统" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), v1))

        else:
            raise ValidationError('验证码错误')
        return self.cleaned_data

        # 这个方法不能抛出异常,否则程序中断
        # def _post_clean(self):
        #     v0 = self.clean_data['vcode']
        #     if v0 == request.session['CheckCode']:
        #         v1 = self.cleaned_data['username']
        #         v2 = self.cleaned_data['password']
        #         if v1 == "root" and v2 == "1234":
        #             pass
        #         else:
        #             self.add_error("__all__", ValidationError('用户名或密码错误...'))
        #     else:
        #         self.add_error(None, ValidationError('验证码错误...'))


# 注册验证form
class RegisterForm(forms.Form):
    username = fields.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = fields.CharField(required=True, error_messages={'required': '密码不能为空'})
    confirmPassword = fields.CharField(required=True, error_messages={'required': '密码不能为空'})
    email = fields.EmailField(required=True, error_messages={'required': '密码不能为空', 'invalid': '邮箱格式错误'})
    vcode = fields.CharField(required=True, error_messages={'required': '验证码不能为空'})

    def clean(self):
        v0 = self.cleaned_data['vcode']
        v1 = self.cleaned_data['password']
        v2 = self.cleaned_data['confirmPassword']
        v3 = self.cleaned_data['email']

        # if v0==self.request.session('vcode').lower():
        if v0:
            self.cleaned_data.pop('vcode')
            self.cleaned_data.pop('confirmPassword')
            print(self.cleaned_data)
            if v1 == v2:
                # user = User(**self.cleaned_data)
                # user.save()
                User.objects.create(**self.cleaned_data)
            else:
                raise ValidationError('密码不一致')
        else:
            raise ValidationError('验证码错误')
        return self.cleaned_data
