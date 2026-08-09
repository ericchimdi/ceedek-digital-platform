from django.db import models


class Organization(models.Model):
    """
    Represents a client business. One organization can have multiple
    User accounts (accounts.User) associated with it, and all business
    relationships (projects, invoices) attach here rather than to an
    individual user.
    """

    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name