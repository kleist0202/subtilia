from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "ordering_website/home.html")


# Create your views here.
