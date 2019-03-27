# -*- coding: utf-8 -*-
__author__ = 'Ginseng'

import django_filters
from .models import Goods
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    pricemin = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')  # lookup_expr 表示 过滤时要进行的操作
    pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    # name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")  # icontains 表示 包含（忽略大小写）

    def top_category_filter(self, queryset, name, value):
        """
        查找一级,二级,三级类目..
        :param queryset:
        :param name:
        :param value:
        :return:
        """
        queryset = queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
                                   Q(category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods  # 操作的表
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']  # 要过滤的字段
