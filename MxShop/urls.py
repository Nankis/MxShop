"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView

from goods.views_base import GoodsListView

import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from goods.views import GoodsListViewset, CategoryListViewset, HotSearchsViewset, BannerViewset, IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from rest_framework_jwt.views import obtain_jwt_token
from trade.views import ShoppingCartViewset, OrderViewset

router = DefaultRouter()
router.register(r'goods', GoodsListViewset, base_name="goods")

# 配置商品分类的url
router.register(r'categorys', CategoryListViewset, base_name="categorys")

# 云片网验证码
router.register(r'codes', SmsCodeViewset, base_name="codes")

router.register(r'users', UserViewset, base_name="users")

# 用户收藏
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

# 用户留言
router.register(r'messages', LeavingMessageViewset, base_name="messages")

# 用户收货地址
router.register(r'address', AddressViewset, base_name="address")

# 购物车
router.register(r'banners', BannerViewset, base_name="banners")

# 订单
router.register(r'orders', OrderViewset, base_name="orders")

# 轮播图
router.register(r'orders', OrderViewset, base_name="orders")

# 首页商品系列分类
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

# goods_list = GoodsListViewSet.as_view({  #自定义绑定方式
#     'get': 'list',
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^', include(router.urls)),  # 路由跳转根目录

    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    url(r'docs/', include_docs_urls(title='慕学生鲜')),  # 一定不能有^和$!

    # drf自带token认证
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口 ,因为第三方登录也存在login 所以在此处的url必须精准匹配,以^开头,$结尾
    url(r'^login/$', obtain_jwt_token),

    # 第三方登录url
    url('', include('social_django.urls', namespace='social'))
]
