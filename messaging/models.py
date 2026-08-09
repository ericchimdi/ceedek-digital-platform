from django.conf import settings
from django.db import models

from projects.models import Project


class Message(models.Model):
    """A single message in a Project's communication thread."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='sent_messages',
        null=True,
        blank=True,
    )

    content = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message on {self.project.name} at {self.sent_at:%Y-%m-%d %H:%M}'