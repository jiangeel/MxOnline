# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-08 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180205_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(default='无名氏', max_length=50, verbose_name='昵称'),
        ),
    ]