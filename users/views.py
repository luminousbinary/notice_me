# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
# from django.contrib import messages
# Create your views here.

def loginPage(request):
    return render(request, 'login.html')


