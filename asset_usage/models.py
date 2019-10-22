from django.db import models
from django.conf import settings
from django.utils import timezone
from asset_info.models import AssetBasicInfo


class UsageInfoType(models.Model):
    usage_type_id = models.BigAutoField(primary_key=True)
    usage_type_code = models.CharField(max_length=10, blank=True, null=True)
    usage_type_desc = models.CharField(max_length=100, blank=True, null=True)
    usage_type_isvalid = models.BooleanField(default=True)
    usage_type_add_date = models.DateTimeField('add_day', default=timezone.now)
    usage_type_mod_date = models.DateTimeField('mod_day', auto_now=True)

    class Meta:
        managed = True
        db_table = 'usage_info_type'
        verbose_name_plural = '资产属性类型'

    def __str__(self):
        return self.usage_type_desc


class UsageInfo(models.Model):
    usage_info_item = models.ForeignKey(AssetBasicInfo, on_delete=models.CASCADE)
    usage_info_type = models.ForeignKey(UsageInfoType, on_delete=models.CASCADE)
    usage_info_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    usage_type_desc = models.CharField(max_length=100, blank=True, null=True)
    usage_info_add_date = models.DateTimeField('add_day', default=timezone.now)

    class Meta:
        managed = True
        db_table = 'usage_info_'
        verbose_name_plural = '资产信息记录'

    def __str__(self):
        return str(self.usage_info_item)