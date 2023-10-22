from django.contrib import admin

from products.admin import BasketAdmin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username',)
    inlines = (BasketAdmin, )
    readonly_fields = ('last_login', 'date_joined')

    
@admin.register(EmailVerification)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiration',)