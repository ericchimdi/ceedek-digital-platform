from django import forms

from quotes.models import Quote


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


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = [
            'name', 'email', 'company', 'service',
            'project_description', 'budget', 'timeline', 'additional_info',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'company': forms.TextInput(attrs={'placeholder': 'Your company (optional)'}),
            'project_description': forms.Textarea(attrs={'placeholder': 'Describe what you need built or fixed...'}),
            'additional_info': forms.Textarea(attrs={'placeholder': 'Anything else we should know?'}),
        }