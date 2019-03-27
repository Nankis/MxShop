# -*- coding: utf-8 -*-
__author__ = 'Ginseng'
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from MxShop.settings import REGEX_MOBILE
from datetime import datetime
from datetime import timedelta
from .models import VerifyCode
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):  # 必须以validate开头并且和models中的字段联合
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送未超过60s")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """
    特别注意!
    在code字段设置 write_only=True后, 在序列化时就不会把code也序列化进去,否则在usermodels中没有
    code字段,而在CreateModelMixin中create方法的return Response(serializer.data, .....)里,序列化的data
    会把该序列化(即UserRegSerializer) 的fields = ("username", "code", "mobile", "password")中所有字段
    均序列化,从而会报错
    """
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")

    # 通过唯一验证 验证 用户是否存在
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")]
                                     )

    """
    注意!
        在成功POST后,(具体函数同上) CreateModelMixin会返回被序列化的字段,而在POST密码时,我们不应该讲密码再返回
        所以,   同样,只需要将其也加上write_only=True,即可
    """
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # 重载create方法,对密码进行加密 ,也可以通过信号量机制对models进行操作.
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)  # 取到一个user
    #     user.set_password(validated_data["password"])  # 将取到的user中的password字段加密
    #     user.save()
    #     return user

    def validate_code(self, code):
        # 前端传过来的值 都放在了self.initial_data里面  注意!!!千万不要写成initial.data
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]  # 取出最新一条信息
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)

            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

        if verify_records:
            last_record = verify_records[0]

    def validate(self, attrs):  # 作用于所有字段的validate,其中 attrs是所有validate_字段  返回的一个dict
        attrs["mobile"] = attrs["username"]  # 即便前端可以不传mobile  在attrs中也可以直接添加一个
        del attrs["code"]  # 由于usermodels里面没有code字段, 所以 验证完成后 需要删除code字段
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
        用户详情序列化类
    """

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")
