from django.conf import settings
from django.db import models


class Quote(models.Model):
    """
    A service enquiry submitted via the public "Get a Quote" form.
    Works fully anonymously (user=None) and can later be linked to a
    User once staff convert the enquiry into a client relationship.
    """

    class Service(models.TextChoices):
        WEB_DEVELOPMENT = 'web_development', 'Web Development'
        BUSINESS_AUTOMATION = 'business_automation', 'Business Automation'
        DATA_ANALYTICS = 'data_analytics', 'Data Analytics'
        CUSTOM_SOFTWARE = 'custom_software', 'Custom Software Development'
        AI_SOLUTIONS = 'ai_solutions', 'AI Solutions'

    class Budget(models.TextChoices):
        UNDER_1000 = 'under_1000', 'Under $1,000'
        RANGE_1000_5000 = '1000_5000', '$1,000 – $5,000'
        RANGE_5000_15000 = '5000_15000', '$5,000 – $15,000'
        PLUS_15000 = '15000_plus', '$15,000+'

    class Timeline(models.TextChoices):
        ASAP = 'asap', 'As soon as possible'
        ONE_TO_THREE_MONTHS = '1_3_months', '1–3 months'
        THREE_TO_SIX_MONTHS = '3_6_months', '3–6 months'
        FLEXIBLE = 'flexible', 'Flexible'

    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        IN_REVIEW = 'IN_REVIEW', 'In Review'
        QUOTED = 'QUOTED', 'Quoted'
        CONVERTED = 'CONVERTED', 'Converted'
        DECLINED = 'DECLINED', 'Declined'

    name = models.CharField(max_length=150)
    email = models.EmailField()
    company = models.CharField(max_length=150, blank=True)
    service = models.CharField(max_length=30, choices=Service.choices)
    project_description = models.TextField()
    budget = models.CharField(max_length=20, choices=Budget.choices, blank=True)
    timeline = models.CharField(max_length=20, choices=Timeline.choices, blank=True)
    additional_info = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='quotes',
        null=True,
        blank=True,
        help_text='Set once staff link this quote to a client User during conversion.',
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} — {self.get_service_display()}'