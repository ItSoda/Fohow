from django.db import models

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
    categories = models.ManyToManyField(Category)
    images = models.ManyToManyField(Image)

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.categories.all().first()}"
