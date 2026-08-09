from django.db import models

from organizations.models import Organization
from projects.models import Project


class Invoice(models.Model):
    """Financial record tied to an Organization and a specific Project."""

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SENT = 'SENT', 'Sent'
        PAID = 'PAID', 'Paid'
        OVERDUE = 'OVERDUE', 'Overdue'
        CANCELLED = 'CANCELLED', 'Cancelled'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='invoices',
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name='invoices',
    )

    invoice_number = models.CharField(max_length=30, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, help_text='ISO 4217 currency code, e.g. USD, GBP')

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)

    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.invoice_number