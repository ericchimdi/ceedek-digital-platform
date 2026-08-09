from django.contrib import admin
from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'status', 'user', 'submitted_at']
    list_filter = ['status', 'service']
    search_fields = ['name', 'email', 'company']