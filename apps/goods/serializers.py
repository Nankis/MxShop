# -*- coding: utf-8 -*-
from django.db.models import Q

__author__ = 'Ginseng'

from rest_framework import serializers
from goods.models import Goods, GoodsCategory, GoodsImage, HotSearchWords, Banner, GoodsCategoryBrand, IndexAd


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):  # 最外层的一类
    sub_cat = CategorySerializer2(many=True)  # 必须设置many=True

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):  # 注意映射顺序
    class Meta:
        model = GoodsImage
        fields = ("image",)


# 若是在user的models中__str__没有返回username 则会报错,需要return self.username 或者退出xadmin的后台
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # 实例化, 嵌套序列化--->进一步序列化 外键 category
    images = GoodsImageSerializer(many=True)  # images是根据外键related_name="images"设置的, many=True一定要设置 ===>> 一对多关系

    class Meta:
        model = Goods
        fields = "__all__"  # 序列化 全部字段


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)  # brands 表有个外键指向category
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods

            """
            在自己写的serializer里嵌套serializer 需要手动添加context={'request': self.context['request']},否则图片文件资料等,其路径资源
            不会加上域名或IP地址
            因为在上下文context中如果有request这个属性,它就会自动添加域名或地址
            """
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
