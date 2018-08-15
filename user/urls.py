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
from django.urls import path

from common import common_view
from user.views import login

urlpatterns = [
    path('', login.Login.as_view(), name='login'),  # 只输入IP和端口时跳转到登录页
    path('login/', login.Login.as_view(), name='login'),
    path('logout/', login.logout, name='logout'),
    path('register/', login.Register.as_view(), name='register'),
    path('check_code/', common_view.getCheckCode, name='check_code'),
    path('valid_username/', login.valid_username, name='valid_username'),

]
