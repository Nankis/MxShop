# -*- coding: utf-8 -*-
from django.views.generic.base import View

from goods.models import Goods

__author__ = 'Ginseng'


class GoodsListView(View):
    def get(self, request):
        """
        通过django的view实现商品列表页
        :param request:
        :return:
        """
        goods = Goods.objects.all()[:10]
        import json
        from django.core import serializers
        json_data = serializers.serialize("json", goods)
        json_data = json.loads(json_data)  # json.loads:str转成dict   json.dumps : dict转成str
        from django.http import JsonResponse
        return JsonResponse(json_data, safe=False)
