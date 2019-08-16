# -*- coding: utf-8 -*-
# @File  : middlewares.py
# @Author: yh
# @Date  : 2019/8/13
# @Software: PyCharm
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class LoginMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        """

        :param request:
        :return:
        """
        if request.path in ["/login/", "/reg/", "/get_valid_img/"]:
            return None
        if not request.user.id:
            return redirect("/login/")

class CurrentUserMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        """

        :param request:
        :return:
        """
        print()



