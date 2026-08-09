from django.conf import settings
from django.db import models

from projects.models import Project


class Document(models.Model):
    """A file attached to a Project, optionally hidden from clients."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='documents',
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='uploaded_documents',
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/%Y/%m/')
    description = models.TextField(blank=True)
    visible_to_client = models.BooleanField(default=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title