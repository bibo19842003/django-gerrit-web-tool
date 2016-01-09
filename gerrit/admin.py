from django.contrib import admin
from models import User, Port
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display = ('name',)
#  list_filter = ('name',)

class PortAdmin(admin.ModelAdmin):
  list_display = ('number',)

admin.site.register(User, UserAdmin)
admin.site.register(Port, PortAdmin)

