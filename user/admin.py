from django.contrib import admin
from user import models


# Register your models here.

# 配置当前model在Django admin中的展示内容，默认配置是只展示model中的__str__方法的返回值
class CustomerUser(admin.ModelAdmin):
    list_display = ('id', 'username', 'sex', 'age', 'email', 'createDate',)
    list_filter = ('username', 'sex', 'age', 'createDate',)
    search_fields = ('username',)
    # raw_id_fields = ('consult_course',)
    # filter_horizontal = ('tags',)
    # list_editable = ('status',)


admin.site.register(models.User, CustomerUser)
