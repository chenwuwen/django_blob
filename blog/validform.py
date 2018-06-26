from django import forms
from django.core.exceptions import ValidationError

# 博客表单验证
from blog.models import BlogClassification, BlogComment


class BlogForm(forms.Form):
    title = forms.CharField(required=True, error_messages={'required': '标题不能为空'})
    content = forms.CharField(required=True, error_messages={'required': '内容不能为空'})
    classification = forms.IntegerField(required=True, error_messages={'required': '该博客类型不存在'})

    def clean_content(self):
        content = self.cleaned_data['content']
        # 检测是否含有敏感字classification
        # todo
        return self.cleaned_data['content']

    def clean_title(self):
        title = self.cleaned_data['title']
        result = "标题" in title
        if result:
            raise ValidationError(message='文章标题不合法', code='invalid')
        return self.cleaned_data['title']

    def clean_classification(self):
        try:
            classification_id = self.cleaned_data['classification']
            BlogClassification.objects.get(pk=classification_id)
            return self.cleaned_data['classification']
        except Exception as e:
            print(e)
            raise ValidationError(message='文章分类不存在', code='invalid')
        finally:
            pass


# 表单评论验证
class CommentForm(forms.Form):
    commentContent = forms.CharField(required=True, error_messages={'required': '评论内容不能为空'})
    commentBlog = forms.IntegerField(required=True, error_messages={'required': '评论博客无效'})
    reply = forms.IntegerField(required=False)

    def clean_commentContent(self):
        commentContent = self.cleaned_data['commentContent']
        ret = "标题" in commentContent
        if ret:
            raise ValidationError(message='评论内容不合法', code='invalid')
        return self.cleaned_data['commentContent']

    def clean_commentBlog(self):
        commentBlog_id = self.cleaned_data['commentBlog']

        if isinstance(commentBlog_id, int):  # 判断是否为int类型
            # todo 此处还可以判断该博客ID是否存在，是否为有效状态
            return self.cleaned_data['commentBlog']
        else:
            raise ValidationError(message='评论博客不存在', code='invalid')

    def clean_reply(self):
        comment_id = self.cleaned_data['reply']
        if comment_id:
            if isinstance(comment_id, int):
                comment = BlogComment.objects.get(pk=comment_id)
                if comment:
                    self.cleaned_data['reply'] = comment
                    return self.cleaned_data['reply']
                else:
                    raise ValidationError(message='回复ID不存在', code='invalid')
            else:
                raise ValidationError(message='回复ID不存在', code='invalid')


def clean(self):
    return self.cleaned_data
