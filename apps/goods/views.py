from rest_framework import generics, viewsets, mixins, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .filters import GoodsFilter
from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer, \
    IndexCategorySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class GoodsPagination(PageNumberPagination):
    page_size = 10  # 默认每页显示的个数
    page_size_query_param = 'limit'  # 可以动态改变每页显示的个数
    page_query_param = 'page'  # 页码参数
    max_page_size = 100  # 最多显示多少页


# CacheResponseMixin的继承必须放在List之前.因此最好都放在第一个  CacheResponseMixin是缓存在内存的而不是磁盘上
# 一般对公共数据设置缓存比较好
# 设置CacheResponseMixin后可能需要设置下settings
class GoodsListViewset(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表,分页,过滤,搜索,排序
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)  # 限制api请求

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # drf自带token认证, 对接口认证从而保证当前端设置全局token时,不会拿不到公共数据
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 继承mixins.RetrieveModelMixin并且配置好router就可以直接获取指定id的商品
class CategoryListViewset(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    List:
        商品分类数据列表
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
