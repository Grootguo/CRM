from django.contrib import admin

# Register your models here.

from app1.models import *

admin.site.register(UserInfo)
admin.site.register(ClassList)
admin.site.register(Customer)
admin.site.register(Campuses)

