"""
Django提供了自定义SIMPLE_TAG (同样的，自定义的tag也需要注册到setting.py中的app中，索性把整个包注册)
需要注意的是自定义的tag一定要建在app下的templatetags包下，否则会报错 xx is not a registered tag library. Must be one of:
使用自定功能的时候只需要在HTML页面中  在HTML顶部预加载｛%load py文件名%｝，然后 {{ blog_preview content reg}}
"""

"""
自定义还包括filter 使用自定filter的时候只需要在HTML页面中  在HTML顶部预加载｛%load py文件名%｝，然后 {{ content | blog_preview: 'reg'}}
"""
from django import template
from django.utils.safestring import mark_safe

# 创建一个library对象，再这个对象上注册，对象名是关键字，不能改动,只有向系统注册过的tags，系统才认得你。
register = template.Library()


# 博客评论树tag
# 这个装饰器表明这个函数是一个模板标签，@register.simple_tag(takes_context=True) takes_context = True 表示接收上下文对象，就是前面所说的封装了各种变量的 Context 对象。
@register.simple_tag  # 加上这句后我就是一名合格的template tags
def comment_tree(comments):
    root_comment_html = ''
    for comment in comments:
        html = '<div class="pui-comment pui-comment-avatar-left pui-unbordered"><div class="pui-comment-avatar">'
        html += '<img src="images/2.png" class="pui-img-circle pui-img-xs"/><p>'
        html += comment['commentUser']
        html += '</p></div>'
        html += '<div class="pui-comment-container"> <div class="pui-comment-main pui-comment-arrow-lt"><header class="pui-comment-header">'
        html += '<div class="pui-comment-title-right"> #1楼 <a href="javascript:;">赞(18)</a> <a href="javascript:;">反对(0)</a>'
        html += '</div>'
        html += '<div class="pui-comment-subtitle">评论于'
        html += comment['commentDate']
        html += '</div>'
        html += '</header>'
        html += '<section class="pui-comment-content">'
        html += comment['commentContent']
        html += '</section>'
        html += '<div class="pui-comment-foot"><a href="javascript:;" class="reply_button">回复</a><ahref="">顶</a><a href="javascript:;">举报</a>'
        html += ' <form action="" class="commitReplyForm" style="display: none;">'
        html += ' <div class="pui-form-group">'
        html += '<textarea name="commentContent" class="pui-input-border-default"></textarea>'
        html += '<input value="{{ blog.id }}" name="commentBlog" style="display: none">'
        html += '<input value="{{ comment.id }}" name="reply" style="display: none">'
        html += '<div class="pui-form-group"><input type="button" value="提交" class="pui-btn pui-btn-primary comment_button"/></div>'
        html += '</div>'
        html += '</form>'
        html += '</div>'
        html += '</div>'

        html += recursion(comment['children'])

        html += '</div>'
        html += '</div>'

        root_comment_html += html
    return mark_safe(root_comment_html)


# 评论回复
@register.simple_tag
def recursion(comment_reply_list):
    leaf_comment_html = ''
    for reply in comment_reply_list:

        leaf_html = ' <div class="pui-comment-reply"><div class="pui-comment pui-comment-avatar-left"><div class="pui-comment-arrow"><span></span></div><div class="pui-comment-avatar">'
        leaf_html += '<img src="images/3.jpg" class="pui-img-circle pui-img-xs"/><p>'
        leaf_html += reply['commentUser']
        leaf_html += '</p> </div>'
        leaf_html += '<div class="pui-comment-container"> <header class="pui-comment-header"><div class="pui-comment-title-right">'
        leaf_html += ' #1楼-2 <a href="javascript:;">赞(1)</a> <a href="javascript:;">反对(18)</a>'
        leaf_html += '</div><div class="pui-comment-subtitle"><a href="javascript:;" class="pui-link">@某某某</a> <span class="pui-comment-reply-time">回复于2014-7-12 15:30</span></div></header>'
        leaf_html += '<section class="pui-comment-content"><blockquote>介就是回复的内容....</blockquote><p>%s</p></section>' %(reply['commentContent'])
        leaf_html += '<footer class="pui-comment-foot"><a href="javascript:;">回复</a><a href="">顶</a><a href="javascript:;">举报</a></footer>'
        leaf_html += '</div>'
        leaf_html += '</div>'
        leaf_html += '</div>'
        leaf_html += recursion(reply['children'])

        leaf_comment_html += leaf_html

    return leaf_comment_html


# 首页博客预览
@register.filter
def blog_preview(content):
    return '这是预览'
