# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import mixins, viewsets
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户收藏
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否收藏
    destroy:
        取消收藏
    create:
        收藏商品
    """
    # queryset = UserFav.objects.all()  # 因为要获取当前登录用户自己的收藏数据库表,所以不能是获取全部的,应该重写get_queryset方法

    # IsAuthenticated 需要用户登录后才能操作
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # 在用户访问这个页面时才会做JWT验证,  而因为JWT不会保存在服务器 所以同时也需要Session用于用户能在网页登录
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 加上 RetrieveModelMixin后 再设置lookup_field = "goods_id" 即可指定对应ID索引,注意goods_id要与数据库字段对应
    # 注意 lookup_field 的字段只是从当前已认证的用户中搜索, 而不是对所有的用户goods_id搜索
    lookup_field = "goods_id"

    def get_serializer_class(self):  # 动态设置serializer
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)  # 获取当前登录用户的收藏表

    # def perform_create(self, serializer):  # 收藏数+1  也可以用信号量机制完成
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()


class LeavingMessageViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    """
    # 必须在views页面设置 permission_classes 和authentication_classes 否则前端无法显示数据 因为传的是'AnonymousUser'  而不是在serializer里设置
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):  # 涉及到增删查改全部操作后,可以直接引用ModelViewSet
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
