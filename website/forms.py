from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Your full name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    company = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Your company (optional)'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'What is this about?'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Tell us more...'})
    )


class QuoteForm(forms.Form):
    SERVICE_CHOICES = [
        ('', 'Select a service'),
        ('web_development', 'Web Development'),
        ('business_automation', 'Business Automation'),
        ('data_analytics', 'Data Analytics'),
        ('custom_software', 'Custom Software Development'),
        ('ai_solutions', 'AI Solutions'),
    ]

    BUDGET_CHOICES = [
        ('', 'Select a budget range'),
        ('under_1000', 'Under $1,000'),
        ('1000_5000', '$1,000 – $5,000'),
        ('5000_15000', '$5,000 – $15,000'),
        ('15000_plus', '$15,000+'),
    ]

    TIMELINE_CHOICES = [
        ('', 'Select a timeline'),
        ('asap', 'As soon as possible'),
        ('1_3_months', '1–3 months'),
        ('3_6_months', '3–6 months'),
        ('flexible', 'Flexible'),
    ]

    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Your full name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    company = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Your company (optional)'})
    )
    service = forms.ChoiceField(choices=SERVICE_CHOICES)
    project_description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe what you need built or fixed...'})
    )
    budget = forms.ChoiceField(choices=BUDGET_CHOICES, required=False)
    timeline = forms.ChoiceField(choices=TIMELINE_CHOICES, required=False)
    additional_info = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Anything else we should know?'}),
        required=False
    )