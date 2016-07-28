from django.contrib import admin
from models import Server
# Register your models here.

class ServerAdmin(admin.ModelAdmin):
  list_display = ('ip', 'user', 'default_ssh', 'gerrit_ssh', 'gerrit_http', 'mail_to', 'project_path', 'reviewsite_path', 'area', 'remark')
  list_filter = ('ip',)

admin.site.register(Server, ServerAdmin)


