from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User, Wine


def home(request):
    is_logged = False

    if "email" in request.session:
        is_logged = True
        logged_user = get_user(request)

    wines = Wine.objects.all()

    data = {"is_logged": is_logged, "wines":wines}
    return render(request, "ordering_website/home.html", data)


def registration_page(request):
    if "email" in request.session:
        return redirect("home")

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


def login_page(request):
    if "email" in request.session:
        return redirect("home")

    form = LoginUserForm()
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session["email"] = user.email
                return redirect("home")
            else:
                messages.error(request, "Invalid password for email: " + user.email)
        else:
            messages.error(request, "There is no such account")

    return render(request, "ordering_website/login_page.html", {"form": form})


def get_user(request):
    return User.objects.get(email=request.session["email"])


def logout(request):
    if "email" in request.session:
        del request.session["email"]
    return redirect("login")


def profile(request):
    if "email" in request.session:
        is_logged = True
        logged_user = get_user(request)

    if request.method == "POST":
        name = request.POST["name"]
        surname = request.POST["surname"]
        adrress = request.POST["adr"]
        city = request.POST["city"]
        phone = request.POST["phone"]
        zip = request.POST["zip"]

        current_user_email = get_user(request).email
        _ = User.objects.filter(email=current_user_email).update(
            name=name,
            surname=surname,
            address_and_number=adrress,
            city=city,
            phone_number=phone,
            zip_code=zip
        )
        logged_user = get_user(request)

        messages.success(request, 'Dane zostały zaktualizowane.')

    data = {"is_logged": is_logged, "user": logged_user}
    return render(request, "ordering_website/profile.html", data)
