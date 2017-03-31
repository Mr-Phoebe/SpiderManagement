from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from management.models import *

class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class TaskFileInline(admin.StackedInline):
    model = TaskFile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)

class TaskAdmin(admin.ModelAdmin):
    inlines = (TaskFileInline,)
    list_display = ('name', 'user')
    search_fields = ('name', 'user')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
