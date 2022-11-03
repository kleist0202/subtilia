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

    items_in_cart = 0
    if "cart" in request.session:
        items_in_cart = len(request.session["cart"])

    wines = Wine.objects.all()

    data = {"is_logged": is_logged, "wines": wines,  "items_in_cart": items_in_cart}
    return render(request, "ordering_website/home.html", data)


def registration_page(request):
    if "email" in request.session:
        return redirect("home")

    items_in_cart = 0
    if "cart" in request.session:
        items_in_cart = len(request.session["cart"])

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

    data = {"form": form, "items_in_cart": items_in_cart}

    return render(request, "ordering_website/registration_page.html", data)


def login_page(request):
    if "email" in request.session:
        return redirect("home")

    items_in_cart = 0
    if "cart" in request.session:
        items_in_cart = len(request.session["cart"])

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

    data = {"form": form, "items_in_cart": items_in_cart}

    return render(request, "ordering_website/login_page.html", data)


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

    items_in_cart = 0
    if "cart" in request.session:
        items_in_cart = len(request.session["cart"])

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

    data = {"is_logged": is_logged, "user": logged_user, "items_in_cart": items_in_cart}

    return render(request, "ordering_website/profile.html", data)


def cart_page(request):
    is_logged = False
    cart_products = []

    items_in_cart = 0
    if "cart" in request.session:
        items_in_cart = len(request.session["cart"])

    if "cart" in request.session:
        wines_ids = request.session["cart"]
        cart_products = Wine.objects.filter(wine_id__in=wines_ids)

    if "email" in request.session:
        is_logged = True
        logged_user = get_user(request)

    data = {"is_logged": is_logged, "cart_products": cart_products, "items_in_cart": items_in_cart}
    return render(request, "ordering_website/cart_page.html", data)


def add_to_cart(request, wine_id):
    if "cart" not in request.session:
        print("New session")
        request.session["cart"] = []

    saved_list = request.session["cart"]
    saved_list.append(wine_id)
    request.session['cart'] = saved_list

    return redirect("home")


def remove_from_cart(request, wine_id):
    if "cart" in request.session:
        saved_list = request.session["cart"]
        saved_list = [i for i in saved_list if i != wine_id]
        request.session['cart'] = saved_list

    return redirect("cart_page")
