from django.contrib import admin
from .models import User, EmailVerification
from products.admin import BasketAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username',)
    inlines = (BasketAdmin, )
    readonly_fields = ('last_login', 'date_joined')

    
@admin.register(EmailVerification)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiration',)