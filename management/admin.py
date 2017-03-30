from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from management.models import *

class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  # 把字段信息全部显示出来
    search_fields = ('name', 'user')  # 添加search bar，在指定的字段中search

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
