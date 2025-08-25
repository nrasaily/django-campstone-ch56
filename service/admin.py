from django.contrib import admin
from .models import Service, Payment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_active", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("client", "amount", "currency", "method", "created_at")
    list_filter = ("status", "method", "currency")
    search_fields = ("client__full_name", "reference")

