from .models import *
from django.forms import ModelForm


class PhysicalInfoForm(ModelForm):
    class Meta:
        model = AssetPhysicalInfo
        fields = [
            'physical_info_id',
            'physical_info_pn_bcd',
            'physical_info_sn_bcd',
            'physical_info_package_img',
            'physical_info_contour_img',
            'physical_info_sn_img',

            ]
        labels = {
            'physical_info_id': '资产DEC编号',
            'physical_info_pn_bcd': '资产型号PN',
            'physical_info_sn_bcd': '资产序列号',
            'physical_info_package_img': '资产包装照片',
            'physical_info_contour_img': '资产外观照片',
            'physical_info_sn_img': '序列号照片',
        }

    def __init__(self, *args, **kwargs):
        super(PhysicalInfoForm, self).__init__(*args, **kwargs)
        self.fields['physical_info_id'].queryset = AssetBasicInfo.objects.all()


class FinanceHistoryForm(ModelForm):
    class Meta:
        model = AssetFinanceHistory
        fields = [
            'asset_finance_history_id',
            'asset_finance_history_item',
            'asset_finance_history_type',
            'asset_finance_history_desc',
            ]

    def __init__(self, *args, **kwargs):
        super(FinanceHistoryForm, self).__init__(*args, **kwargs)
        self.fields['asset_finance_history_item'].queryset = AssetBasicInfo.objects.all()
        self.fields['asset_finance_history_type'].queryset = FinanceInfoType.objects.all()