from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to the Ricardo's directory")

# Create your views here.
