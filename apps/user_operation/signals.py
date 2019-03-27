# -*- coding: utf-8 -*-
__author__ = 'Ginseng'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from user_operation.models import UserFav


# 商品收藏总数
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:  # 首次创建时,created为True
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


# 商品取消收藏总数
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
