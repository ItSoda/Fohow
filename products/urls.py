from django.urls import include, path
from rest_framework import routers

from .views import (CategoryModelViewSet,
                    FiltersProductListView, ProductModelViewSet,
                    ProductSearchView)

app_name = "products"

router = routers.DefaultRouter()
router.register(r"products", ProductModelViewSet, basename="products")
router.register(r"categories", CategoryModelViewSet, basename="categories")


urlpatterns = [
    path("", include(router.urls)),
    path("search/", ProductSearchView.as_view(), name="search-list"),
    path("product_filters/", FiltersProductListView.as_view(), name="product_filters"),
]
