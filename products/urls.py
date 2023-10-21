from django.urls import path, include
from django.conf import settings

from rest_framework import routers
from .views import ProductModelViewSet, CategoryModelViewSet, ProductSearchView, BasketModelViewSet


app_name = 'products'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'categories', CategoryModelViewSet)
router.register(r'baskets', BasketModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('search/', ProductSearchView.as_view(), name='search-list'),
]