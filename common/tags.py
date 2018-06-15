"""
Django提供了自定义SIMPLE_TAG (同样的，自定义的tag也需要注册到setting.py中的app中，索性把整个包注册)
使用自定功能的时候只需要在HTML页面中  在HTML顶部预加载｛%load py文件名%｝，然后 {{ blog_preview content reg}}
"""

"""
自定义还包括filter 使用自定filter的时候只需要在HTML页面中  在HTML顶部预加载｛%load py文件名%｝，然后 {{ content | blog_preview: 'reg'}}
"""
from django import template
from django.utils.safestring import mark_safe

# 创建一个library对象，再这个对象上注册，对象名是关键字，不能改动
register = template.Library()


# 博客评论树tag
@register.simple_tag
def comment_tree(comments):
    for comment in comments:
       html = '<div class="pui-comment pui-comment-avatar-left pui-unbordered"><div class="pui-comment-avatar">'
       html +=


# 首页博客预览
@register.filter
def blog_preview(content):
    return '这是预览'
