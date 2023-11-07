from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Fohow.permissions import IsAdminOrReadOnly
from products.services import (basket_filter_for_one_user,
                               filters_product_queryset,
                               proccess_basket_create_or_update,
                               product_not_exists, product_search,
                               product_serializer_queryset)

from .models import Basket, Category, Product
from .serializers import (BasketSerializer, CategorySerializer,
                          ProductCreateSerializer, ProductSerializer)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)

    # Переопределил queryset для одного юзера
    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return basket_filter_for_one_user(self, queryset)

    # Логика создания корзины
    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data["product"]  # Берем данные из запроса
            if product_not_exists(product_id):
                return Response(
                    {"product": "There is no product with this ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            obj, is_created = proccess_basket_create_or_update(
                product_id, self, request
            )
            serializer = self.get_serializer(obj)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response(
                {"product": "product id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get(
            "query", ""
        )  # Получите параметр запроса "query"
        # Используйте фильтр для поиска товаров по имени (или другим полям) по запросу
        queryset = product_search(query)
        return queryset
