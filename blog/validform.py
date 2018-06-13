from django import forms
from django.core.exceptions import ValidationError

# 博客表单验证
from blog.models import BlogClassification


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
