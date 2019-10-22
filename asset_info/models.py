from django.db import models
from django.conf import settings
from django.utils import timezone
from manage_unit.models import CostCenter as CC


class AssetBasicInfo(models.Model):
    a = '''
    ASSET_TYPE = (
        (1, "FIXED ASSET"),
        (2, "LOW VALUE IT PARTS"),
    )
    ASSET_STATUS_TYPE = (
        (1, "Asset create in system"),
        (2, "Asset info collected, Waiting for confirmation"),
        (3, "Info confirmed, Waiting for labeling"),
        (4, "IN user"),
        (5, "Loss"),
        (6, "Scrap"),
    )
    # item_status = models.ForeignKey('ItemStatus', on_delete=models.CASCADE)
    # item_status = models.IntegerField('status', choices=ASSET_STATUS_TYPE, default=1)
    # item_type = models.IntegerField('type', choices=ASSET_TYPE, default=1)
'''
    item_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    item_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_cc = models.ForeignKey(CC, on_delete=models.CASCADE)
    item_drx_asset_nr = models.BigIntegerField(blank=True, null=True)
    item_drx_inventory_nr = models.BigIntegerField(blank=True, null=True)
    item_pn_bcd = models.CharField(max_length=45, blank=True, null=True)
    item_sn_bcd = models.CharField(unique=True, max_length=45, blank=True, null=True)
    item_sn_img = models.ImageField(upload_to='asset_basic_sn', blank=True, null=True)
    item_contour_img = models.ImageField(upload_to='asset_basic_contour', blank=True, null=True)
    item_sn_confirmed = models.BooleanField(default=False)
    item_in_use = models.BooleanField(default=False)
    item_is_fixed_asset = models.BooleanField(default=True)
    item_add_date = models.DateTimeField('add_day', default=timezone.now)
    item_mod_date = models.DateTimeField('mod_day', auto_now=True)

    class Meta:
        managed = True
        db_table = 'asset_basic_info'
        verbose_name_plural = '资产列表'

    def __str__(self):
        return str(self.item_id)
