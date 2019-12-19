"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import common
from apscheduler.schedulers.background import BackgroundScheduler

from common import consul_config

'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/',app1_views.test)
]
'''

urlpatterns = [
    path('', include('user.urls')),  # 只输入IP和端口时跳转到登录页
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('blog/', include('blog.urls')),
    path('remote/', include('remote.urls')),
    path('health/', common.common_view.health, name='health'),
]

# Django项目如果想在启动时自动执行某些方法? 需要注意的是两种只能取其一(本例中写一块会重复多执行一次)
'''
在 Django 2.1 中 views.py() 文件会在 Django 启动的时候执行一次
那么我们直接把 function_run() 丢在 views.py 文件中它应该就会跟随Django一块启动
切记不要加上 if name == ‘main’
既然能让脚本在 Django 启动的时候一块启动，那么我们就可以随心所欲的添加启动任务了。比如定时任务，让 Django 担任 MQTT 的客户端。。。。。。
注意：你的脚本/函数有可能会阻塞 Django 的进程。
'''

'''
另一种方法是使用定时执行库，如 APScheduler这样的一个库
https://www.jianshu.com/p/4f5305e220f0
'''

print("========Django启动了,我可以在Django启动后搞一些事情========")
consul_config.ConsulConf().register()

'''
使用APScheduler库
'''

# # 实例化定时器，固定格式
# scheduler = BackgroundScheduler()
# # 未指定时间，则会立即执行
# scheduler.add_job(print('@@@'))
# # 启动该脚本
# scheduler.start()
