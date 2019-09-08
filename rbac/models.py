from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin

from django.utils.translation import gettext_lazy as _


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32, verbose_name='权限名称')
    type = models.CharField(max_length=32, verbose_name='资源类型', choices=[("menu", "菜单权限"), ("button", "按钮权限")])
    url = models.CharField(max_length=128, verbose_name='访问url地址', null=True, blank=True)
    code = models.CharField(max_length=32, verbose_name='权限代码字符', null=True, blank=True)
    pid = models.ForeignKey("self", on_delete=models.CASCADE, null=True, verbose_name='父权限', blank=True)
    # per_level = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="权限级别")
    pids = models.CharField(max_length=32, null=True, blank=True, verbose_name="父权限组合")  # "1/5/13" 可避开递归,当然需要重写save

    class Meta:
        verbose_name_plural = '权限表'
        verbose_name = '权限表'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        count = 1
        pid_list = []
        while self.pid:
            count += 1
            pid_list.append(self.pid_id)
            self.pid = self.pid.pid
        self.per_level = count
        self.pids = "/".join([str(i) for i in pid_list])
        super(Permission, self).save(*args, **kwargs)


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色所拥有的权限', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '角色表'
        verbose_name = '角色表'


class User(AbstractUser):
    """
    用户表
    """
    roles = models.ManyToManyField(to=Role, verbose_name='用户所拥有的角色', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        abstract = True
