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

from blog.views import index, blog, comment, blog_extend

urlpatterns = [
    path('index/', index.Index.as_view()),
    path('read_blog/<int:blog_id>', blog.ReadBlog.as_view()),
    path('write_blog/', blog.WriteBlog.as_view()),
    path('commitComment/', comment.commitComment.as_view()),
    path('getComment/<int:blog_id>', comment.getComment.as_view()),
    path('add_read_count/<int:blog_id>', blog_extend.addReadCount.as_view()),
    path('add_favor_count/<int:blog_id>', blog_extend.addFavorCount.as_view()),

]
