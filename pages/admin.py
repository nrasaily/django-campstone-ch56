from django.contrib import admin
from .models import Client, TaxDocument, TaxFiling, Consultation, Payment

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "created_at")
    search_fields = ("full_name", "email")

@admin.register(TaxDocument)
class TaxDocumentAdmin(admin.ModelAdmin):
    list_display = ("document_name", "client", "uploaded_at")
    list_filter = ("uploaded_at",)

@admin.register(TaxFiling)
class TaxFilingAdmin(admin.ModelAdmin):
    list_display = ("client", "year", "filing_type", "status", "submitted_on")
    list_filter = ("status", "year", "filing_type")
    search_fields = ("client__full_name",)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("client", "topic", "date")
    list_filter = ("date",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("client", "amount", "method", "paid_on")
    list_filter = ("method",)
