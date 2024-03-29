# Generated by Django 2.0.1 on 2018-11-27 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='权限名称')),
                ('type', models.CharField(choices=[('menu', '菜单权限'), ('button', '按钮权限')], max_length=32, verbose_name='资源类型')),
                ('url', models.CharField(max_length=32, verbose_name='访问url地址')),
                ('code', models.CharField(blank=True, max_length=32, null=True, verbose_name='权限代码字符')),
                ('pid_list', models.CharField(blank=True, max_length=32, null=True)),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='父权限')),
            ],
            options={
                'verbose_name': '权限表',
                'verbose_name_plural': '权限表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='角色名称')),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='角色所拥有的权限')),
            ],
        ),
    ]
