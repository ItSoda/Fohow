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
