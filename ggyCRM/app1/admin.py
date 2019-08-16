from django.contrib import admin
from .models import *

admin.site.site_header = 'CRM后台管理'
admin.site.index_title = '后台系统'
admin.site.site_title = '管理'


# Register your models here.
@admin.register(UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'gender', 'tel']
    list_filter = ['gender']
    search_fields = ['account', 'username']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sex', 'class_type', 'status']


@admin.register(Campuses)
class CampusesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address']


@admin.register(ClassList)
class ClassListAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'campuses']


@admin.register(ConsultRecord)
class ConsultRecord(admin.ModelAdmin):
    list_display = ['customer', 'status', 'consultant', 'date']
