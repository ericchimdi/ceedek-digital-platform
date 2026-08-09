from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'uploaded_by', 'visible_to_client', 'uploaded_at']
    list_filter = ['visible_to_client']