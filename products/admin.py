from django.contrib import admin
from .models import Product, Category, Image, Basket

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    fields = ('name', 'description', 'price', 'product_composition', 'packaging_standard', \
                'expiration_date', 'method_of_application', 'quantity', 'categories', 'images')
    search_fields = ('name', )
    ordering = ('name', )
    filter_horizontal = ['categories', 'images']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fields = ('name', )
    search_fields = ('name', )
    ordering = ('name', )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('img',)
    fields = ('img',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0