from django.shortcuts import render
from .form import *
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
    list_context = AssetBasicInfo.objects.all()
    list_context = {'list_context': list_context}
    return render(request, "2.html", list_context)
