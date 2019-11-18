from django.db import models
from django.conf import settings
from django.utils import timezone
from manage_unit.models import CostCenter as CC
from manage_unit.models import ManageGroup as MG


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
    item_user = models.ForeignKey(MG, on_delete=models.CASCADE)
    item_po = models.BigIntegerField(blank=True, null=True)
    item_purchase_cc = models.ForeignKey(CC, on_delete=models.CASCADE)
    item_drx_asset_nr = models.BigIntegerField(blank=True, null=True)
    item_drx_inventory_nr = models.BigIntegerField(blank=True, null=True)
    item_available = models.BooleanField(default=False)
    item_is_fixed_asset = models.BooleanField(default=True)
    item_add_date = models.DateTimeField('add_day', default=timezone.now)
    item_mod_date = models.DateTimeField('mod_day', auto_now=True)

    class Meta:
        managed = True
        db_table = 'asset_basic_info'
        verbose_name_plural = '资产列表'

    def __str__(self):
        return str(self.item_id)


class AssetPhysicalInfo(models.Model):
    physical_info_id = models.OneToOneField(AssetBasicInfo, on_delete=models.CASCADE, verbose_name='资产DEC编号')
    physical_info_pn_bcd = models.CharField(max_length=45, blank=True, null=True,
                                            verbose_name='资产型号', help_text='Product #/Part #/Model/BM #')
    physical_info_sn_bcd = models.CharField(unique=True, max_length=45, blank=True, null=True,
                                            verbose_name='资产序列号', help_text='SN/serial number')
    physical_info_sn_img = models.ImageField(upload_to='img/asset_basic_sn/', blank=True, null=True,
                                             verbose_name='序列号照片', help_text='清晰完整的SN照片')
    physical_info_package_img = models.ImageField(upload_to='img/asset_basic_package/', blank=True, null=True,
                                                  verbose_name='资产包装图', help_text='资产包装标签信息')
    physical_info_contour_img = models.ImageField(upload_to='img/asset_basic_contour/', blank=True, null=True,
                                                  verbose_name='资产外观图', help_text='清晰完整的外观照片')
    physical_info_confirmed = models.BooleanField(default=False, verbose_name='资产信息财务确认状态')
    physical_add_date = models.DateTimeField('add_day', default=timezone.now)

    class Meta:
        managed = True
        db_table = 'asset_physical_info'
        verbose_name_plural = '资产实物登记信息'

    def __str__(self):
        return str(self.physical_info_id)


class FinanceInfoType(models.Model):
    info_type_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产属性类型编码')
    info_type_desc = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产属性类型描述')
    info_type_isvalid = models.BooleanField(default=True, verbose_name='资产属性有效')
    info_type_add_date = models.DateTimeField('add_day', default=timezone.now)
    info_type_mod_date = models.DateTimeField('mod_day', auto_now=True)

    class Meta:
        managed = True
        db_table = 'finance_info_type'
        verbose_name_plural = '资产属性类型'

    def __str__(self):
        return str(self.info_type_desc)


class AssetFinanceHistory(models.Model):
    asset_finance_history_id = models.BigAutoField(primary_key=True)
    asset_finance_history_item = models.ForeignKey(AssetBasicInfo, on_delete=models.CASCADE, verbose_name='资产编号')
    asset_finance_history_type = models.ForeignKey(FinanceInfoType, on_delete=models.CASCADE, verbose_name='信息类型')
    asset_finance_history_desc = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产信息描述')
    asset_finance_history_add_date = models.DateTimeField('add_day', default=timezone.now)

    class Meta:
        managed = True
        db_table = 'asset_finance_history'
        verbose_name_plural = '资产属性记录'

    def __str__(self):
        return str(self.asset_finance_history_id)
