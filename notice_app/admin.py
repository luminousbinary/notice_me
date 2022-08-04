from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminUser, Staff, Course,  Student,  Department, PostModel, Comment
# Register your models here.

class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
admin.site.register(AdminUser)
admin.site.register(Staff)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(PostModel)
admin.site.register(Comment)