# MODELS METHODS
# Basket
def product_sum(product_price, quantity):
    return int(product_price * quantity)


def de_json(product_name, quantity, product_price):
    basket_item = {
        "name": product_name,
        "quantity": quantity,
        "price": float(product_price),
        "sum": float(product_sum(product_price, quantity)),
    }
    return basket_item


def create_or_update(product_id, user):
    from products.models import Basket, Product

    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=user, product=product)

    if not baskets.exists():
        obj = Basket.objects.create(user=user, product=product, quantity=1)
        is_created = True
        return obj, is_created
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        is_created = False
        return basket, is_created


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


def basket_filter_for_one_user(self, queryset):
    return queryset.filter(user=self.request.user)


def product_not_exists(product_id):
    from .models import Product

    products = Product.objects.filter(id=product_id)
    if not products.exists():
        return True
    return False


def proccess_basket_create_or_update(product_id, self, request):
    from products.models import Basket

    return Basket.create_or_update(product_id=product_id, user=request.user)


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