from django.contrib import admin

from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'contact', 'address']

class ShiftAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_time', 'end_time', 'date']

class FaceAdmin(admin.ModelAdmin):  
    list_display = ['user', 'picture']

admin.site.register(User, UserAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Face, FaceAdmin)