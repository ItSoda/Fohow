from django.db import models
from users.models import User

class Category(models.Model):
    """Model for categories"""

    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "Категории"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Image(models.Model):
    """Model for images"""

    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to="products_images")

    class Meta:
        verbose_name = "фотографию"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Фото {self.img}"


class Product(models.Model):
    """Model for products"""

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
        return f"Продукт: {self.name} | Категория: {self.categories.all().first()} | Цена: {self.price}"
    

# modelsQuerySet and modelsManager
class ReviewQuerySet(models.QuerySet):
    def total_rating(self):
        if self.count() > 0:
            return round(sum([review.rating for review in self])/self.count(), 2)
        else:
            return 0.0


class ReviewManager(models.Manager):
    def get_queryset(self):
        return ReviewQuerySet(self.model)
    
    def total_rating(self):
        return self.get_queryset().total_rating()


class Reviews(models.Model):
    """Model for reviews"""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    ReviewManager = ReviewManager()

    class Meta:
        verbose_name = "отзыву"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв: {self.user.email} | продукт: {self.product.name}"