# -*- coding: utf-8 -*-
__author__ = 'Ginseng'
"""
说明:
    对models操作会返回一些全局信号量,通过捕获信号量的机制,并对其操作可以实现一些想要的功能
    如,对其post_save后进行操作,对用户注册的密码进行加密存储
注意:
    1.需要在user.apps下进行配置
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:  # 首次创建时,created为True
        password = instance.password
        instance.set_password(password)
        instance.save()
