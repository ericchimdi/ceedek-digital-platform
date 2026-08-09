from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'organization', 'project', 'amount', 'currency', 'status', 'due_date']
    list_filter = ['status', 'currency']
    search_fields = ['invoice_number', 'organization__name']