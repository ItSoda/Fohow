from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Fohow.permissions import IsAdminOrReadOnly
from products.services import (filters_product_queryset, product_search,
                                product_serializer_queryset)

from .models import Category, Product
from .serializers import (CategorySerializer, ProductCreateSerializer, ProductSerializer)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        # return super().list(request, *args, **kwargs)
        return 1/0

    def create(self, request, *args, **kwargs):
        self.get_serializer = ProductCreateSerializer
        return super().create(request, *args, **kwargs)


class FiltersProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Берем параметры из url
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        categories_names = self.request.GET.getlist("categories")
        return filters_product_queryset(min_price, max_price, categories_names)

    def get(self, request, *args, **kwargs):
        serialized_data = product_serializer_queryset(self.get_queryset())
        return Response({"products": serialized_data}, status=status.HTTP_200_OK)


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get(
            "query", ""
        )  # Получите параметр запроса "query"
        # Используйте фильтр для поиска товаров по имени (или другим полям) по запросу
        queryset = product_search(query)
        return queryset
