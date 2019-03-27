# -*- coding: utf-8 -*-
__author__ = 'Ginseng'
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
        显示收藏页面商品的详情
    """
    goods = GoodsSerializer()  # 嵌套序列化

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):  # 此处用modelserializer

    """
        只允许当前登录的用户收藏,而不能是选择用户
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        """
        注意!
            因为此处的validators是作用在多个字段之上的,所以不能写在单字段处,
            因此在此处--->需要写在Meta里
            
            解决联合唯一键的问题:  方法1. 在models里设置unique_together 然后生成表  
                                   方法2. 在对应的serializer的Meta里设置Validators
        """
        validators = [   # 注意 不是validator  而是validators
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')  # 设置添加留言时,不用手动选择时间,而服务器返回时可以有

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")
