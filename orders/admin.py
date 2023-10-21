from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'status', 'email')
    readonly_fields = ('initiator', )