# -*- coding: utf-8 -*-
__author__ = 'Ginseng'
import time
from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):  # 当继承serializers.Serializer时,需要自己重写某些方法,比如update
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于1",
                                        "required": "请选择购买数量"
                                    })

    """
     注意, 此处由于继承的是serializer,而不是serializer.Models所以必须要加上queryset
     设置外键,序列化时,会返回一个对象
    """
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        """
        注意!在serializer里还有一个字段是initial_data,是前段最初传来的字段,里面的数据没有经过处理,是没有调用validated之前的数据
        在serializer里,获取request是在context里,而在views里可以直接从self.request.user获取
        :param validated_data:
        :return:
        """
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]  # 此处返回的是一个goods对象而不是字段属性

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]  # ??
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        """
        因为继承的是serializers.Serializer,则需要自己重写某些方法,比如update
        :param instance: 
        :param validated_data: 
        :return: 
        """
        # 修改购物车商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m %H-%M-%S")

    def generate_order_sn(self):
        # 当前时间 + uid + 2位随机整数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))  # 从10开始到99 随机取一个两位数
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
