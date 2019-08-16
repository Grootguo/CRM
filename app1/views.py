from django.shortcuts import render, HttpResponse,reverse

# Create your views here.
from django.http import JsonResponse
from django.contrib import auth
from app1.form import UserForm
from app1.models import UserInfo, Customer
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.contrib.auth.decorators import login_required
from app1.utils.page import Pagination

import random


def login(request):
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
                response["user"] = user
            else:
                response['err_msg'] = "用户名或者密码错误！"
        else:
            response["err_msg"] = "验证码错误！"

        return JsonResponse(response)
    else:
        return render(request, "login.html")


def get_valid_img(request):
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
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)
        res = {"user": None, "err_msg": ""}
        if form.is_valid():
            res["user"] = form.cleaned_data.get("user")
            print("cleaned_data", form.cleaned_data)
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")

            user = UserInfo.objects.create_user(username=user, password=pwd, email=email)


        else:
            print(form.errors)
            print(form.cleaned_data)
            res["err_msg"] = form.errors

        return JsonResponse(res)


    else:
        form = UserForm()
        return render(request, "register.html", locals())


def index(request):

    return render(request, "index.html")

@login_required
def customers(request):

    if reverse("customers_list")==request.path:
        customer_list=Customer.objects.all()
    else:
        customer_list = Customer.objects.filter(consultant=request.user)

    # search过滤
    val=request.GET.get("q")
    filter_field="name"
    if val:
        q=Q()
        q.children.append()

        customer_list=customer_list.filter(filter_field=val)

        #customer_list=customer_list.filter(Q(name__contains=val)|Q(qq__contains=val))

    # 分页
    current_page_num=request.GET.get("page")
    pagination=Pagination(current_page_num,customer_list.count(),request)

    customer_list=customer_list[pagination.start:pagination.end]


    return render(request,"customer_list.html",{"customer_list":customer_list,"pagination":pagination})