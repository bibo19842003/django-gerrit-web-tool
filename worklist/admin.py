from django.contrib import admin
from .models import Handler, ListSort, ListStatus, WorkList
# Register your models here.

class HandlerAdmin(admin.ModelAdmin):
  list_display = ('handler',)

class ListSortAdmin(admin.ModelAdmin):
  list_display = ('list_sort',)

class ListStatusAdmin(admin.ModelAdmin):
  list_display = ('list_status',)

class WorkListAdmin(admin.ModelAdmin):
  list_display = ('creator','create_time','descripe','list_num','list_status','list_sort','handler','handle_begin','wait_time','handle_end','handle_time','list_time')

admin.site.register(Handler, HandlerAdmin)
admin.site.register(ListSort, ListSortAdmin)
admin.site.register(ListStatus, ListStatusAdmin)
admin.site.register(WorkList, WorkListAdmin)

