# -*- coding: utf-8 -*-
# @File  : form.py
# @Author: yh
# @Date  : 2019/8/13
# @Software: PyCharm
from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets
from multiselectfield.forms.fields import MultiSelectFormField
from app1.models import *
import re


class CustomerModelForm(forms.ModelForm):
    """

    """
    class Meta:
        """

        """
        model = Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


class UserForm(forms.Form):
    """

    """
    user = forms.CharField(min_length=2, label="用户名")
    gender = forms.ChoiceField(choices=((1, "男"), (2, "女")), label="性别")
    pwd = forms.CharField(min_length=5, label="密码", widget=widgets.PasswordInput)
    r_pwd = forms.CharField(min_length=5, label="确认密码", widget=widgets.PasswordInput)
    email = forms.EmailField(min_length=5, label="邮箱")

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})

    def clean_user(self):
        """

        :return:
        """
        val = self.cleaned_data.get("user")
        user = UserInfo.objects.filter(username=val).first()
        if user:
            raise ValidationError("用户已存在！")
        else:
            return val

    def clean_pwd(self):
        """

        :return:
        """
        val = self.cleaned_data.get("pwd")
        if val.isdigit():
            raise ValidationError("密码不能是纯数字！")
        else:
            return val

    def clean_email(self):
        """

        :return:
        """
        val = self.cleaned_data.get("email")
        if re.search("\w+@qq.com$", val):
            return val
        else:
            raise ValidationError("邮箱必须是163邮箱！")

    def clean(self):
        """

        :return:
        """
        pwd = self.cleaned_data.get("pwd")
        r_pwd = self.cleaned_data.get("r_pwd")

        if pwd and r_pwd and r_pwd != pwd:
            self.add_error("r_pwd", ValidationError("两次密码不一致！"))
        else:
            return self.cleaned_data


class ConsultRecordModelForm(forms.ModelForm):
    """
    未完成当前用户显示
    """

    class Meta:
        model = ConsultRecord
        # fields = "__all__"
        exclude = ["delete_status"]
