from django.contrib import admin

from blog import models


class CustomerBlog(admin.ModelAdmin):
    list_display = ('id', 'title', 'classification', 'type', 'createUser', 'createDate',)


class CustomerBlogType(admin.ModelAdmin):
    list_display = ('id', 'name',)


class CustomerBlogClassification(admin.ModelAdmin):
    list_display = ('id', 'name', 'createDate',)


class CustomerBlogTag(admin.ModelAdmin):
    list_display = ('id', 'name', 'createDate',)


admin.site.register(models.Blog, CustomerBlog)
admin.site.register(models.BlogType, CustomerBlogType)
admin.site.register(models.BlogClassification, CustomerBlogClassification)
admin.site.register(models.BlogTag, CustomerBlogTag)
