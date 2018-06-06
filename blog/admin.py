from django.contrib import admin

from blog import models


class CustomerBlog(admin.ModelAdmin):
    list_display = ('id', 'title', 'classification', 'type', 'createUser', 'createDate',)


admin.site.register(models.Blog, CustomerBlog)
