from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from Fohow.permissions import IsAdminOrReadOnly
from django.db.models import Q
from .models import Basket, Category, Product
from .serializers import (BasketSerializer, CategorySerializer,
                          ProductSerializer)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FiltersProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Береме параметры из url
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        category_names = self.request.GET.getlist('categories')
        if min_price == None and max_price == None:
            return Product.objects.filter(categories__name__in=category_names)
        return Product.objects.filter(
            Q(categories__name__in=category_names) |
            Q(price__gte=min_price) &
            Q(price__lte=max_price)
            )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = ProductSerializer(queryset, many=True).data
        return Response({'products': serialized_data}, status=status.HTTP_200_OK)
    


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated, )

    # Переопределил queryset для одного юзера
    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)
    
    # Логика создания корзины
    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product'] # Берем данные из запроса
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product': 'There is no product with this ID'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(product_id=product_id, user=request.user)
            serializer = self.get_serializer(obj)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product': 'product id is required'}, status=status.HTTP_400_BAD_REQUEST)


class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('query', '')  # Получите параметр запроса "query"
        # Используйте фильтр для поиска товаров по имени (или другим полям) по запросу
        queryset = Product.objects.filter(name__icontains=query)
        return queryset
