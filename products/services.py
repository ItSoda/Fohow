# Views
def filters_product_queryset(min_price, max_price, category_names):
    from django.db.models import Q
    from products.models import Product

    if min_price == None and max_price == None:
        return Product.objects.filter(categories__name__in=category_names)
    return Product.objects.filter(
        Q(categories__name__in=category_names)
        | Q(price__gte=min_price) & Q(price__lte=max_price)
    )


def product_serializer_queryset(queryset):
    from .serializers import ProductSerializer

    return ProductSerializer(queryset, many=True).data


def product_not_exists(product_id):
    from .models import Product

    products = Product.objects.filter(id=product_id)
    if not products.exists():
        return True
    return False



def product_search(query):
    from products.models import Product

    Product.objects.filter(name__icontains=query)

# Serializers
def get_total_sum(self, obj):
    from products.models import Basket
    return Basket.basketmanager.filter(user_id=obj.user.id).total_sum()

def product_instance(categories_ids, images_ids, **kwargs):
    from products.models import Product
    instance = Product.objects.create(**kwargs)

    instance.categories.set(categories_ids)
    instance.images.set(images_ids)
    return instance