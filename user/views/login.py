from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.views import View

from user.validform import LoginForm


def test(request):
    return HttpResponse('人生苦短，我用Python')


'''如果用户名密码验证通过，这里做了两件事，第一，页面跳转到index；
第二，保存session；request.session['user'] = u这一步就是django提供的session保存功能，它实际做了两件事，
生成一个随机码放到本地，然后将这个随机码写入到浏览器的cookie里，
下次浏览器访问会将cookie里的这个随机码发送给服务端比对.django的session可以保存在数据库、缓存、文件里，
默认是保存在数据库的django_session表里.如果是新建的app，默认是没有表的，需要
“python manage.py makemigrations；python manage.py migrate”生成默认表
'''


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
        return render(request, 'login.html', {})

    def post(self, request):
        result = LoginForm(request.POST)

        # 如果所有规则都满足，则ret为true，只要有一条不满足，ret就为false。
        ret = result.is_valid()
        # 在此我注释以下代码是因为我在from表单进行校验时,删除了数据中的 验证码的key，在此获取用户输入的信息的时候，会报找不到key的错误
        # result.clean()  # 就是获取到的用户输入信息,但必须放在is_valid方法后,否则报object has no attribute 'cleaned_data'异常
        # data = result.clean()
        # print(data)
        if ret:
            # user = result.cleaned_data
            user = result.cleaned_data
            # print("登陆成功，当前登陆人是：", user.__dict__['username'])
            print("登陆成功，当前登陆人是：", user['username'])
            request.session['user'] = user
            return redirect("/blog/index/")
        else:  # result.errors，获取错误信息
            print(result.errors)
            return render(request, "login.html", {'err': result.errors})


# 验证Session是否存在的装饰器
def auth(func):
    def inner(request, *args, **kwargs):
        user = request.session.get('user', None)
        if not user:
            return redirect('/session_login/')
        return func(request, *args, **kwargs)

    return inner


# 注销
@auth
def session_logout(request):
    # 删除session
    del request.session['user']
    return redirect('/session_login/')
