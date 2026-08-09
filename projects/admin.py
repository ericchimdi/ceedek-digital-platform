from django.contrib import admin
from .models import Project, Milestone


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'status', 'start_date', 'end_date']
    list_filter = ['status']
    search_fields = ['name', 'organization__name']
    inlines = [MilestoneInline]