from django.db import models

# Create your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils import timezone


class ManageGroup(models.Model):
    manage_group_name = models.CharField(max_length=10)
    manage_group_desc = models.CharField(max_length=100)
    manage_group_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    manage_group_is_active = models.BooleanField(default=True)
    manage_group_add_date = models.DateTimeField('add_day', default=timezone.now)
    manage_group_mod_date = models.DateTimeField('mod_day', auto_now=True)

    class Mate:
        managed = True
        db_table = 'manage_group'
        verbose_name_plural = '资产管理组别设置'

    def __str__(self):
        return self.manage_group_name


class CostCenter(models.Model):
    cost_center_code = models.CharField(max_length=20)
    cost_center_desc = models.CharField(max_length=100, blank=True, null=True)
    cost_center_group = models.ForeignKey(ManageGroup, on_delete=models.CASCADE)
    cost_center_is_active = models.BooleanField(default=True)
    cost_center_add_date = models.DateTimeField('add_day', default=timezone.now)
    cost_center_mod_date = models.DateTimeField('mod_day', auto_now=True)

    class Mate:
        managed = True
        db_table = 'cost_center'
        # verbose_name_plural = '成本中心设置'

    def __str__(self):
        return self.cost_center_code


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_manage_group = models.ForeignKey(ManageGroup, on_delete=models.CASCADE)
    user_phone_number = models.CharField(max_length=12, blank=True, null=True)
    user_desc = models.CharField(max_length=100, blank=True, null=True)
    user_qualification_date = models.DateTimeField(blank=True)


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = '资产协调员信息'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ManageGroup)
admin.site.register(CostCenter)