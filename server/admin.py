from django.contrib import admin
from models import Server
# Register your models here.

class ServerAdmin(admin.ModelAdmin):
  list_display = ('ip', 'area', 'remark')
  list_filter = ('area',)

admin.site.register(Server, ServerAdmin)


