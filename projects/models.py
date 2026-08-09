from django.db import models

from organizations.models import Organization
from quotes.models import Quote


class Project(models.Model):
    """
    The core unit of client work. Belongs to an Organization (not an
    individual User), so every user in that organization can see it.
    """

    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'Planning'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        TESTING = 'TESTING', 'Testing'
        LAUNCHED = 'LAUNCHED', 'Launched'
        ON_HOLD = 'ON_HOLD', 'On Hold'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='projects',
    )
    quote = models.ForeignKey(
        Quote,
        on_delete=models.SET_NULL,
        related_name='projects',
        null=True,
        blank=True,
        help_text='The quote this project originated from, if any.',
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PLANNING)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_currency = models.CharField(max_length=3, blank=True, help_text='ISO 4217 currency code, e.g. USD, GBP')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.organization.name})'


class Milestone(models.Model):
    """A discrete deliverable or checkpoint within a Project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} ({self.project.name})'