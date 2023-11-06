from products.models import Basket


# MODELS METHODS
# Order
def update_after_success_payments(self):
    baskets = Basket.objects.filter(user=self.initiator)
    self.status = self.PAID
    purchased_item = []
    total_price = 0.0

    for basket in baskets:
        purchased_item.append(basket.de_json())
        total_price += basket.product_sum()

    self.basket_history = {
        "purchased_item": purchased_item,
        "total_price": total_price,
    }
    baskets.delete()
    self.save()


def update_after_canceled_payments(self):
    baskets = Basket.objects.filter(user=self.initiator)
    self.status = self.NOT_PAID
    baskets.delete()
    self.save()
