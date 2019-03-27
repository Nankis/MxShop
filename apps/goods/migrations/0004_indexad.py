# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-01-08 11:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20181231_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='goods.GoodsCategory', verbose_name='商品类目')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='goods.Goods')),
            ],
            options={
                'verbose_name': '首页商品类广告',
                'verbose_name_plural': '首页商品类广告',
            },
        ),
    ]
