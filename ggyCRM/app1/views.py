from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, reverse, redirect
# 使用PIl模块创建图片
from PIL import Image, ImageDraw, ImageFont
# 创建随机数
import random
# 创建内存缓存
from io import BytesIO
from django.http import JsonResponse
from app1.form import *
from app1.models import UserInfo, Customer, ConsultRecord
from app1.utils.page import Pagination
from django.db.models import F, Q
from django.views import View


# Create your views here.
def login(request):
    """
    登录界面
    :param request:
    :return:
    """
    # if request.method=="POST":
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        validcode = request.POST.get("validcode")

        # Ajax请求返回一个字典
        response = {"user": None, "err_msg": ""}
        if validcode.upper() == request.session.get("keep_str").upper():
            user_obj = auth.authenticate(username=user, password=pwd)
            if user_obj:
                auth.login(request, user_obj)
                response["user"] = user
            else:
                response['err_msg'] = "用户名或者密码错误！"
        else:
            response["err_msg"] = "验证码错误！"

        return JsonResponse(response)
    else:
        return render(request, "login.html")


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect('/login/')


def get_valid_img(request):
    """
    获取验证码
    :param request:
    :return:
    """

    #  方式1：读取指定图片
    # with open("static/img/valid.jpg","rb") as f:
    #     data=f.read()

    # 方式2：基于PIL模块创建验证码图片

    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    img = Image.new("RGB", (300, 38), get_random_color())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/kumo.ttf", 32)

    keep_str = ""
    for i in range(6):
        random_num = str(random.randint(0, 9))
        random_lowalf = chr(random.randint(97, 122))
        random_upperalf = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_lowalf, random_upperalf])
        draw.text((i * 30 + 50, 0), random_char, get_random_color(), font=font)
        keep_str += random_char

    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()

    print('keep_str', keep_str)

    # 将验证码存在各自的session中

    request.session['keep_str'] = keep_str

    return HttpResponse(data)


def reg(request):
    """
    注册页面
    :param request:
    :return:
    """
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        res = {"user": None, "err_msg": ""}
        if form.is_valid():
            res["user"] = form.cleaned_data.get("user")
            print("ok", form.cleaned_data)
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            # 此处因继承用户类，所以加 _user 创建
            user = UserInfo.objects.create_user(username=user, password=pwd, email=email)

        else:
            res["err_msg"] = form.errors
            print(form.errors)
            print(form.cleaned_data)

        return JsonResponse(res)
    else:
        form = UserForm()
        return render(request, "reg.html", locals())


@login_required
def index(request):
    """
    主页显示
    :param request:
    :return:
    """
    user = request.user
    return render(request, 'index.html', {"user": user})


class CustomersView(View):
    """

    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        if reverse("customers_list") == request.path:
            label = "公户列表"
            customer_list = Customer.objects.filter(consultant__isnull=True)
        else:
            label = "我的客户"
            customer_list = Customer.objects.filter(consultant=request.user)
        val = request.GET.get("q")
        field = request.GET.get("field")
        if val:
            q = Q()
            q.children.append((field + "__contains", val))
            customer_list = customer_list.filter(q)

        current_page_num = request.GET.get("page")
        pagination = Pagination(current_page_num, customer_list.count(), request)
        customer_list = customer_list[pagination.start:pagination.end]

        path = request.path
        next = "?next=%s" % (path,)
        return render(request, 'customer/customer_list.html',
                      {'next': next, 'label': label, 'customer_list': customer_list, "pagination": pagination})

    def post(self, request):
        """

        :param request:
        :return:
        """
        print(request)
        func_str = request.POST.get("action")
        data = request.POST.get("select_pk_list")
        if not hasattr(self, func_str):
            return HttpResponse("非法输入！")
        else:
            func = getattr(self, func_str)
            queryset = Customer.objects.filter(pk__in=data)
            ret = func(request, queryset)
            if ret:
                return ret
            return redirect(request.path)

    def patch_delete(self, request, queryset):
        """

        :param request:
        :param queryset:
        :return:
        """
        queryset.delete()

    def patch_reverse_gs(self, request, queryset):
        """
        公户转私户
        :param request:
        :param queryset:
        :return:
        """

        ret = queryset.filter(consultant__isnull=True)
        if ret:
            ret.update(consultant=request.user)
        else:
            return HttpResponse("手速太慢！")

    def patch_reverse_sg(self, request, queryset):
        """
        私户转公户
        :param request:
        :param queryset:
        :return:
        """
        queryset.update(consultant=None)


# def customers(request):
#     """
#     客户显示
#     :param request:
#     :return:
#     """
#     pass

#
# class AddCustomersView(View):
#
#     def get(self, request):
#         form = CustomerModelForm()
#         return render(request, 'add_customers.html', {"form": form})
#
#     def post(self, request):
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("customers_list"))
#         else:
#             return render(request, 'add_customers.html', {'form': form})
#
#
# class EditCustomersView(View):
#
#     def get(self, request, id):
#         edit_obj = Customer.objects.get(pk=id)
#         form = CustomerModelForm(instance=edit_obj)
#         return render(request, "edit_customers.html", {"form": form})
#
#     def post(self, request, id):
#         edit_obj = Customer.objects.get(pk=id)
#         form = CustomerModelForm(request.POST, instance=edit_obj)
#         if form.is_valid():
#             form.save()
#             return redirect(request.GET.get("next"))
#         else:
#             return render(request, 'edit_customers.html', {'form': form})


class AddEditCustomerView(View):

    def get(self, request, edit_id=None):
        """

        :param request:
        :param edit_id:
        :return:
        """
        edit_obj = Customer.objects.filter(pk=edit_id).first()
        form = CustomerModelForm(instance=edit_obj)
        return render(request, "customer/add_edit_customers.html", {'form': form, 'edit_obj': edit_obj})

    def post(self, request, edit_id=None):
        """

        :param request:
        :param edit_id:
        :return:
        """
        edit_obj = Customer.objects.filter(pk=edit_id).first()
        form = CustomerModelForm(request.POST, instance=edit_obj)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))
        else:
            return render(request, 'customer/add_edit_customers.html', {'form': form})


class ConsultRecordsView(View):

    def get(self, request):
        """

        :param request:
        :return:
        """
        consult_record_list = ConsultRecord.objects.filter(consultant=request.user)
        customer_id = request.GET.get("customer_id")
        if customer_id:
            consult_record_list = consult_record_list.filter(customer_id=customer_id)
        return render(request, 'customer/consultrecord.html', {'consult_record_list': consult_record_list})


class AddEditConsultRecordView(View):
    """

    """
    def get(self, request, edit_id=None):
        """

        :param request:
        :param edit_id:
        :return:
        """
        edit_obj = ConsultRecord.objects.filter(pk=edit_id).first()
        form = ConsultRecordModelForm(instance=edit_obj)
        return render(request, "customer/add_edit_consultrecord.html", {'form': form, 'edit_obj': edit_obj})

    def post(self, request, edit_id=None):
        """

        :param request:
        :param edit_id:
        :return:
        """
        edit_obj = ConsultRecord.objects.filter(pk=edit_id).first()
        form = ConsultRecordModelForm(request.POST, instance=edit_obj)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))
        else:
            return render(request, 'customer/add_edit_consultrecord.html', {'form': form})

