from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib import messages


def home(request):
    return render(request, "ordering_website/home.html")


def registration_page(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            current_username = form.cleaned_data.get("username")
            print(current_username)
            messages.success(request, "Account was created successfully")
            return redirect("login")
    else:
        form = CreateUserForm()

    return render(request, "ordering_website/registration_page.html", {"form": form})
