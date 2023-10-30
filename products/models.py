from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "Категории"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Image(models.Model):
    img = models.ImageField(upload_to="products_images")

    class Meta:
        verbose_name = "фотографию"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Фото {self.img}"


class Product(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_composition = models.TextField()
    packaging_standard = models.TextField()
    expiration_date = models.CharField(max_length=150)
    method_of_application = models.TextField()
    quantity = models.PositiveBigIntegerField(default=0)
    categories = models.ManyToManyField(Category)
    images = models.ManyToManyField(Image)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.categories.all()[0]} | Цена: {self.price}"


# modelsQuerySet and modelsManager
class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum([basket.sum() for basket in self])

    def total_quantity(self):
        return sum([basket.quantity() for basket in self])


class BasketManager(models.Manager):
    def get_queryset(self):
        return BasketQuerySet(self.model)

    def total_sum(self):
        return self.get_queryset().total_sum()

    def total_quantity(self):
        return self.get_queryset().total_quantity()


class Basket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    basketmanager = BasketManager()

    class Meta:
        verbose_name = "корзину"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина для {self.user} | Продукт {self.product}"

    def sum(self):
        return int(self.product.price * self.quantity)

    def de_json(self):
        basket_item = {
            "name": self.product.name,
            "quantity": self.quantity,
            "price": float(self.product.price),
            "sum": float(self.sum()),
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
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
