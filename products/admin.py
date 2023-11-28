from django.contrib import admin

from .models import Category, Image, Product, Reviews


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    fields = (
        "name",
        "description",
        "price",
        "product_composition",
        "packaging_standard",
        "expiration_date",
        "method_of_application",
        "quantity",
        "categories",
        "images",
    )
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ["categories", "images"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    search_fields = ("user",)
    ordering = ("user",)