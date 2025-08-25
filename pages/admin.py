from django.contrib import admin
from .models import Client, TaxDocument, TaxFiling, Consultation


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display  = ("user", "full_name", "phone", "created_at")
    search_fields = ("full_name", "user__username", "phone", "email")


@admin.register(TaxDocument)
class TaxDocumentAdmin(admin.ModelAdmin):
    list_display  = ("client", "document_name", "uploaded_at")
    search_fields = ("document_name", "client__full_name")
    list_filter   = ("uploaded_at",)


@admin.register(TaxFiling)
class TaxFilingAdmin(admin.ModelAdmin):
    list_display  = ("client", "year", "filing_type", "status", "submitted_on")
    list_filter   = ("status", "filing_type", "year")
    search_fields = ("client__full_name",)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display  = ("client", "topic", "date", "created_at")
    list_filter   = ("date",)
    search_fields = ("topic", "client__full_name")
