from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'questAI/index.html')

def home(request):
    return HttpResponse("Test for Home Page")

def login(request):
    return HttpResponse("Test for Login Page")

def signup(request):
    return HttpResponse("Test for Sign-Up Page")

def basket(request):
    return HttpResponse("Test for Basket Page")

def topup(request):
    return HttpResponse("Test for Top Up Page")

def checkout(request):
    return HttpResponse("Test for Checkout Page")

