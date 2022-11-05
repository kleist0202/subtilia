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

    items_in_cart = get_cart_items_number(request)

    wines = Wine.objects.all()

    data = {"is_logged": is_logged, "wines": wines, "items_in_cart": items_in_cart}
    return render(request, "ordering_website/home.html", data)


def registration_page(request):
    if "email" in request.session:
        return redirect("home")

    items_in_cart = get_cart_items_number(request)

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

    items_in_cart = get_cart_items_number(request)

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

    items_in_cart = get_cart_items_number(request)

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
            zip_code=zip,
        )
        logged_user = get_user(request)

        messages.success(request, "Dane zostały zaktualizowane.")

    data = {"is_logged": is_logged, "user": logged_user, "items_in_cart": items_in_cart}

    return render(request, "ordering_website/profile.html", data)


def cart_page(request):
    is_logged = False
    cart_products = []
    whole_products = []
    total_price = 0
    sum_price = 0

    qty = 1

    for id, qty in request.session["cart"].items():
        if request.method == "POST":
            qty = request.POST["product_" + str(id)]

            dic = request.session["cart"]
            dic[str(id)] = int(qty)
            request.session["cart"] = dic

        cp = Wine.objects.get(pk=id)
        price = int(qty) * float(cp.price)
        whole_products.append([cp, qty, price])
        sum_price += price

    if "email" in request.session:
        is_logged = True

    total_price = float(sum_price) + 9.99

    items_in_cart = get_cart_items_number(request)

    data = {
        "is_logged": is_logged,
        "whole_products": whole_products,
        "items_in_cart": items_in_cart,
        "sum_price": sum_price,
        "total_price": total_price,
    }
    return render(request, "ordering_website/cart_page.html", data)


def get_cart_items_number(request):
    if "cart" not in request.session:
        return 0

    items = 0
    for _, k in request.session["cart"].items():
        items += k
    return items


def add_to_cart(request, wine_id):
    # del request.session["cart"]
    if "cart" not in request.session:
        print("New session")
        request.session["cart"] = {}

    print(wine_id,request.session["cart"].keys())
    if str(wine_id) not in request.session["cart"].keys():
        print("New wine")
        request.session["cart"][str(wine_id)] = 0

    dic = request.session["cart"]
    dic[str(wine_id)] += 1
    request.session["cart"] = dic
    print(request.session["cart"])

    return redirect("home")


def remove_from_cart(request, wine_id):
    if "cart" in request.session:
        dic = request.session["cart"]
        dic.pop(str(wine_id))
        request.session["cart"] = dic

    return redirect("cart_page")


def wine_page(request, wine_id):
    chosen_wine = Wine.objects.get(pk=wine_id)
    print(chosen_wine.name)

    items_in_cart = get_cart_items_number(request)

    data = {"wine": chosen_wine, "items_in_cart": items_in_cart}
    return render(request, "ordering_website/wine_page.html", data)
