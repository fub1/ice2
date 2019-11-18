from django.shortcuts import render
from .form import *
from asset_usage.models import *
from asset_info import *
from manage_unit.models import *
from django.contrib.auth.decorators import login_required

# 资产基本信息录入
@login_required(login_url='/admin/login/')
def asset_info_from(request):
    if request.method == "GET":
        obj = PhysicalInfoForm()
    if request.method == "POST":
        obj = PhysicalInfoForm(data=request.POST) ##传入进行验证
        if obj.is_valid():
            #models.News.objects.create(**obj.cleaned_data) ##以前Form的时候添加数据要这样写
            obj.save()  ##modelform现在可以直接save就可以，save的时候可以保存一对多、多对多的数据
            return render(request, 'ok.html')
        else:
            print(obj.errors)
    return render(request, "basicinfoinput.html", locals())


@login_required(login_url='/admin/login/')
def f2(request):
    if request.method == "GET":
        obj = FinanceHistoryForm()
    if request.method == "POST":
        obj = FinanceHistoryForm(data=request.POST) ##传入进行验证
        if obj.is_valid():
            #models.News.objects.create(**obj.cleaned_data) ##以前Form的时候添加数据要这样写
            obj.save()  ##modelform现在可以直接save就可以，save的时候可以保存一对多、多对多的数据
            return render(request, 'ok.html')
        else:
            print(obj.errors)
    return render(request, "f002.html", locals())


@login_required(login_url='/admin/login/')
def asset_list(request):
    login_mg = UserInfo.objects.values_list('user_manage_group', flat=True).filter(user=request.user).first()
    list_context = AssetBasicInfo.objects.filter(item_user=login_mg)
    if request.user.is_superuser:
        list_context = AssetBasicInfo.objects.all()

    list_context = {'list_context': list_context}
    return render(request, "2.html", list_context)


@login_required(login_url='/admin/login/')
def asset_details(request):
    login_mg = UserInfo.objects.values_list('user_manage_group', flat=True).filter(user=request.user).first()
    print(login_mg)
    user_asset_list = list((AssetBasicInfo.objects.values_list('item_id', flat=True).filter(item_user=login_mg)))
    print(user_asset_list)
    list_context = AssetFinanceHistory.objects.filter(asset_finance_history_item__in=user_asset_list)
    print(list_context)
    list_context = {'list_context': list_context}
    return render(request, '3.html', list_context)