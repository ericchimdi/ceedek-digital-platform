from django.shortcuts import render
from .forms import ContactForm, QuoteForm


def home(request):
    return render(request, 'website/home.html')


def services(request):
    return render(request, 'website/services.html')


def solutions(request):
    return render(request, 'website/solutions.html')


def projects(request):
    return render(request, 'website/projects.html')


def about(request):
    return render(request, 'website/about.html')


def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submitted = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'website/contact.html', {'form': form, 'submitted': submitted})


def quote(request):
    submitted = False
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            submitted = True
            form = QuoteForm()
    else:
        form = QuoteForm()
    return render(request, 'website/quote.html', {'form': form, 'submitted': submitted})