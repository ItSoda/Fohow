from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Product, Category, Basket
from .serializers import ProductSerializer, CategorySerializer, BasketSerializer
from Fohow.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
