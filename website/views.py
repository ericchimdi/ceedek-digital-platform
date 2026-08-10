from django.shortcuts import render, redirect
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
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user if request.user.is_authenticated else None
            new_quote.save()
            return redirect('website:quote_success')
    else:
        form = QuoteForm()
    return render(request, 'website/quote.html', {'form': form})


def quote_success(request):
    return render(request, 'website/quote_success.html')