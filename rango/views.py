from django.shortcuts import render

#3.4 - Creating a view
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there partner!")