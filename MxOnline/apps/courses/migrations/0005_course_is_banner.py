# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-13 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20180213_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='首页轮播'),
        ),
    ]