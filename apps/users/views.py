# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from requests import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets, status
from random import choice
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions

from utils.yunpian import YunPian
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from MxShop.settings import APIKEY
from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码,
        每次从seeds中随机选择一个数字,并添加到random_str的list中,一共选择4次
        最后通过""连接,将list转换成str字符串  如['1','2','3','4'] ===>>  1234
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # 直接获取  serializer_class = SmsSerializer 这个serialize
        serializer.is_valid(raise_exception=True)  # 验证serializer是否调用成功. 若设置True,失败则不会执行之后代码

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):  # 动态设置serializer
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):  # 动态设置某操作是否需要权限
        """
        只有使用viewset才有action
        :return:
        """
        if self.action == "retrieve":
            return [permissions.IsAuthenticated(), ]  # 注意 是返回实例需要加括号,此处不是函数
        elif self.action == "create":
            return []

        return []  # 此处一定要再返回个空数组,不然容易出错

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        re_dict["token"] = token
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写该方法 用于控制Retrieve方法 (也能影响delet方法) 这么写可以在接口users/id 返回任意id值 也能返回当前的用户
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
