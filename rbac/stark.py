from stark.service.stark import site, ModelStark

from rbac.models import *
from django import forms
from django.urls.resolvers import URLPattern
from django.conf.urls import url
from django.forms import widgets as wid
from django.shortcuts import HttpResponse, render, redirect
from rbac.models import Role, Permission
from app1.models import UserInfo
from django.http import JsonResponse


class PermissionModelForm(forms.ModelForm):
    class Meta:
        model = Permission
        exclude = ["per_level", "pids"]
        widgets = {
            "url": wid.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ggyCRM.urls import urlpatterns
        ret = [[i, i] for i in self.get_all_url(urlpatterns, prev='/', is_first=True)]
        ret.insert(0, ["", ""])
        self.fields['url'].widget.choices = ret

    def get_all_url(self, urlparrentens, prev, is_first=False, result=[]):
        if is_first:
            result.clear()
        ignore_list = ["admin/"]
        for item in urlparrentens:
            if isinstance(item, URLPattern):
                if str(item.pattern) == "^$":
                    result.append(prev)
                else:
                    result.append(prev + str(item.pattern))
            else:
                if str(item.pattern) in ignore_list: continue
                self.get_all_url(item.urlconf_name, prev + str(item.pattern))
        print("result", result)

        return result


class PermissionConfig(ModelStark):

    def per_data(self, request):

        permissions = Permission.objects.values("pk", "title", "url", "pid", "type")
        print("permissions", permissions)
        return JsonResponse(list(permissions), safe=False)

    def permission_distribute(self, request):

        uid = request.GET.get('uid')
        rid = request.GET.get('rid')
        user = UserInfo.objects.filter(id=uid)

        if request.method == "POST" and request.POST.get('postType') == 'role':
            print(request.POST.getlist("roles"))
            l = request.POST.getlist("roles")
            user.first().roles.set(l)

        if request.method == "POST" and request.POST.get('postType') == 'permission':

            role = Role.objects.filter(id=rid).first()
            if not role:
                return HttpResponse('角色不存在')
            role.permissions.set(request.POST.getlist('permissions_id'))

        # 所有用户
        user_list = UserInfo.objects.all()
        role_list = Role.objects.all()

        print("uid", uid)

        if uid:
            role_id_list = UserInfo.objects.get(pk=uid).roles.all().values_list("pk")
            role_id_list = [item[0] for item in role_id_list]
            per_id_list = UserInfo.objects.get(pk=uid).roles.filter(permissions__isnull=False).values_list(
                "permissions__pk").distinct()
            per_id_list = [item[0] for item in per_id_list]

        if rid:
            per_id_list = Role.objects.filter(pk=rid).filter(permissions__isnull=False).values_list(
                "permissions__pk").distinct()
            per_id_list = [item[0] for item in per_id_list]

        return render(request, "permission_distribute.html", locals())

    def extra_url(self):
        l = [
            url(r"distribute/", self.permission_distribute),
            url(r"per_data/", self.per_data),
        ]
        return l

    list_display = ['title', "type", 'url', "code", "pid"]
    model_form_class = PermissionModelForm


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = Role
        exclude = ["permissions", ]


class RoleConfig(ModelStark):
    model_form_class = RoleModelForm


site.register(Role, RoleConfig)
site.register(Permission, PermissionConfig)
