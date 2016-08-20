from django.contrib import admin
from models import User, Port, Branch, Owner, Qdownloadcommand
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display = ('name',)
#  list_filter = ('name',)

class PortAdmin(admin.ModelAdmin):
  list_display = ('number',)

class BranchAdmin(admin.ModelAdmin):
  list_display = ('branch',)

class OwnerAdmin(admin.ModelAdmin):
  list_display = ('owner',)

class QdownloadcommandAdmin(admin.ModelAdmin):
  list_display = ('branch', 'download_command', 'descripe', 'owner', 'create_time')

admin.site.register(User, UserAdmin)
admin.site.register(Port, PortAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Qdownloadcommand, QdownloadcommandAdmin)

