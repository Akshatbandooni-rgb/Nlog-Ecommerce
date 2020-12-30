from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.


def handlelogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You are logged out succesfully')
        return redirect("shopHome")

    return HttpResponse('Error 404-Forbidden')
