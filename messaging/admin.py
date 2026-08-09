from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['project', 'sender', 'is_read', 'sent_at']
    list_filter = ['is_read']