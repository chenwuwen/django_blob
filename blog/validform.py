from django.forms import forms, fields


# 博客表单验证
class BlogForm(forms.Form):
    title = fields.CharField(required=True, error_messages={'required': '标题不能为空'})
    content = fields.CharField(required=True, error_messages={'required': '内容不能为空'})

    def clean_content(self):
        content = self.cleaned_data['content']
        # 检测是否含有敏感字classification
        # todo
        return self.cleaned_data

    def clean_title(self):
        title = self.cleaned_data['title']
        return self.cleaned_data
