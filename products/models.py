from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

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
        return f"Продукт: {self.name} | Категория: {self.categories.all().first()} | Цена: {self.price}"