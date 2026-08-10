from django.contrib import admin
from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'service', 'status', 'user', 'submitted_at']
    list_filter = ['status', 'service']
    search_fields = ['name', 'email', 'company']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at']

    fieldsets = (
        ('Submitted by visitor', {
            'fields': ('name', 'email', 'company', 'service', 'project_description', 'budget', 'timeline', 'additional_info', 'submitted_at'),
        }),
        ('Staff management', {
            'fields': ('status', 'user'),
        }),
    )