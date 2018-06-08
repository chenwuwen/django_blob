import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.views import View

from common.decorators import auth
from common.utils.json_util import JsonCustomEncoder
from common.utils.response import BaseResponse
from user.models import User
from user.validform import RegisterForm, LoginForm


def test(request):
    return HttpResponse('人生苦短，我用Python')


'''如果用户名密码验证通过，这里做了两件事，第一，页面跳转到index；
第二，保存session；request.session['user'] = u这一步就是django提供的session保存功能，它实际做了两件事，
生成一个随机码放到本地，然后将这个随机码写入到浏览器的cookie里，
下次浏览器访问会将cookie里的这个随机码发送给服务端比对.django的session可以保存在数据库、缓存、文件里，
默认是保存在数据库的django_session表里.如果是新建的app，默认是没有表的，需要
“python manage.py makemigrations；python manage.py migrate”生成默认表
'''


# 登录
class Login(View):  # 这里需要注意，使用CBV必须继承View类


    def dispatch(self, request, *args, **kwargs):
        # 调用父类中的dispatch
        print('before')  # 类似装饰器的功能,这个地方更像java servlet过滤器,但并不是,Django中的中间件更像是
        result = super(Login, self).dispatch(request, *args, **kwargs)
        print('after')  # 类似装饰器的功能
        return result

    # 根据请求头中的request method进行自动执行get和post,而不必像使用FBV那样就是判断了,是GET还是POST请求了
    def get(self, request):
        print(request)
        print(request.method)
        return render(request, 'login.html')

    def post(self, request):

        remember_me = request.POST.get('rememberMe')

        result = LoginForm(request.POST)

        vcode = request.session['CheckCode']

        # 如果所有规则都满足，则ret为true，只要有一条不满足，ret就为false。
        ret = result.is_valid()
        # 在此我注释以下代码是因为我在from表单进行校验时,删除了数据中的 验证码的key，在此获取用户输入的信息的时候，会报找不到key的错误
        # result.clean()  # 就是获取到的用户输入信息,但必须放在is_valid方法后,否则报object has no attribute 'cleaned_data'异常
        # data = result.clean()
        # print(data)
        if ret:
            user = result.cleaned_data
            # print("登陆成功，当前登陆人是：", user.__dict__['username'])
            print("登陆成功，当前登陆人是：", user['username'])
            # request.session['user'] = user   #这个地方保存的session只是一个字典对象(而且这个字典对象内的key跟实体对象的字段也不一致,不能用来做数据库过滤条件),不能用于反向查询
            request.session['user'] = User.objects.get(username=user['username'])
            if remember_me:  # 记住我,设定过期时间在1个月之后
                request.session.set_expiry(2592000)
            # return redirect("/blog/index/")
            response = BaseResponse()
            response.status = True
            # 通过dumps()方法中的cls函数,添加自定义的处理函数
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type="application/json")
        else:
            # form.errors: 获取错误信息,表单的错误以字典形式返回(如果有多个错误, 可以循环这个字典, 然后传给前端)
            print(result)
            print(result.errors)
            print(result.errors.as_json())
            # return render(request, "login.html", {'err': result})
            response = BaseResponse()
            response.message = result.errors.as_json()
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type="application/json")


# 注册（返回统一为json，提示注册成功，重新登录）
class Register(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):

        result = RegisterForm(request.POST)
        ret = result.is_valid()
        response = BaseResponse()
        if ret:
            response.status = True
            return HttpResponse(json.dumps(response.__dict__), content_type="application/json")
        else:
            # 错误返回json
            print(result.errors)
            error = result.errors.as_json()
            # error = result.errors.as_data()
            response.message = result.errors.as_json()
            return HttpResponse(json.dumps(response.__dict__), content_type="application/json")


# 验证用户名
def valid_username(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        users = User.objects.filter(username=username)
        # https://code.ziqiangxuetang.com/django/django-queryset-api.html
        response = BaseResponse()
        if not users.exists():
            response.status = True
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type="application/json")
        else:
            response.summary = '用户名已存在'
            return HttpResponse(json.dumps(response.__dict__, cls=JsonCustomEncoder), content_type="application/json")


# 校验邮箱
def valid_email(request):
    if request.method == 'GET':
        email = User.objects.filter(email=request.GET.get('email')).count()
        if not email:
            pass
        else:
            BaseResponse.summary = '邮箱已存在'
            return HttpResponse(json.dumps(BaseResponse, cls=JsonCustomEncoder), content_type="application/json")


# 注销
@auth
def logout(request):
    # 删除session
    del request.session['user']
    return redirect('/user/login/')
