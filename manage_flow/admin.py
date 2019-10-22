from django.contrib import admin

# Register your models here.
from .models import *

from .models import Modal,Node,TodoList,Instance,History


class NodeInline(admin.TabularInline):
    model = Node
    fields = ['code','name','next_user_handler','can_deny','can_terminate']

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class WorkflowModelAdmin(admin.ModelAdmin):
    list_display = ['code','name','begin','end']
    inlines = [NodeInline]
    readonly_fields = ['app_name','model_name']
    raw_id_fields = ['content_type']
    fields = (
        ('begin','end',),('code','name',),('description',),('content_type',),('app_name','model_name',),
    )


class TodoAdmin(admin.ModelAdmin):
    list_display = ['code_link','modal_dsc','href','node_dsc','is_read','status','submitter','arrived_time']
    list_filter = ['status']

    def get_queryset(self, request):
        return super(TodoAdmin,self).get_queryset(request).filter(user=request.user)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['inst','node','user','pro_time','memo']


class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ['app_label','model']
    search_fields = ['app_label','model']
    list_per_page = 20
    list_filter = ['app_label']


admin.site.register(Modal, WorkflowModelAdmin)
admin.site.register(Node)
admin.site.register(Instance)
admin.site.register(TodoList, TodoAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(ContentType, ContentTypeAdmin)

from asset_info.models import *
admin.site.register(AssetBasicInfo)
# admin.site.register(UsageInfo)
from asset_usage.models import *
admin.site.register(UsageInfoType)
admin.site.register(UsageInfo)