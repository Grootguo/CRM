from django.conf.urls import url
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse

from app1.models import *
from stark.service.stark import site, ModelStark


class CustomerConfig(ModelStark):
    def classes(self, obj=None, is_header=False):
        if is_header:
            return "所报班级"
        return obj.get_classlist()

    def gender(self, obj=None, is_header=False):
        if is_header:
            return "性别"

        return obj.get_sex_display()

    def status(self, obj=None, is_header=False):
        if is_header:
            return "状态"
        return obj.get_status()

    list_display = ["name", "qq", gender, classes, status, "consultant"]

    search_fields = ["name", "qq"]

    def statistics(self, request):
        date = request.GET.get("date", "recent_month")
        import datetime
        now = datetime.datetime.now().date()
        delta1 = datetime.timedelta(days=1)
        delta2 = datetime.timedelta(weeks=1)
        delta3 = datetime.timedelta(weeks=4)

        dtae_show = {
            "today": "今日",
            "yesterday": "昨日",
            "week": "近一周",
            "recent_month": "近一月",
        }.get(date)

        condition = {
            "today": [{"deal_date__date": now}, {"customers__deal_date": now}],
            "yesterday": [{"deal_date__date": now - delta1}, {"customers__deal_date": now - delta1}],
            "week": [{"deal_date__gte": now - delta2, "deal_date__lte": now},
                     {"customers__deal_date__gte": now - delta2, "customers__deal_date__lte": now}
                     ],
            "recent_month": [{"deal_date__gte": now - delta3, "deal_date__lte": now},
                             {"customers__deal_date__gte": now - delta3, "customers__deal_date__lte": now}
                             ],
        }

        customer_list = Customer.objects.filter(**(condition.get(date)[0]))
        ret = UserInfo.objects.all().filter(**(condition.get(date)[1])).annotate(c=Count("customers")).values_list(
            "username", "c")
        ret_x = [i[0] for i in list(ret)]
        ret_y = [i[1] for i in list(ret)]

        return render(request, "statistics.html", locals())

    def extra_url(self):

        l = [
            url("statistics/", self.statistics),
            url("own/", self.own_or_public_customer, name="own_customer"),
            url("public/", self.own_or_public_customer)
        ]
        return l

    # 我的客户
    def own_or_public_customer(self, request):
        if request.method == "GET":
            if request.path == reverse("own_customer"):
                customer_list = Customer.objects.filter(consultant=request.user)
                action = ("own2public", "私户转公户")
                title = "我的客户"
            else:
                customer_list = Customer.objects.filter(consultant__isnull=True)
                action = ("public2own", "公户转私户")
                title = "公户列表"
            return render(request, "customer.html", locals())
        else:
            action = request.POST.get("action")
            pk_list = request.POST.getlist("pk_list")
            print("pk_list--->", pk_list)
            if hasattr(self, action):
                getattr(self, action)(request, pk_list)
                return redirect(request.path)

    def own2public(self, request, pk_list):
        Customer.objects.filter(pk__in=pk_list).update(consultant=None)

    def public2own(self, request, pk_list):
        print("pk_list", pk_list)
        Customer.objects.filter(pk__in=pk_list).update(consultant=request.user)

    list_filter = ["consultant", "status", "class_list"]


class UserInfoConfig(ModelStark):
    list_display = ["name", "age", "gender", "depart"]


class ConsultRecordConfig(ModelStark):

    def filter_date(self, obj=None, is_header=False):
        if is_header:
            return "跟进日期"
        return obj.date.strftime("%Y-%m-%d")

    list_display = ["customer", "note", "consultant", filter_date]


site.register(Campuses)
site.register(Department)

site.register(Customer, CustomerConfig)
site.register(UserInfo, UserInfoConfig)
site.register(ConsultRecord, ConsultRecordConfig)
site.register(Enrollment)
site.register(Student)
site.register(StudentStudyRecord)
site.register(ClassStudyRecord)
site.register(ClassStudyRecord)

# class HostConfig(ModelStark):
#     list_display = ["name","IP","dist","room"]
#     list_filter = ["room"]
#     search_fields = ["name"]
# site.register(Host,HostConfig)
# site.register(HostRoom)
