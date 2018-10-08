from django.contrib import admin
from .models import Server, Gerritserver
# Register your models here.

class ServerAdmin(admin.ModelAdmin):
  list_display = ('ip', 'area', 'remark')
  list_filter = ('area',)


class GerritserverAdmin(admin.ModelAdmin):
  list_display = ('gerrit_ip', 'user', 'gerrit_ssh_port', 'gerrit_http_port', 'gerrit_http_port', 'mail_to', 'project_path', 'reviewsite_path', 'sshkey_path', 'gerrit_user', 'gerrit_pass')
  list_filter = ('gerrit_ip',)

admin.site.register(Server, ServerAdmin)
admin.site.register(Gerritserver, GerritserverAdmin)


