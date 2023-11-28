from django.contrib import admin

from .models import EmailVerification, User


class EmailVerificationAdmin(admin.TabularInline):
    model = EmailVerification
    fields = ("user", "expiration",)
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username",)
    inlines = (EmailVerificationAdmin,)
    readonly_fields = ("last_login", "date_joined")