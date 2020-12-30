from django.shortcuts import render, HttpResponse, redirect
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def handlelogin(request):
    form = forms.Login()
    if request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("shopHome")
            messages.error(request, "Invalid Credentials")
    return render(request, 'login/login.html', {'form': form})
