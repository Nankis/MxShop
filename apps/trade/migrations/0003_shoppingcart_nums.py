# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-01-06 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20181229_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='nums',
            field=models.IntegerField(default=0, verbose_name='购买数量'),
        ),
    ]
