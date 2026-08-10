from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:account')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data.get('phone', ''),
                country=form.cleaned_data.get('country', ''),
                role=User.Role.CLIENT,
            )
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            if user is not None:
                login(request, user)
            return redirect('accounts:account')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:account')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('accounts:account')
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('website:home')


@login_required
def account(request):
    return render(request, 'accounts/account.html')