# -*- coding: utf-8 -*-
__author__ = 'Ginseng'
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    检测当前要操作的需权限资源是否是登录用户自己的资源

    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user
